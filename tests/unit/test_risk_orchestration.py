from unittest.mock import Mock

from agents.risk_restructuring.agent import RiskRestructuringAgent
from core.agent_registry import AgentRegistry
from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import (
    AgentContext,
    AgentStatus,
    Department,
    SourceCitation,
)


def test_risk_agent_routes_through_orchestrator():
    # Arrange: mock external dependencies
    retriever = Mock()
    gateway = Mock()

    retriever.search.return_value = [
        Mock(
            relevance_score=0.91,
            document_name="risk_policy.md",
            chunk_id="chunk-1",
            source_id="risk_policy",
            excerpt="Restructuring cases require documented review.",
        )
    ]

    gateway.generate.return_value = (
        "The policy requires documented review."
    )

    risk_agent = RiskRestructuringAgent(
        retriever=retriever,
        gateway=gateway,
    )

    registry = AgentRegistry()
    registry.register(
        Department.RISK_RESTRUCTURING,
        risk_agent,
    )

    orchestrator = AgentOrchestrator(registry)

    context = AgentContext(
        department=Department.RISK_RESTRUCTURING,
    )

    # Act
    response = orchestrator.run(
        query="What does the policy require?",
        context=context,
    )

    # Assert
    assert response.department == Department.RISK_RESTRUCTURING
    assert response.status == AgentStatus.SUCCESS
    assert "documented review" in response.answer
    assert len(response.sources) == 1
    assert isinstance(response.sources[0], SourceCitation)

    retriever.search.assert_called_once()
    gateway.generate.assert_called_once()
