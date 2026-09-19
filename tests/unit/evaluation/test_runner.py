from unittest.mock import Mock

import pytest

from core.schemas.agent_contracts import (
    ActionProposal,
    AgentResponse,
    AgentStatus,
    Department,
    SourceCitation,
)
from evaluation.runner import EvaluationRunner
from evaluation.scenario import EvaluationScenario


@pytest.fixture
def orchestrator():
    return Mock()


def make_scenario(**overrides):
    values = {
        "scenario_id": "finance-grounded-001",
        "description": "Grounded finance response",
        "department": Department.FINANCE,
        "query": "What does the policy say?",
        "expected_status": AgentStatus.SUCCESS,
        "min_sources": 1,
        "require_source_ids": True,
    }
    values.update(overrides)
    return EvaluationScenario(**values)


def make_response(**overrides):
    values = {
        "department": Department.FINANCE,
        "answer": "The policy provides this guidance.",
        "status": AgentStatus.SUCCESS,
        "sources": [
            SourceCitation(
                source_id="finance_policy",
                document_name="finance_policy.md",
            )
        ],
        "actions": [],
    }
    values.update(overrides)
    return AgentResponse(**values)


def test_runner_passes_when_response_meets_expectations(orchestrator):
    scenario = make_scenario()
    orchestrator.run.return_value = make_response()

    result = EvaluationRunner(orchestrator).run_scenario(scenario)

    assert result.passed is True
    assert result.messages == ()
    assert all(result.checks.values())
    orchestrator.run.assert_called_once()


def test_runner_fails_when_status_does_not_match(orchestrator):
    scenario = make_scenario()
    orchestrator.run.return_value = make_response(
        status=AgentStatus.INSUFFICIENT_EVIDENCE,
        sources=[],
    )

    result = EvaluationRunner(orchestrator).run_scenario(scenario)

    assert result.passed is False
    assert "status_matches" in result.messages
    assert "min_sources_met" in result.messages


def test_runner_checks_expected_action_count(orchestrator):
    scenario = make_scenario(expected_action_count=1)
    orchestrator.run.return_value = make_response()

    result = EvaluationRunner(orchestrator).run_scenario(scenario)

    assert result.passed is False
    assert "action_count_matches" in result.messages


def test_runner_rejects_action_without_required_approval(orchestrator):
    scenario = make_scenario(expected_action_count=1)
    action = ActionProposal(
        action_id="action-001",
        action_type="create_report",
        description="Create a synthetic report",
        requires_approval=False,
    )
    orchestrator.run.return_value = make_response(actions=[action])

    result = EvaluationRunner(orchestrator).run_scenario(scenario)

    assert result.passed is False
    assert "actions_require_approval" in result.messages


def test_runner_can_evaluate_multiple_scenarios(orchestrator):
    scenarios = [
        make_scenario(scenario_id="scenario-1"),
        make_scenario(scenario_id="scenario-2"),
    ]
    orchestrator.run.return_value = make_response()

    results = EvaluationRunner(orchestrator).run(scenarios)

    assert len(results) == 2
    assert all(result.passed for result in results)
    assert orchestrator.run.call_count == 2
