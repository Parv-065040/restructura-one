import pytest

from core.agent_registry import AgentRegistry
from core.schemas.agent_contracts import (
    AgentContext,
    AgentResponse,
    Department,
)


class DummyAgent:
    """Lightweight agent for registry tests."""

    def run(self, query: str, context: AgentContext) -> AgentResponse:
        return AgentResponse(
            department=context.department,
            answer="Test response",
        )


def test_register_and_get_agent():
    registry = AgentRegistry()
    agent = DummyAgent()

    registry.register(Department.RISK_RESTRUCTURING, agent)

    assert registry.get(Department.RISK_RESTRUCTURING) is agent


def test_is_registered_returns_correct_status():
    registry = AgentRegistry()

    assert not registry.is_registered(Department.FINANCE)

    registry.register(Department.FINANCE, DummyAgent())

    assert registry.is_registered(Department.FINANCE)


def test_registered_departments_returns_registered_agents():
    registry = AgentRegistry()
    registry.register(Department.FINANCE, DummyAgent())
    registry.register(Department.SALES, DummyAgent())

    assert set(registry.registered_departments()) == {
        Department.FINANCE,
        Department.SALES,
    }


def test_duplicate_registration_raises_value_error():
    registry = AgentRegistry()
    registry.register(Department.FINANCE, DummyAgent())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(Department.FINANCE, DummyAgent())


def test_get_unregistered_agent_raises_lookup_error():
    registry = AgentRegistry()

    with pytest.raises(LookupError, match="No agent registered"):
        registry.get(Department.IT)
