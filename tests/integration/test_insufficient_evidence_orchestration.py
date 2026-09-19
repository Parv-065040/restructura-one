from unittest.mock import Mock

import pytest

from agents.finance.agent import FinanceAgent
from agents.sales.agent import SalesAgent
from agents.it.agent import ITAgent
from core.agent_registry import AgentRegistry
from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
)


@pytest.mark.parametrize(
    ("department", "agent_class"),
    [
        (Department.FINANCE, FinanceAgent),
        (Department.SALES, SalesAgent),
        (Department.IT, ITAgent),
    ],
)
def test_orchestrator_preserves_insufficient_evidence_response(
    department,
    agent_class,
):
    # Arrange: retrieval returns no relevant evidence
    retriever = Mock()
    gateway = Mock()
    retriever.search.return_value = []

    agent = agent_class(
        retriever=retriever,
        gateway=gateway,
    )

    registry = AgentRegistry()
    registry.register(department, agent)
    orchestrator = AgentOrchestrator(registry)

    context = AgentContext(department=department)

    # Act
    response = orchestrator.run(
        query="Provide guidance not present in the knowledge base.",
        context=context,
    )

    # Assert: abstention is preserved and no LLM call occurs
    assert response.department == department
    assert response.status == AgentStatus.INSUFFICIENT_EVIDENCE
    assert response.answer
    assert response.sources == []
    assert response.actions == []

    retriever.search.assert_called_once()
    gateway.generate.assert_not_called()
