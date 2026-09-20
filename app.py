"""Streamlit entry point for Restructura One."""

import streamlit as st

from core.app_bootstrap import build_orchestrator
from core.schemas.agent_contracts import AgentContext, Department


st.set_page_config(
    page_title="Restructura One | AI Workspace",
    page_icon="🏢",
    layout="wide",
)

DEPARTMENTS = [
    ("Risk & Restructuring", Department.RISK_RESTRUCTURING, "📊",
     "Risk signals, restructuring options, and evidence-based insights."),
    ("Finance", Department.FINANCE, "💰",
     "Financial analysis, planning, and decision support."),
    ("Sales", Department.SALES, "📈",
     "Sales insights, pipeline questions, and customer opportunities."),
    ("IT", Department.IT, "🖥️",
     "Technology operations, troubleshooting, and IT knowledge."),
    ("Human Resources", Department.HR, "👥",
     "People policies, HR processes, and employee support."),
    ("Marketing", Department.MARKETING, "📣",
     "Campaign insights, customer understanding, and marketing strategy."),
    ("Legal & Compliance", Department.LEGAL_COMPLIANCE, "⚖️",
     "Compliance guidance and policy-grounded information."),
    ("Customer Support", Department.CUSTOMER_SUPPORT, "🎧",
     "Customer queries, service guidance, and support knowledge."),
]

DEPARTMENT_LOOKUP = {
    label: department
    for label, department, _, _ in DEPARTMENTS
}



def inject_custom_css():
    """Apply a polished enterprise theme without changing app behavior."""
    st.markdown("""
    <style>
    /* RESTRUCTURA_PREMIUM_THEME */
    :root {
        --ro-bg: #0b1120;
        --ro-panel: #111c2e;
        --ro-panel-2: #162338;
        --ro-border: rgba(148, 163, 184, 0.16);
        --ro-text: #e8eef8;
        --ro-muted: #94a8c4;
        --ro-accent: #38bdf8;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(14, 116, 144, .13), transparent 34%),
            linear-gradient(145deg, #0b1120 0%, #0d1728 55%, #101a2d 100%);
        color: var(--ro-text);
    }

    [data-testid="stHeader"] {
        background: rgba(11, 17, 32, .78);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1221 0%, #101b2d 100%);
        border-right: 1px solid var(--ro-border);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label {
        color: #b6c6dc;
    }

    h1, h2, h3 {
        color: #f3f7ff !important;
        letter-spacing: -0.035em;
    }

    h1 {
        font-weight: 750 !important;
        line-height: 1.15 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--ro-muted);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--ro-border);
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, rgba(22, 35, 56, .88), rgba(15, 27, 44, .88));
        border: 1px solid var(--ro-border) !important;
        border-radius: 16px !important;
        transition: border-color .18s ease, transform .18s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(56, 189, 248, .42) !important;
    }

    [data-testid="stButton"] button,
    [data-testid="stFormSubmitButton"] button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
        transition: all .18s ease;
    }

    [data-testid="stButton"] button[kind="primary"],
    [data-testid="stFormSubmitButton"] button[kind="primary"] {
        background: linear-gradient(110deg, #0284c7, #2563eb);
        border: 1px solid rgba(125, 211, 252, .3);
        color: white;
        box-shadow: 0 5px 18px rgba(2, 132, 199, .15);
    }

    [data-testid="stButton"] button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        border-color: #38bdf8;
        transform: translateY(-1px);
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        background: #0d1829;
        border: 1px solid #2b3c55;
        border-radius: 10px;
        color: #e8eef8;
    }

    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: #38bdf8;
        box-shadow: 0 0 0 1px #38bdf8;
    }

    [data-testid="stExpander"] {
        background: rgba(17, 28, 46, .72);
        border: 1px solid var(--ro-border);
        border-radius: 12px;
    }

    hr {
        border-color: var(--ro-border);
    }

    [data-testid="stMarkdownContainer"] a {
        color: #7dd3fc;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource(show_spinner="Initializing departmental assistants...")
def get_orchestrator():
    """Initialize the shared orchestrator once per Streamlit process."""
    return build_orchestrator()


def render_response(response):
    """Render a standardized agent response, sources, and proposed actions."""
    status = response.status.value

    if status == "success":
        st.success("Request completed")
    elif status == "insufficient_evidence":
        st.warning("Insufficient evidence")
    elif status == "needs_clarification":
        st.info("More information required")
    else:
        st.error("Assistant error")

    st.markdown(response.answer)

    if response.sources:
        with st.expander(f"Sources ({len(response.sources)})"):
            for index, source in enumerate(response.sources, start=1):
                st.markdown(
                    f"**{index}. {source.document_name}**  \n"
                    f"Source ID: `{source.source_id}`"
                )
                if source.relevance_score is not None:
                    st.caption(f"Relevance: {source.relevance_score:.2f}")
                if source.excerpt:
                    st.write(source.excerpt)

    if response.actions:
        st.subheader("Proposed actions")
        st.caption(
            "These are proposals only. No action is executed by this interface."
        )

        for action in response.actions:
            with st.container(border=True):
                st.markdown(f"**{action.action_type}**")
                st.write(action.description)
                st.caption(
                    f"Status: {action.status.value} | "
                    f"Approval required: "
                    f"{'Yes' if action.requires_approval else 'No'}"
                )


def render_dashboard():
    """Render the Restructura One homepage and departmental directory."""

    # Hero / company introduction
    st.title("RESTRUCTURA ONE")
    st.subheader("The Intelligent AI Workforce")
    st.markdown(
        "**One unified platform. Eight specialized AI agents. "
        "Smarter business automation.**"
    )

    st.write(
        "Restructura One is an enterprise AI workspace designed to help "
        "teams access department-specific intelligence, analyze business "
        "questions, and prepare informed next steps from a single interface."
    )

    st.caption(
        "Powered by Restructura Intelligence | "
        "RAG | Agentic AI | Business Process Automation"
    )

    st.divider()

    # Platform overview
    st.subheader("Your AI workspace")
    st.subheader("Your enterprise, connected with AI")
    st.write(
        "Explore a fictional Restructura company environment where "
        "specialized AI assistants support key business functions. "
        "Each assistant uses its own synthetic departmental knowledge "
        "base to provide context-aware decision support."
    )

    metric_cols = st.columns(2)
    metric_cols[0].metric("8", "Specialized AI Agents")
    metric_cols[1].metric("1", "Unified Workspace")
    st.caption("Decision governance: Human-led review of consequential actions.")

    st.info(
        "AI outputs are decision support, not autonomous approvals. "
        "Review evidence and approve consequential actions before acting. "
        "This academic prototype uses synthetic company data only."
    )

    # How it works
    st.subheader("How Restructura One works")
    step_cols = st.columns(2)

    with step_cols[0]:
        st.markdown("**01 - Choose**")
        st.write(
            "Select a department and its specialized AI assistant."
        )

    with step_cols[1]:
        st.markdown("**02 - Ask**")
        st.write(
            "Submit a business question grounded in that department's "
            "knowledge base."
        )

    st.markdown("**03 - Review**")
    st.write(
        "Review the response, supporting sources, and any proposed "
        "actions before deciding what to do."
    )

    st.divider()

    # Department directory / quick access
    st.subheader("Explore the AI workforce")
    st.write(
        "Choose a department to open its dedicated conversational workspace."
    )

    columns = st.columns(2)

    for index, (label, _, emoji, description) in enumerate(DEPARTMENTS):
        with columns[index % 2]:
            with st.container(border=True):
                st.subheader(f"{emoji}  {label}")
                st.write(description)

                if st.button(
                    f"Open {label}",
                    key=f"open_{index}",
                    use_container_width=True,
                ):
                    st.session_state.selected_department = label
                    st.rerun()


def render_department_workspace(label):
    """Render a conversational workspace for one department."""
    department = DEPARTMENT_LOOKUP[label]
    department_key = department.value

    if "department_chats" not in st.session_state:
        st.session_state.department_chats = {}

    chats = st.session_state.department_chats
    if department_key not in chats:
        chats[department_key] = []

    header_col, button_col = st.columns([5, 1])

    with header_col:
        st.title(label)
        st.caption("Department Assistant · Conversational Workspace")

    with button_col:
        if st.button("＋ New chat", key=f"new_chat_{department_key}"):
            chats[department_key] = []
            st.rerun()

    st.info(
        "Responses are decision support. Verify evidence and review "
        "consequential recommendations before acting."
    )

    st.caption(
        "Ask a business question or task. Responses use the "
        "department-specific knowledge base."
    )

    # Display this department's conversation
    for message in chats[department_key]:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and message.get("response"):
                render_response(message["response"])
            else:
                st.markdown(message["content"])

    with st.form(
        key=f"chat_form_{department_key}",
        clear_on_submit=True,
    ):
        query = st.text_area(
            "Your message",
            placeholder=f"Ask the {label} assistant...",
            height=100,
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "Send message",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    if not query or not query.strip():
        st.warning("Please enter a message before submitting.")
        return

    query = query.strip()

    chats[department_key].append({
        "role": "user",
        "content": query,
    })

    try:
        orchestrator = get_orchestrator()

        prior_messages = chats[department_key][:-1]

        context = AgentContext(
            department=department,
            session_id="streamlit-demo",
            user_role="employee",
            metadata={
                "conversation_history": [
                    {
                        "role": message["role"],
                        "content": message["content"],
                    }
                    for message in prior_messages
                    if message.get("role") in {"user", "assistant"}
                    and isinstance(message.get("content"), str)
                ]
            },
        )

        with st.spinner(f"Consulting {label}..."):
            response = orchestrator.run(
                query=query,
                context=context,
            )

        chats[department_key].append({
            "role": "assistant",
            "content": response.answer,
            "response": response,
        })

        st.session_state.history.insert(
            0,
            {
                "department": label,
                "query": query,
                "response": response,
            },
        )

        st.rerun()

    except Exception:
        st.error(
            "The workspace could not process this request. "
            "Check your local configuration and terminal logs."
        )

def render_history():
    """Render query history stored for this browser session."""
    st.subheader("Recent requests")

    if not st.session_state.history:
        st.caption("Your submitted requests will appear here.")
        return

    for index, item in enumerate(st.session_state.history):
        with st.expander(
            f"{item['department']} — {item['query'][:70]}",
            expanded=(index == 0),
        ):
            st.markdown(f"**Request:** {item['query']}")
            render_response(item["response"])


def main():
    inject_custom_css()
    if "selected_department" not in st.session_state:
        st.session_state.selected_department = None

    if "history" not in st.session_state:
        st.session_state.history = []

    with st.sidebar:
        st.title("🏢 Restructura One")
        st.caption("Enterprise AI Workspace")
        st.divider()

        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.selected_department = None
            st.rerun()

        st.markdown("**Departments**")

        for index, (label, _, emoji, _) in enumerate(DEPARTMENTS):
            if st.button(
                f"{emoji}  {label}",
                key=f"nav_{index}",
                use_container_width=True,
            ):
                st.session_state.selected_department = label
                st.rerun()

        st.divider()
        st.caption("Academic prototype")
        st.caption("Synthetic knowledge bases only")

    if st.session_state.selected_department is None:
        render_dashboard()
    else:
        render_department_workspace(
            st.session_state.selected_department
        )

    st.divider()
    render_history()


if __name__ == "__main__":
    main()
