from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agents.it.agent import ITAgent
from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
)


def make_context(department=Department.IT):
    return AgentContext(department=department)


def make_chunk(score=0.85):
    return SimpleNamespace(
        relevance_score=score,
        document_name="it_support_policies.md",
        chunk_id="it-001",
        source_id="it-policy-001",
        excerpt="Use the approved IT support channel for account issues.",
    )


@pytest.fixture
def agent():
    instance = ITAgent.__new__(ITAgent)
    instance.retriever = Mock()
    instance.gateway = Mock()
    instance.min_relevance = 0.25
    return instance


def test_success_returns_answer_and_sources(agent):
    agent.retriever.search.return_value = [make_chunk()]
    agent.gateway.generate.return_value = "Contact the approved IT channel."

    response = agent.run("How do I get IT support?", make_context())

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.IT
    assert response.answer == "Contact the approved IT channel."
    assert len(response.sources) == 1
    assert response.actions == []


def test_insufficient_evidence_does_not_call_llm(agent):
    agent.retriever.search.return_value = [make_chunk(score=0.1)]

    response = agent.run("What is the admin password?", make_context())

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    agent.gateway.generate.assert_not_called()
    assert response.actions == []


def test_wrong_department_is_rejected(agent):
    response = agent.run(
        "Help with my laptop",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR
    agent.retriever.search.assert_not_called()


def test_blank_query_requests_clarification(agent):
    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
    agent.retriever.search.assert_not_called()


def test_gateway_failure_returns_safe_error(agent):
    agent.retriever.search.return_value = [make_chunk()]
    agent.gateway.generate.side_effect = RuntimeError("mock failure")

    response = agent.run("How do I get IT support?", make_context())

    assert response.status == AgentStatus.ERROR
    assert response.actions == []
    assert "error" in response.answer.lower()
