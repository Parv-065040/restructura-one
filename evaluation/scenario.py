"""Data models for deterministic agent evaluation scenarios."""

from pydantic import BaseModel, ConfigDict, Field

from core.schemas.agent_contracts import AgentStatus, Department


class EvaluationScenario(BaseModel):
    """Defines an expected outcome for one agent evaluation."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    department: Department
    query: str = Field(min_length=1)
    expected_status: AgentStatus

    min_sources: int = Field(default=0, ge=0)
    max_sources: int | None = Field(default=None, ge=0)

    expected_action_count: int | None = Field(default=None, ge=0)
    require_source_ids: bool = False
    expected_source_ids: list[str] | None = None
    require_approval_for_actions: bool = True
