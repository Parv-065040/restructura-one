
from types import SimpleNamespace
from unittest.mock import Mock

from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
)
from agents.finance.agent import FinanceAgent


def make_context(department=Department.FINANCE):
    return AgentContext(department=department)


def make_chunk(score=0.85):
    return SimpleNamespace(
        source_id="finance-doc-1",
        document_name="quarterly_financials.md",
        excerpt="Revenue: INR 12,000,000. Operating Profit: INR 1,800,000.",
        chunk_id="chunk-1",
        relevance_score=score,
    )


def make_agent(chunks=None, answer="Revenue was INR 12,000,000."):
    retriever = Mock()
    retriever.search.return_value = chunks or []

    gateway = Mock()
    gateway.generate.return_value = answer

    agent = FinanceAgent(
        retriever=retriever,
        gateway=gateway,
    )
    return agent, retriever, gateway


def test_finance_agent_returns_grounded_answer_with_citation():
    chunk = make_chunk()
    agent, retriever, gateway = make_agent(chunks=[chunk])

    response = agent.run(
        "What was the revenue?",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.FINANCE
    assert response.answer == "Revenue was INR 12,000,000."
    assert len(response.sources) == 1
    assert response.sources[0].document_name == "quarterly_financials.md"
    assert response.actions == []
    retriever.search.assert_called_once_with("What was the revenue?", top_k=4)
    gateway.generate.assert_called_once()


def test_finance_agent_rejects_wrong_department():
    agent, retriever, gateway = make_agent(chunks=[make_chunk()])

    response = agent.run(
        "What was revenue?",
        make_context(Department.HR),
    )

    assert response.status == AgentStatus.ERROR
    assert response.department == Department.FINANCE
    retriever.search.assert_not_called()
    gateway.generate.assert_not_called()


def test_finance_agent_requests_clarification_for_blank_query():
    agent, retriever, gateway = make_agent()

    response = agent.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
    retriever.search.assert_not_called()
    gateway.generate.assert_not_called()


def test_finance_agent_abstains_when_no_relevant_evidence():
    agent, retriever, gateway = make_agent(chunks=[make_chunk(score=0.10)])

    response = agent.run("What is the tax liability?", make_context())

    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.sources == []
    gateway.generate.assert_not_called()


def test_finance_agent_handles_retriever_or_llm_error_safely():
    agent, retriever, gateway = make_agent(chunks=[make_chunk()])
    gateway.generate.side_effect = RuntimeError("Simulated provider failure")

    response = agent.run("What was revenue?", make_context())

    assert response.status == AgentStatus.ERROR
    assert "internal error" in response.answer.lower()
    assert response.actions == []