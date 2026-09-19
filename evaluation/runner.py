"""Run deterministic evaluation scenarios against the orchestrator."""

from dataclasses import dataclass

from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import AgentContext

from evaluation.scenario import EvaluationScenario


@dataclass(frozen=True)
class EvaluationResult:
    """Outcome of evaluating one scenario."""

    scenario_id: str
    passed: bool
    checks: dict[str, bool]
    messages: tuple[str, ...]


class EvaluationRunner:
    """Evaluate agent responses against declared expectations."""

    def __init__(self, orchestrator: AgentOrchestrator) -> None:
        self.orchestrator = orchestrator

    def run_scenario(
        self,
        scenario: EvaluationScenario,
    ) -> EvaluationResult:
        context = AgentContext(department=scenario.department)

        response = self.orchestrator.run(
            query=scenario.query,
            context=context,
        )

        cited_source_ids = {
            source.source_id for source in response.sources
        }

        expected_source_ids = scenario.expected_source_ids

        citation_integrity = (
            expected_source_ids is None
            or cited_source_ids.issubset(set(expected_source_ids))
        )

        checks: dict[str, bool] = {
            "department_matches": response.department == scenario.department,
            "status_matches": response.status == scenario.expected_status,
            "min_sources_met": len(response.sources) >= scenario.min_sources,
            "max_sources_met": (
                scenario.max_sources is None
                or len(response.sources) <= scenario.max_sources
            ),
            "action_count_matches": (
                scenario.expected_action_count is None
                or len(response.actions) == scenario.expected_action_count
            ),
            "source_ids_present": (
                not scenario.require_source_ids
                or all(source.source_id.strip() for source in response.sources)
            ),
            "actions_require_approval": (
                not scenario.require_approval_for_actions
                or all(action.requires_approval for action in response.actions)
            ),
            "citation_integrity": citation_integrity,
        }

        messages = tuple(
            name for name, passed in checks.items() if not passed
        )

        return EvaluationResult(
            scenario_id=scenario.scenario_id,
            passed=all(checks.values()),
            checks=checks,
            messages=messages,
        )

    def run(
        self,
        scenarios: list[EvaluationScenario],
    ) -> list[EvaluationResult]:
        """Run scenarios independently and return each result."""
        return [self.run_scenario(scenario) for scenario in scenarios]
