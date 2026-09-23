# One — Restructura One frontend

A React + Vite frontend for **One**, the conversational assistant that
sits in front of Restructura One's eight department agents. This repo is
the presentation layer only — retrieval, grounding, and generation still
run on the existing Python stack (Groq gateway, FAISS + Sentence
Transformers retrieval, Pydantic contracts) described in
`RESTRUCTURA_ONE_MASTER_CONTEXT.md`.

## Stack

- **React 19 + Vite** — app shell and routing (`react-router-dom`)
- **Tailwind CSS v3** — styling, with the project's design tokens in
  `tailwind.config.js`
- **Framer Motion** — page-load choreography and message animations
- **React Three Fiber + drei** — the interactive 3D mark on the landing hero
- **Phosphor Icons** — the icon set used throughout
- **Geist Sans / Geist Mono** — self-hosted via `@fontsource`, no runtime
  Google Fonts request

## Getting started

\`\`\`bash
npm install
npm run dev      # start the dev server
npm run build    # production build to dist/
npm run preview  # preview the production build locally
\`\`\`

## Structure

\`\`\`
src/
  components/     UI building blocks (hero, department cards, chat UI)
  pages/          Home.jsx (landing) and Chat.jsx (department workspace)
  data/           departments.js — the single source of truth for all 8 agents
  hooks/          useChat.js — per-department conversation state
  lib/            mockAgent.js — local stand-in for the real backend call
\`\`\`

## Wiring up the real backend

Right now `src/lib/mockAgent.js` simulates a call to the orchestrator and
returns a response shaped like the project's real `AgentResponse` contract
(`answer`, `citations`, `proposed_action`). Once the backend exposes an
HTTP endpoint for `AgentOrchestrator.route()`, replace the body of
`mockAgentCall` (or swap the import in `src/hooks/useChat.js`) with a
`fetch()` call to that endpoint. No other component needs to change —
every component downstream (`MessageBubble`, `CitationChip`,
`ProposedActionCard`) already renders that exact shape.

\`\`\`js
// src/hooks/useChat.js
const response = await fetch('/api/departments/' + departmentSlug + '/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: text, history: store[departmentSlug] }),
}).then((r) => r.json());
\`\`\`

## Department data

Every department card, chat header, and suggested prompt set is driven by
`src/data/departments.js`. The `slug` values match the backend's
department keys (`finance`, `risk_restructuring`, `sales`, `it`, `hr`,
`marketing`, `legal_compliance`, `customer_support`) so routing stays in
sync with the orchestrator without renaming anything on either side.

## Design notes

- Palette, type, and motion tokens live in `tailwind.config.js` and
  `src/index.css` — a navy/slate base (`base-*`) with a restrained
  blue/teal accent pair (`signal-*` / `current-*`), matching the direction
  already set for Restructura One's UI.
- The 3D orb (`src/components/OrbScene.jsx`) is isolated as its own leaf
  component and driven entirely inside `useFrame`, so pointer movement
  never triggers a React re-render elsewhere in the tree.
- Department switching is a single click in the rail — no confirmation
  step, no modal — per the product's "no complex multi-step flows"
  requirement. Conversation history stays isolated per department.
- Proposed actions are always rendered in their own visually distinct
  card with an "awaiting human review" label — never styled as completed
  or approved, matching the product's human-review requirement.
- `prefers-reduced-motion` is respected globally in `src/index.css`.

## Known gaps (by design, for this handoff)

- No authentication — matches the current state of the real project.
- Chat responses are simulated locally (`mockAgent.js`); wire the real
  endpoint per the section above before this goes further than a demo.
- No test suite yet for the frontend (the Python backend has its own,
  per the master context doc).

## Running end-to-end (frontend + real backend)

This folder lives inside the main `restructura-one` repo, on the
`streamlit` branch (a branch name only — Streamlit itself has been
removed from this codebase), as `frontend/`. Run both halves from the
repo root:

1. **Backend** — from the repo root (one level up from this folder):
   ```bash
   python -m venv .venv && source .venv/bin/activate   # or your usual env setup
   pip install -r requirements.txt
   cp .env.example .env    # then fill in GROQ_API_KEY
   uvicorn api.main:app --reload --port 8000
   ```
   Visit `http://localhost:8000/api/health` — you should see `{"status":"ok"}`.

2. **Frontend** — in a second terminal, from this `frontend/` folder:
   ```bash
   cp .env.example .env.local   # defaults already point at localhost:8000
   npm install
   npm run dev
   ```
   Open the printed local URL, pick a department, and ask a real question —
   it now calls the Groq-backed orchestrator instead of `mockAgent.js`.

Set `VITE_USE_MOCK=true` in `.env.local` any time you want to work on the
frontend without the Python backend running.
