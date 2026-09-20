# Restructura One --- The Intelligent AI Workforce

**Restructura One** is an academic prototype of an enterprise AI
workspace that brings eight department-specific assistants into one
Streamlit application. Each assistant uses retrieval-augmented
generation (RAG) over its own synthetic departmental knowledge base and
a shared Groq LLM gateway.

> **Academic demo notice:** Restructura One is a decision-support
> prototype using fictional company information and synthetic
> knowledge-base documents. It is not an autonomous approval system.
> Review outputs, cited evidence, and proposed actions before taking
> consequential action.

## Live Demo

-   **Streamlit Community Cloud:** *Add your deployed app URL here*
-   **GitHub:** https://github.com/Parv-065040/restructura-one

## What it does

-   One Streamlit workspace for eight specialized departmental AI
    assistants.
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
    U[User / Professor] --> UI[Streamlit App<br/>app.py]
    UI --> WS[Department Workspace<br/>chat, history, follow-ups]
    WS --> ORCH[Agent Orchestrator<br/>core/orchestrator.py]
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
    ORCH --> UI
    UI --> HUMAN[Human reviews evidence<br/>and decides next steps]
```

### Request lifecycle

1.  The user selects a department and submits a question in Streamlit.
2.  The app builds an `AgentContext`, including department/session
    details and permitted conversation history.
3.  The orchestrator routes the request to the selected department
    agent.
4.  The agent retrieves relevant passages from its own knowledge base
    using the local retrieval layer.
5.  The agent combines the current query, bounded conversation context,
    and retrieved evidence, then calls the shared Groq gateway.
6.  The agent returns a structured `AgentResponse`, which may include an
    answer, source citations, and proposed actions.
7.  The UI displays the response. A human reviews the evidence and any
    proposed action before acting.

Conversation history is context, not verified evidence. Retrieved
knowledge-base material should ground factual claims; prior assistant
responses can be fallible.

## Technology stack

-   **UI:** Streamlit
-   **LLM provider:** Groq API (`openai/gpt-oss-120b`, configurable)
-   **RAG / vector retrieval:** FAISS and Sentence Transformers
-   **Language:** Python
-   **Contracts / validation:** Pydantic
-   **Configuration:** environment variables / Streamlit Secrets
-   **Testing:** pytest
-   **Hosting:** Streamlit Community Cloud

## Repository layout

``` text
restructura-one/
├── agents/                     # Department-specific agent implementations
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
├── tests/                      # Unit and integration tests
├── app.py                      # Streamlit entry point
├── requirements.txt
└── README.md
```

Folder contents may evolve as the project develops.

## Run locally

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

### 3. Install dependencies

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
```

Keep `.env` out of version control. Never publish API keys in source
code, screenshots, logs, or GitHub.

### 5. Start the app

``` powershell
# Windows PowerShell
$env:PYTHONPATH = (Get-Location).Path
streamlit run app.py --server.fileWatcherType none
```

Or, on macOS/Linux:

``` bash
PYTHONPATH=. streamlit run app.py
```

Streamlit will print the local URL (commonly `http://localhost:8501`).

## Deploy on Streamlit Community Cloud

1.  Connect Streamlit Community Cloud to the GitHub repository.
2.  Select the `main` branch and `app.py` as the app entry point.
3.  In **App settings → Secrets**, add the following TOML, substituting
    your private key:

``` toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

4.  Save and allow the app to restart.
5.  Open the deployed URL and test department selection, retrieval,
    citations, and follow-up questions.

Do not commit `.env` or paste secrets into README, GitHub issues, or
chat. The deployed app requires a valid Groq API key and outbound access
to the configured provider. First-time embedding/model initialization
may take time.

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

-   **Parv Jhamb** --- Streamlit workspace/UI, shared integration, and
    project development
-   **Awantika** --- Department-agent development and project
    collaboration

Update contributor roles if the final division of work differs.

## License

No license is specified yet. All rights reserved unless a license is
added to this repository.
