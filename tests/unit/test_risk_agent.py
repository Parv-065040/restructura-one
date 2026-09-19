from types import SimpleNamespace

from agents.risk_restructuring.agent import RiskRestructuringAgent
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
    def generate(self, system_prompt, user_prompt, **kwargs):
        return "The guide lists tenure extension as an option for human review."


def make_chunk(score=0.8):
    return SimpleNamespace(
        source_id="restructuring_options_guide",
        document_name="restructuring_options_guide.md",
        excerpt="Tenure extension may reduce periodic payment burden.",
        chunk_id="chunk-1",
        relevance_score=score,
    )


def make_context(department=Department.RISK_RESTRUCTURING):
    return AgentContext(department=department)


def test_risk_agent_returns_grounded_response_with_source():
    agent = RiskRestructuringAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What is a tenure extension?",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.RISK_RESTRUCTURING
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "restructuring_options_guide.md"


def test_risk_agent_abstains_when_evidence_is_weak():
    agent = RiskRestructuringAgent(
        retriever=FakeRetriever([make_chunk(score=0.1)]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What is the current market interest rate?",
        make_context(),
    )

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.sources == []


def test_risk_agent_rejects_wrong_department_context():
    agent = RiskRestructuringAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "Summarize this",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR


def test_risk_agent_requests_clarification_for_empty_query():
    agent = RiskRestructuringAgent(
        retriever=FakeRetriever([]),
        gateway=FakeGateway(),
    )

    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
