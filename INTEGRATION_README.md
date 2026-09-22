# Restructura One — Phase 1 scaffold (React + FastAPI)

This adds an API layer and a Next.js frontend **alongside** your existing
Streamlit app — nothing in `core/`, `agents/`, `data/`, or `app.py` is
modified or deleted. Streamlit keeps working as your fallback demo until
the new stack is verified end to end.

## 0. Branch first

```powershell
git checkout main
git pull origin main
git checkout -b develop
git push -u origin develop
```

Do all of this work on `develop`. Do not open a PR into `main` until the
new stack has been run locally, tested, and reviewed by you and Awantika.

## 1. Where these files go

Copy this scaffold into your repo root so it looks like:

```
restructura-one/
├── agents/              (unchanged)
├── core/                (unchanged)
├── data/                (unchanged)
├── tests/               (unchanged)
├── app.py               (unchanged — Streamlit still works)
├── requirements.txt     (unchanged)
├── api/                 <-- NEW
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/             <-- NEW (separate Next.js project)
│   └── ... (all files as given)
└── docker-compose.yml    <-- NEW
```

## 2. Before you run anything — verify these against your real code

`api/main.py` has three assumptions flagged in its docstring that WILL
break the app if wrong. Open `core/app_bootstrap.py` and
`core/schemas/agent_contracts.py` and confirm:

1. **The builder function name** in `core/app_bootstrap.py` that returns
   a ready-to-use `AgentOrchestrator` (the code tries a few common names
   — `build_orchestrator`, `bootstrap_orchestrator`, etc. — and tells you
   in `/health` if none matched).
2. **`AgentResponse`'s real field names.** The code assumes something
   like `answer`, `citations`, `proposed_actions` — adjust the
   `.get(...)` calls in `main.py`'s `chat()` and `chat_ws()` if the real
   names differ.
3. **`Department` enum values** must match the slugs in
   `frontend/lib/departments.ts` exactly (`risk_restructuring`,
   `finance`, `sales`, `it`, `hr`, `marketing`, `legal_compliance`,
   `customer_support`) — these were inferred from your master context
   file, not read from source. Fix either side if they don't match.

Don't skip this — run `python -c "from core import app_bootstrap; print(dir(app_bootstrap))"`
first and report back before wiring further.

## 3. Run the backend locally

```powershell
pip install -r requirements.txt
pip install -r api/requirements.txt
$env:PYTHONPATH = (Get-Location).Path
Copy-Item api\.env.example .env   # fill in your real GROQ_API_KEY
uvicorn api.main:app --reload --port 8000
```

Visit `http://localhost:8000/health` — it should report
`"orchestrator_ready": true`. If not, the `error` field tells you what to
fix (see step 2).

## 4. Run the frontend locally

```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Visit `http://localhost:3000`.

## 5. What's real vs. what's a placeholder right now

**Working as-is:**
- Homepage, department directory, workspace routing, chat UI, empty
  states, source/action panel, dark navy/teal theme, reduced-motion
  support.
- `POST /chat` — full request/response against your real orchestrator
  (once step 2 is verified).

**Placeholder / needs a follow-up change:**
- `WS /ws/chat` currently sends the **complete** answer chunked into
  fake "tokens" after the orchestrator finishes — it is not real
  token-level streaming yet. True streaming needs a small, additive
  change to `core/llm/groq_gateway.py` (Groq's SDK supports
  `stream=True`) plus threading that through each agent's call path.
  That touches shared code Awantika may be working in — coordinate
  before making it, per your own project rules. Do it as its own
  reviewed step once the non-streaming path is confirmed working.
- `SourcesPanel.tsx` reads `c.source ?? c.title ?? c.excerpt` and
  `a.description ?? a.title` as guesses at your `SourceCitation` /
  `ActionProposal` field names — fix once confirmed.

## 6. Testing

- Keep running `python -m pytest -q` — none of this touches what those
  88 tests cover.
- Add `tests/api/test_main.py` using FastAPI's `TestClient` once step 2
  is verified, so the new layer has its own coverage before it goes near
  `main`.

## 7. Deploying (once verified on `develop`)

- **Frontend → Vercel:** import the repo, set root directory to
  `frontend/`, add `NEXT_PUBLIC_API_BASE_URL` as an env var pointing at
  your deployed API.
- **Backend → Fly.io or Render:** deploy `api/Dockerfile` from the repo
  root (not from inside `api/`), set the same secrets you already use in
  Streamlit Cloud (`GROQ_API_KEY`, `GROQ_MODEL`, `EMBEDDING_MODEL`) plus
  `FRONTEND_ORIGIN` set to your Vercel URL.
- Keep Streamlit Community Cloud deployment live and untouched until the
  new stack is validated — don't cut over until you're ready.

## 8. Merge to main

Only after: local run works end to end, `/health` is green, pytest
suite passes, Awantika has reviewed any `core/` changes (streaming),
and you've smoke-tested all 8 departments in the new UI.
