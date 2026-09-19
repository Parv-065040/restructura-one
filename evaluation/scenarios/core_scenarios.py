"""Synthetic baseline scenarios for core Restructura One agents."""

from evaluation.scenario import EvaluationScenario
from core.schemas.agent_contracts import AgentStatus, Department


CORE_SCENARIOS = [
    EvaluationScenario(
        scenario_id="risk-insufficient-evidence",
        description="Risk agent abstains when evidence is unavailable",
        department=Department.RISK_RESTRUCTURING,
        query="What is the undocumented restructuring policy?",
        expected_status=AgentStatus.INSUFFICIENT_EVIDENCE,
        max_sources=0,
        expected_action_count=0,
    ),
    EvaluationScenario(
        scenario_id="finance-insufficient-evidence",
        description="Finance agent abstains when evidence is unavailable",
        department=Department.FINANCE,
        query="What is the undocumented finance policy?",
        expected_status=AgentStatus.INSUFFICIENT_EVIDENCE,
        max_sources=0,
        expected_action_count=0,
    ),
    EvaluationScenario(
        scenario_id="sales-insufficient-evidence",
        description="Sales agent abstains when evidence is unavailable",
        department=Department.SALES,
        query="What is the undocumented sales policy?",
        expected_status=AgentStatus.INSUFFICIENT_EVIDENCE,
        max_sources=0,
        expected_action_count=0,
    ),
    EvaluationScenario(
        scenario_id="it-insufficient-evidence",
        description="IT agent abstains when evidence is unavailable",
        department=Department.IT,
        query="What is the undocumented IT policy?",
        expected_status=AgentStatus.INSUFFICIENT_EVIDENCE,
        max_sources=0,
        expected_action_count=0,
    ),
]
