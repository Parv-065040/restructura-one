import pytest

from core.agent_registry import AgentRegistry
from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import (
    AgentContext,
    AgentResponse,
    AgentStatus,
    Department,
)


class DummyAgent:
    def run(self, query: str, context: AgentContext) -> AgentResponse:
        return AgentResponse(
            department=context.department,
            answer=f"Processed: {query}",
        )


class ExplodingAgent:
    def run(self, query: str, context: AgentContext) -> AgentResponse:
        raise RuntimeError("Simulated internal failure")


class MismatchedAgent:
    def run(self, query: str, context: AgentContext) -> AgentResponse:
        return AgentResponse(
            department=Department.FINANCE,
            answer="Incorrect department response",
        )


def make_context(
    department: Department = Department.RISK_RESTRUCTURING,
) -> AgentContext:
    return AgentContext(department=department)


def make_orchestrator(agent, department=Department.RISK_RESTRUCTURING):
    registry = AgentRegistry()
    registry.register(department, agent)
    return AgentOrchestrator(registry)


def test_successful_routing_returns_agent_response():
    orchestrator = make_orchestrator(DummyAgent())

    response = orchestrator.run(
        "Summarize risk policy",
        make_context(),
    )

    assert response.status == AgentStatus.SUCCESS
    assert response.department == Department.RISK_RESTRUCTURING
    assert response.answer == "Processed: Summarize risk policy"


def test_empty_query_returns_needs_clarification():
    orchestrator = make_orchestrator(DummyAgent())

    response = orchestrator.run("   ", make_context())

    assert response.status == AgentStatus.NEEDS_CLARIFICATION
    assert response.answer == "Please enter a question."


def test_unregistered_department_returns_error():
    orchestrator = AgentOrchestrator(AgentRegistry())

    response = orchestrator.run(
        "Review financial data",
        make_context(Department.FINANCE),
    )

    assert response.status == AgentStatus.ERROR
    assert "not available yet" in response.answer


def test_agent_exception_returns_safe_error():
    orchestrator = make_orchestrator(ExplodingAgent())

    response = orchestrator.run("Check risk", make_context())

    assert response.status == AgentStatus.ERROR
    assert "internal error" in response.answer
    assert "Simulated internal failure" not in response.answer


def test_department_mismatch_returns_error():
    orchestrator = make_orchestrator(MismatchedAgent())

    response = orchestrator.run("Check risk", make_context())

    assert response.status == AgentStatus.ERROR
    assert "invalid department response" in response.answer
