"""
Restructura One — API layer (Phase 1 scaffold)
================================================

Wraps the EXISTING core/ orchestrator (contracts, agents, Groq gateway,
RAG) behind FastAPI so a React/Next.js frontend can call it instead of
Streamlit. Nothing in core/ is modified by this file.

Confirmed against the real core/ code:
  - core.app_bootstrap.build_orchestrator(gateway=None, retriever_factory=LocalRetriever)
  - AgentContext fields: department, session_id, user_role, permissions, metadata
  - AgentResponse fields: department, answer, status, sources, actions, metadata
  - Department values: risk_restructuring, finance, sales, it, hr, marketing,
    legal_compliance, customer_support

Run locally:
    pip install -r api/requirements.txt
    uvicorn api.main:app --reload --port 8000

This does NOT touch app.py / Streamlit. Both can run side by side while
you validate the new stack.
"""

from __future__ import annotations

import inspect
import os
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Wire up the existing orchestrator.
# ---------------------------------------------------------------------------
_orchestrator = None
_bootstrap_error: str | None = None

try:
    from core import app_bootstrap  # type: ignore

    _orchestrator = app_bootstrap.build_orchestrator()
except Exception as exc:  # pragma: no cover - surfaced via /health instead
    _bootstrap_error = f"Failed to import/build orchestrator: {exc!r}"

try:
    from core.schemas.agent_contracts import AgentContext, Department  # type: ignore
except Exception as exc:  # pragma: no cover
    AgentContext = None  # type: ignore
    Department = None  # type: ignore
    if _bootstrap_error is None:
        _bootstrap_error = f"Failed to import agent_contracts: {exc!r}"


# ---------------------------------------------------------------------------
# API request/response models (the wire contract the frontend talks to —
# deliberately separate from AgentContext/AgentResponse so the frontend
# never depends on your internal core/ schema shape directly).
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    department: str = Field(..., description="e.g. 'finance', 'sales'")
    query: str
    session_id: str
    user_role: str = "analyst"
    permissions: list[str] = Field(default_factory=list)
    conversation_history: list[dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    department: str
    answer: str
    citations: list[dict[str, Any]] = Field(default_factory=list)
    proposed_actions: list[dict[str, Any]] = Field(default_factory=list)
    raw: dict[str, Any] = Field(default_factory=dict)


app = FastAPI(title="Restructura One API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        os.getenv("FRONTEND_ORIGIN", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok" if _orchestrator is not None else "degraded",
        "orchestrator_ready": _orchestrator is not None,
        "error": _bootstrap_error,
    }


@app.get("/departments")
def list_departments() -> list[str]:
    if Department is None:
        raise HTTPException(500, "Department enum not available — see /health")
    return [d.value if hasattr(d, "value") else str(d) for d in Department]


def _to_dict(obj: Any) -> Any:
    """Best-effort serialization for AgentResponse / nested contract objects."""
    if obj is None:
        return None
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, (list, tuple)):
        return [_to_dict(o) for o in obj]
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    return obj


def _build_context(req: ChatRequest):
    if AgentContext is None:
        raise HTTPException(500, "AgentContext not available — see /health")
    return AgentContext(
        department=req.department,
        session_id=req.session_id,
        user_role=req.user_role,
        permissions=req.permissions,
        metadata={"conversation_history": req.conversation_history},
    )


async def _run_orchestrator(query: str, context: Any) -> Any:
    if _orchestrator is None:
        raise HTTPException(500, f"Orchestrator not ready: {_bootstrap_error}")
    result = _orchestrator.run(query, context)
    if inspect.isawaitable(result):
        result = await result
    return result


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    context = _build_context(req)
    try:
        response = await _run_orchestrator(req.query, context)
    except HTTPException:
        raise
    except Exception as exc:
        # Deliberately generic to the client — never leak internals/secrets.
        raise HTTPException(502, f"Agent invocation failed: {type(exc).__name__}")

    payload = _to_dict(response) or {}
    return ChatResponse(
        department=req.department,
        answer=payload.get("answer", ""),
        citations=payload.get("sources", []),
        proposed_actions=payload.get("actions", []),
        raw=payload,
    )


@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket) -> None:
    """
    NOTE: this currently sends the FULL answer as one WS message once the
    orchestrator finishes — it is NOT true token-level streaming yet.
    Real streaming requires adding a streaming method to
    core/llm/groq_gateway.py (Groq's SDK supports `stream=True`) and
    threading it through the agent -> orchestrator call path. Do that as
    a deliberate, coordinated change to core/ — see the integration
    README for the exact patch shape. This endpoint is wired so the
    frontend's streaming UI can be built against it now and upgraded
    later without an API contract change.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            req = ChatRequest(**data)
            context = _build_context(req)
            try:
                response = await _run_orchestrator(req.query, context)
                payload = _to_dict(response) or {}
                answer = payload.get("answer", "")
            except Exception as exc:
                await websocket.send_json(
                    {"type": "error", "message": f"Agent invocation failed: {type(exc).__name__}"}
                )
                continue

            # Fake a stream client-side by chunking words — replace this
            # loop once groq_gateway exposes real token streaming.
            words = answer.split(" ")
            for i, w in enumerate(words):
                await websocket.send_json({"type": "token", "content": w + (" " if i < len(words) - 1 else "")})
            await websocket.send_json(
                {
                    "type": "done",
                    "citations": payload.get("sources", []),
                    "proposed_actions": payload.get("actions", []),
                }
            )
    except WebSocketDisconnect:
        pass
