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
