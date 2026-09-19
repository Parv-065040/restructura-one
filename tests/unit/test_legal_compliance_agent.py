from types import SimpleNamespace

from agents.legal_compliance.agent import LegalComplianceAgent
from core.schemas.agent_contracts import AgentContext, AgentStatus, Department


class FakeRetriever:
    def __init__(self, chunks):
        self.chunks = chunks

    def search(self, query, top_k=4):
        return self.chunks


class FakeGateway:
    def generate(self, system_prompt, user_prompt, **kwargs):
        return (
            "The compliance policy requires employees to follow approved "
            "company procedures and escalate potential compliance concerns."
        )


def make_chunk(score=0.8):
    return SimpleNamespace(
        source_id="compliance_policies",
        document_name="compliance_policies.md",
        excerpt=(
            "Employees should follow applicable company policies and "
            "escalate potential compliance concerns through approved "
            "internal channels."
        ),
        chunk_id="chunk-1",
        relevance_score=score,
    )


def make_context(department=Department.LEGAL_COMPLIANCE):
    return AgentContext(department=department)


def test_legal_agent_returns_grounded_response_with_source():
    agent = LegalComplianceAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What should employees do with potential compliance concerns?",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.LEGAL_COMPLIANCE
    assert "not legal advice" in response.answer
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "compliance_policies.md"


def test_legal_agent_abstains_when_evidence_is_weak():
    agent = LegalComplianceAgent(
        retriever=FakeRetriever([make_chunk(score=0.1)]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What penalty applies to a regulatory violation?",
        make_context(),
    )

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.sources == []


def test_legal_agent_rejects_wrong_department_context():
    agent = LegalComplianceAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "Summarize this policy",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR


def test_legal_agent_requests_clarification_for_empty_query():
    agent = LegalComplianceAgent(
        retriever=FakeRetriever([]),
        gateway=FakeGateway(),
    )

    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
