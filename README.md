# Restructura One --- The Intelligent AI Workforce

**Restructura One** is an academic prototype of an enterprise AI
workspace that brings eight department-specific assistants into a
single workspace: a FastAPI backend orchestrating eight RAG agents,
served through a React frontend. Each assistant uses retrieval-augmented
generation (RAG) over its own synthetic departmental knowledge base and
a shared Groq LLM gateway.

> **Academic demo notice:** Restructura One is a decision-support
> prototype using fictional company information and synthetic
> knowledge-base documents. It is not an autonomous approval system.
> Review outputs, cited evidence, and proposed actions before taking
> consequential action.

## Live Demo

-   **GitHub:** https://github.com/Parv-065040/restructura-one

## What it does

-   One workspace (React frontend + FastAPI backend) for eight
    specialized departmental AI assistants.
-   Department-scoped conversations and context-aware follow-up
    questions.
-   Retrieval-augmented answers grounded in each department's knowledge
    base.
-   Source citations where supporting retrieved material is available.
-   Shared response/action contracts and orchestration across agents.
-   Human-led review for consequential recommendations or proposed
    actions.

## Departmental AI workforce

  Department             Example focus
  ---------------------- -------------------------------------------------
  Risk & Restructuring   Risk cases and restructuring decision support
  Finance                Financial analysis and finance knowledge
  Sales                  Sales processes and sales knowledge
  IT                     IT support and technology knowledge
  HR                     Human-resources policies and processes
  Marketing              Marketing strategy and execution knowledge
  Legal & Compliance     Compliance guidance and policy knowledge
  Customer Support       Customer-service knowledge and response support

The assistants use a common contract while retaining department-specific
retrieval sources and prompts.

## Architecture

``` mermaid
flowchart TB
    U[User] --> UI[React Frontend<br/>frontend/]
    UI --> API[FastAPI<br/>api/main.py]
    API --> ORCH[Agent Orchestrator<br/>core/orchestrator.py]
    ORCH --> CONTRACT[Shared Agent Contracts<br/>AgentContext · AgentResponse · ActionProposal]

    subgraph AGENTS[Eight Department Agents]
      A1[Risk & Restructuring]
      A2[Finance]
      A3[Sales]
      A4[IT]
      A5[HR]
      A6[Marketing]
      A7[Legal & Compliance]
      A8[Customer Support]
    end

    CONTRACT --> AGENTS

    subgraph RAG[Department-Scoped Retrieval]
      R1[(Risk KB)]
      R2[(Finance KB)]
      R3[(Sales KB)]
      R4[(IT KB)]
      R5[(HR KB)]
      R6[(Marketing KB)]
      R7[(Legal & Compliance KB)]
      R8[(Customer Support KB)]
      RET[Local Retriever<br/>Sentence Transformers + FAISS]
    end

    AGENTS --> RET
    RET <--> RAG
    AGENTS --> GW[Shared Groq Gateway<br/>core/llm/groq_gateway.py]
    GW --> LLM[Groq API<br/>openai/gpt-oss-120b]
    LLM --> GW
    GW --> AGENTS

    AGENTS --> RESP[AgentResponse<br/>answer · citations · proposed actions]
    RESP --> ORCH
    ORCH --> API
    API --> UI
    UI --> HUMAN[Human reviews evidence<br/>and decides next steps]
```

### Request lifecycle

1.  The user selects a department and submits a question in the React
    frontend.
2.  The frontend calls `POST /api/departments/{department}/ask`, which
    builds an `AgentContext`, including department/session details and
    bounded conversation history.
3.  The orchestrator routes the request to the selected department
    agent.
4.  The agent retrieves relevant passages from its own knowledge base
    using the local retrieval layer.
5.  The agent combines the current query, bounded conversation context,
    and retrieved evidence, then calls the shared Groq gateway.
6.  The agent returns a structured `AgentResponse`, which may include an
    answer, source citations, and proposed actions.
7.  The frontend displays the response. A human reviews the evidence
    and any proposed action before acting.

Conversation history is context, not verified evidence. Retrieved
knowledge-base material should ground factual claims; prior assistant
responses can be fallible.

## Technology stack

-   **Frontend:** React + Vite (`frontend/`)
-   **API:** FastAPI (`api/main.py`)
-   **LLM provider:** Groq API (`openai/gpt-oss-120b`, configurable)
-   **RAG / vector retrieval:** FAISS and Sentence Transformers
-   **Language:** Python (backend), JavaScript (frontend)
-   **Contracts / validation:** Pydantic
-   **Configuration:** environment variables (`.env`)
-   **Testing:** pytest

## Repository layout

``` text
restructura-one/
├── agents/                     # Department-specific agent implementations
├── api/
│   └── main.py                 # FastAPI app — the frontend's entry point
├── core/
│   ├── conversation/           # Conversation-history formatting
│   ├── llm/                    # Shared Groq gateway
│   ├── rag/                    # Local retrieval components
│   ├── schemas/                # Shared agent contracts
│   ├── agent_interface.py      # Common agent interface
│   ├── app_bootstrap.py        # Agent and service initialization
│   └── orchestrator.py         # Department routing/orchestration
├── data/
│   └── knowledge_base/         # Synthetic, department-scoped knowledge
├── frontend/                   # React + Vite UI (see frontend/README.md)
├── tests/                      # Unit and integration tests
├── requirements.txt
└── README.md
```

Folder contents may evolve as the project develops.

## Run locally

**Quick start (after first-time setup below):** `./dev.sh` (macOS/Linux)
or `.\dev.ps1` (Windows) starts the API and the frontend together.

### 1. Clone the repository

``` bash
git clone https://github.com/Parv-065040/restructura-one.git
cd restructura-one
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

``` powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file (do not commit it):

``` env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CORS_ORIGINS=http://localhost:5173
```

Keep `.env` out of version control. Never publish API keys in source
code, screenshots, logs, or GitHub.

### 5. Start the API

``` bash
uvicorn api.main:app --reload --port 8000
```

Visit `http://localhost:8000/api/health` — you should see
`{"status":"ok"}`.

### 6. Start the frontend

In a second terminal:

``` bash
cd frontend
cp .env.example .env.local   # defaults already point at localhost:8000
npm install
npm run dev
```

Open the printed local URL (typically `http://localhost:5173`), pick a
department, and ask a question.

## Run tests

From the repository root:

``` powershell
$env:PYTHONPATH = (Get-Location).Path
python -m pytest -q
```

The latest reported local test run during deployment preparation was
**88 passed**. Re-run tests against the current checkout before relying
on that result.

## Safety, governance, and limitations

-   The prototype uses synthetic/fictional company knowledge; it is not
    a source of real company policy.
-   LLM responses can be incorrect or incomplete. Retrieval and
    citations do not guarantee correctness.
-   Conversation history is bounded context and must not be treated as
    authoritative evidence.
-   Proposed actions are not executed automatically; a human must review
    and authorize consequential steps.
-   Do not enter confidential, personal, regulated, or production
    customer data.
-   This demo is not a substitute for professional legal, financial, HR,
    compliance, or risk advice.

## Contributors

-   **Parv** 
-   **Awantika** 
-   **Aman**

## License

No license is specified yet. All rights reserved unless a license is
added to this repository.
