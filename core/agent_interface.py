"""Shared interface implemented by all Restructura One agents."""

from typing import Protocol

from core.schemas.agent_contracts import AgentContext, AgentResponse


class AgentRunner(Protocol):
    """Contract that every departmental agent must implement."""

    def run(self, query: str, context: AgentContext) -> AgentResponse:
        """Process a user query and return a standardized response."""
        ...
