from types import SimpleNamespace

from agents.marketing.agent import MarketingAgent
from core.schemas.agent_contracts import AgentContext, AgentStatus, Department


class FakeRetriever:
    def __init__(self, chunks):
        self.chunks = chunks

    def search(self, query, top_k=4):
        return self.chunks


class FakeGateway:
    def generate(self, system_prompt, user_prompt, **kwargs):
        return (
            "The campaign should use a clear, professional, "
            "customer-focused tone and avoid unsupported claims."
        )


def make_chunk(score=0.8):
    return SimpleNamespace(
        source_id="brand_guidelines",
        document_name="brand_guidelines.md",
        excerpt=(
            "Restructura communications should be clear, professional, "
            "customer-focused, and practical."
        ),
        chunk_id="chunk-1",
        relevance_score=score,
    )


def make_context(department=Department.MARKETING):
    return AgentContext(department=department)


def test_marketing_agent_returns_grounded_response_with_source():
    agent = MarketingAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What tone should our marketing communication use?",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.MARKETING
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "brand_guidelines.md"


def test_marketing_agent_abstains_when_evidence_is_weak():
    agent = MarketingAgent(
        retriever=FakeRetriever([make_chunk(score=0.1)]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What was our campaign conversion rate?",
        make_context(),
    )

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.sources == []


def test_marketing_agent_rejects_wrong_department():
    agent = MarketingAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "Summarize the campaign guidelines.",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR
    assert response.department == Department.MARKETING


def test_marketing_agent_requests_clarification_for_empty_query():
    agent = MarketingAgent(
        retriever=FakeRetriever([]),
        gateway=FakeGateway(),
    )

    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
