from types import SimpleNamespace

from agents.hr.agent import HRAgent
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
        return "The HR policy provides 18 working days of annual leave per calendar year."


def make_chunk(score=0.8):
    return SimpleNamespace(
        source_id="leave_attendance_policy",
        document_name="leave_attendance_policy.md",
        excerpt="Employees may request 18 working days of annual leave per calendar year.",
        chunk_id="chunk-1",
        relevance_score=score,
    )


def make_context(department=Department.HR):
    return AgentContext(department=department)


def test_hr_agent_returns_grounded_response_with_source():
    agent = HRAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "How many annual leave days are available?",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.HR
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "leave_attendance_policy.md"


def test_hr_agent_abstains_when_evidence_is_weak():
    agent = HRAgent(
        retriever=FakeRetriever([make_chunk(score=0.1)]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "What is the employee's salary?",
        make_context(),
    )

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.sources == []


def test_hr_agent_rejects_wrong_department_context():
    agent = HRAgent(
        retriever=FakeRetriever([make_chunk()]),
        gateway=FakeGateway(),
    )

    response = agent.run(
        "Summarize this",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR


def test_hr_agent_requests_clarification_for_empty_query():
    agent = HRAgent(
        retriever=FakeRetriever([]),
        gateway=FakeGateway(),
    )

    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION