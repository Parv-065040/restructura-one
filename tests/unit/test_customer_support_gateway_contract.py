from unittest.mock import Mock

from agents.customer_support.agent import CustomerSupportAgent
from core.schemas.agent_contracts import AgentContext, AgentStatus, Department


def test_customer_support_uses_gateway_user_prompt_keyword():
    retriever = Mock()
    gateway = Mock()

    retriever.search.return_value = [
        Mock(
            relevance_score=0.9,
            document_name="faqs.md",
            chunk_id="faq-1",
            source_id="faqs",
            excerpt="Synthetic support guidance.",
        )
    ]
    gateway.generate.return_value = "Support draft for review."

    agent = CustomerSupportAgent(retriever=retriever, gateway=gateway)

    response = agent.run(
        "Draft a response",
        AgentContext(department=Department.CUSTOMER_SUPPORT),
    )

    assert response.status == AgentStatus.SUCCESS
    gateway.generate.assert_called_once()
    assert "user_prompt" in gateway.generate.call_args.kwargs
    assert "prompt" not in gateway.generate.call_args.kwargs
