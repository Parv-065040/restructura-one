
from types import SimpleNamespace
from unittest.mock import Mock

from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
)
from agents.sales.agent import SalesAgent


def make_context(department=Department.SALES):
    return AgentContext(department=department)


def make_chunk(score=0.85):
    return SimpleNamespace(
        source_id="sales_doc_001",
        document_name="sales_performance.md",
        excerpt="Q2 sales target was INR 15 million.",
        chunk_id="chunk_0",
        relevance_score=score,
    )


def make_agent(chunks=None, answer="Sales answer"):
    retriever = Mock()
    retriever.search.return_value = chunks or []

    gateway = Mock()
    gateway.generate.return_value = answer

    agent = SalesAgent(retriever=retriever, gateway=gateway)
    return agent, retriever, gateway


def test_sales_agent_returns_grounded_answer_and_source():
    chunk = make_chunk()
    agent, retriever, gateway = make_agent([chunk])

    response = agent.run("What was the sales target?", make_context())

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.SALES
    assert response.answer == "Sales answer"
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "sales_performance.md"
    assert response.actions == []

    retriever.search.assert_called_once_with(
        "What was the sales target?", top_k=4
    )
    gateway.generate.assert_called_once()


def test_sales_agent_returns_insufficient_evidence():
    agent, _, gateway = make_agent([make_chunk(score=0.10)])

    response = agent.run("Unrelated question", make_context())

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.sources == []
    assert response.actions == []
    gateway.generate.assert_not_called()


def test_sales_agent_rejects_wrong_department():
    agent, retriever, gateway = make_agent([make_chunk()])

    response = agent.run(
        "What was the sales target?",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR
    assert response.department == Department.SALES
    retriever.search.assert_not_called()
    gateway.generate.assert_not_called()


def test_sales_agent_handles_blank_query():
    agent, retriever, gateway = make_agent()

    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
    retriever.search.assert_not_called()
    gateway.generate.assert_not_called()


def test_sales_agent_handles_gateway_failure():
    agent, _, gateway = make_agent([make_chunk()])
    gateway.generate.side_effect = RuntimeError("Simulated failure")

    response = agent.run("Summarize sales", make_context())

    assert response.status == AgentStatus.ERROR
    assert "internal error" in response.answer.lower()
    assert response.actions == []