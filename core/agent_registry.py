"""Registry for Restructura One departmental agents."""

from core.agent_interface import AgentRunner
from core.schemas.agent_contracts import Department


class AgentRegistry:
    """Register and retrieve agents by department."""

    def __init__(self) -> None:
        self._agents: dict[Department, AgentRunner] = {}

    def register(
        self,
        department: Department,
        agent: AgentRunner,
    ) -> None:
        """Register an agent for a department."""
        if department in self._agents:
            raise ValueError(
                f"An agent is already registered for: {department.value}"
            )

        self._agents[department] = agent

    def get(self, department: Department) -> AgentRunner:
        """Return the registered agent for a department."""
        try:
            return self._agents[department]
        except KeyError as exc:
            raise LookupError(
                f"No agent registered for: {department.value}"
            ) from exc

    def is_registered(self, department: Department) -> bool:
        """Check whether a department has a registered agent."""
        return department in self._agents

    def registered_departments(self) -> list[Department]:
        """Return the departments that currently have registered agents."""
        return list(self._agents.keys())
