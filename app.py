"""Streamlit entry point for Restructura One."""

import streamlit as st

from core.app_bootstrap import build_orchestrator
from core.schemas.agent_contracts import AgentContext, Department


st.set_page_config(
    page_title="Restructura One | AI Workspace",
    page_icon="🏢",
    layout="wide",
)

DEPARTMENT_LABELS = {
    "Risk & Restructuring": Department.RISK_RESTRUCTURING,
    "Finance": Department.FINANCE,
    "Sales": Department.SALES,
    "IT": Department.IT,
    "Human Resources": Department.HR,
    "Marketing": Department.MARKETING,
    "Legal & Compliance": Department.LEGAL_COMPLIANCE,
    "Customer Support": Department.CUSTOMER_SUPPORT,
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
                    st.caption(
                        f"Relevance: {source.relevance_score:.2f}"
                    )
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
                    f"Approval required: {'Yes' if action.requires_approval else 'No'}"
                )


def main():
    st.title("Restructura One")
    st.caption("Enterprise AI Workspace | Departmental Intelligence")

    st.info(
        "AI-generated outputs are decision support, not autonomous approvals. "
        "Review consequential recommendations before acting."
    )

    with st.sidebar:
        st.header("Workspace")
        selected_label = st.selectbox(
            "Choose a department",
            options=list(DEPARTMENT_LABELS.keys()),
        )
        st.divider()
        st.caption("Restructura One")
        st.caption("Academic prototype • Synthetic knowledge bases")

    department = DEPARTMENT_LABELS[selected_label]

    st.subheader(f"{selected_label} Assistant")
    st.write(
        "Enter a business question or task. The selected assistant will "
        "respond using its department-specific knowledge base."
    )

    with st.form("agent_query_form", clear_on_submit=False):
        query = st.text_area(
            "Your request",
            placeholder="Describe the business question or task...",
            height=140,
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

            with st.spinner(f"Consulting {selected_label}..."):
                response = orchestrator.run(
                    query=query.strip(),
                    context=context,
                )

            st.divider()
            st.subheader("Assistant Response")
            render_response(response)

        except Exception:
            st.error(
                "The workspace could not initialize or process this request. "
                "Check your local configuration and terminal logs."
            )


if __name__ == "__main__":
    main()
