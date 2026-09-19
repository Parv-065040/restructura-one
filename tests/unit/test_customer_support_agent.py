from types import SimpleNamespace

from agents.customer_support.agent import CustomerSupportAgent
from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
)


class FakeRetriever:
    def __init__(self, chunks):
        self.chunks = chunks

    def search(self, query, top_k=4):
        return self.chunks


class FakeGateway:
    def generate(self, prompt, system_prompt):
        return (
            "Ticket category: Account Access.\n"
            "Response draft: Please contact the approved support channel "
            "and provide the required account information for verification."
        )


def make_chunk(score=0.8):
    return SimpleNamespace(
        source_id="CS-001",
        document_name="faqs.md",
        excerpt="Customers should contact the approved support channel.",
        chunk_id="chunk-1",
        relevance_score=score,
    )


def make_context():
    return AgentContext(
        department=Department.CUSTOMER_SUPPORT,
        session_id="test-session",
    )


def test_customer_support_grounded_response_and_source():
    agent = CustomerSupportAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "Customer cannot access their account. Draft a response.",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert "Ticket category" in response.answer
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "faqs.md"


def test_customer_support_weak_evidence():
    agent = CustomerSupportAgent(
        retriever=FakeRetriever([make_chunk(score=0.1)]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "How should this customer issue be handled?",
        make_context(),
    )

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE


def test_customer_support_wrong_department():
    agent = CustomerSupportAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    context = AgentContext(
        department=Department.HR,
        session_id="test-session",
    )

    response = agent.run(
        "Customer cannot access their account.",
        context,
    )

    assert response.status == AgentStatus.ERROR


def test_customer_support_empty_query():
    agent = CustomerSupportAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run("", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
