"""HTTP API for Restructura One.

Thin wrapper around the existing AgentOrchestrator — no agent, retrieval,
or gateway logic lives here. This is the backend's only entry point; the
React frontend (frontend/) is the only client.

Run from the repository root:

    uvicorn api.main:app --reload --port 8000

Requires GROQ_API_KEY in the environment or a local .env file, exactly
as core/llm/groq_gateway.py expects.
"""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.app_bootstrap import build_orchestrator
from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import AgentContext, Department

load_dotenv()
logger = logging.getLogger("restructura_one.api")

app = FastAPI(title="Restructura One API", version="0.1.0")

# Comma-separated list of allowed origins, e.g. "http://localhost:5173".
# Defaults to the Vite dev server so `npm run dev` works out of the box.
_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _origins if o.strip()],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Built once, lazily, on first request — not at import time — so the
# module can still be imported (e.g. for tests) without GROQ_API_KEY set.
_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        try:
            _orchestrator = build_orchestrator()
        except Exception as exc:
            logger.exception("Failed to build orchestrator")
            raise HTTPException(
                status_code=503,
                detail=(
                    "The assistant backend is not configured. Set "
                    "GROQ_API_KEY in your .env file and restart the API."
                ),
            ) from exc
    return _orchestrator


class ChatMessage(BaseModel):
    role: str
    content: str


class AskRequest(BaseModel):
    message: str
    # Bounded conversation history for this department only — the
    # frontend keeps history isolated per department, matching
    # core/conversation/history.py's expectations.
    history: list[ChatMessage] = Field(default_factory=list)
    session_id: str | None = None


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/departments/{department}/ask")
def ask(department: str, payload: AskRequest):
    try:
        dept = Department(department)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Unknown department: {department}")

    if not payload.message.strip():
        raise HTTPException(status_code=422, detail="message must not be empty.")

    orchestrator = get_orchestrator()

    context = AgentContext(
        department=dept,
        session_id=payload.session_id,
        metadata={
            "conversation_history": [m.model_dump() for m in payload.history],
        },
    )

    response = orchestrator.run(query=payload.message, context=context)
    return response.model_dump(mode="json")
