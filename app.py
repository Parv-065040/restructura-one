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
    """Render the departmental landing page."""
    st.title("Restructura One")
    st.caption("Enterprise AI Workspace | Departmental Intelligence")

    st.info(
        "AI-generated outputs are decision support, not autonomous approvals. "
        "Review consequential recommendations before acting."
    )

    st.subheader("Your AI workspace")
    st.write(
        "Choose a department to work with its specialized assistant, "
        "grounded in its department-specific synthetic knowledge base."
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
    """Render the query and response workspace for one department."""
    department = DEPARTMENT_LOOKUP[label]

    st.title(label)
    st.caption("Department Assistant")

    st.info(
        "Responses are decision support. Verify evidence and review "
        "consequential recommendations before acting."
    )

    st.write(
        "Enter a business question or task. The assistant will respond "
        "using its department-specific knowledge base."
    )

    with st.form(f"agent_query_form_{label}", clear_on_submit=False):
        query = st.text_area(
            "Your request",
            placeholder="Describe the business question or task...",
            height=130,
        )

        submitted = st.form_submit_button(
            "Submit request",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not query or not query.strip():
            st.warning("Please enter a request before submitting.")
            return

        try:
            orchestrator = get_orchestrator()

            context = AgentContext(
                department=department,
                session_id="streamlit-demo",
                user_role="employee",
            )

            with st.spinner(f"Consulting {label}..."):
                response = orchestrator.run(
                    query=query.strip(),
                    context=context,
                )

            st.session_state.history.insert(
                0,
                {
                    "department": label,
                    "query": query.strip(),
                    "response": response,
                },
            )

            st.divider()
            st.subheader("Assistant Response")
            render_response(response)

        except Exception:
            st.error(
                "The workspace could not initialize or process this request. "
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
