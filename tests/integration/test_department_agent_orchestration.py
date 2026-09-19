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
    ("department", "agent_class", "document_name", "source_id"),
    [
        (
            Department.FINANCE,
            FinanceAgent,
            "finance_policy.md",
            "finance_policy",
        ),
        (
            Department.SALES,
            SalesAgent,
            "sales_playbook.md",
            "sales_playbook",
        ),
        (
            Department.IT,
            ITAgent,
            "it_policy.md",
            "it_policy",
        ),
    ],
)
def test_department_agent_routes_through_orchestrator(
    department,
    agent_class,
    document_name,
    source_id,
):
    # Arrange: mock retrieval and LLM dependencies
    retriever = Mock()
    gateway = Mock()

    retriever.search.return_value = [
        Mock(
            relevance_score=0.91,
            document_name=document_name,
            chunk_id="chunk-1",
            source_id=source_id,
            excerpt="This synthetic document contains relevant guidance.",
        )
    ]

    gateway.generate.return_value = (
        "The response is grounded in the retrieved synthetic guidance."
    )

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
        query="What does the relevant guidance say?",
        context=context,
    )

    # Assert
    assert response.department == department
    assert response.status == AgentStatus.SUCCESS
    assert "grounded" in response.answer
    assert len(response.sources) >= 1
    assert response.actions == []

    retriever.search.assert_called_once()
    gateway.generate.assert_called_once()
