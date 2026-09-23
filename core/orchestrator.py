"""Central request orchestrator for Restructura One."""

import logging

from core.agent_registry import AgentRegistry
from core.agent_interface import AgentRunner
from core.schemas.agent_contracts import (
    AgentContext,
    AgentResponse,
    AgentStatus,
    Department,
)

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Routes requests to registered departmental agents."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def run(
        self,
        query: str,
        context: AgentContext,
    ) -> AgentResponse:
        """Validate and route a request to its departmental agent."""

        if not query or not query.strip():
            return AgentResponse(
                department=context.department,
                answer="Please enter a question.",
                status=AgentStatus.NEEDS_CLARIFICATION,
            )

        try:
            agent: AgentRunner = self.registry.get(context.department)
        except LookupError:
            logger.warning(
                "No agent registered for department: %s",
                context.department.value,
            )
            return AgentResponse(
                department=context.department,
                answer=(
                    f"The {context.department.value} assistant "
                    "is not available yet."
                ),
                status=AgentStatus.ERROR,
            )

        try:
            response = agent.run(query=query, context=context)
        except Exception:
            logger.exception(
                "Agent execution failed for department: %s",
                context.department.value,
            )
            return AgentResponse(
                department=context.department,
                answer=(
                    "The assistant encountered an internal error. "
                    "Please try again later. No action was executed."
                ),
                status=AgentStatus.ERROR,
            )

        if response.department != context.department:
            logger.error(
                "Agent response department mismatch. Requested: %s",
                context.department.value,
            )
            return AgentResponse(
                department=context.department,
                answer="The assistant returned an invalid department response.",
                status=AgentStatus.ERROR,
            )

        return response
