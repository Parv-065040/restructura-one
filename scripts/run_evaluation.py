"""Run deterministic baseline evaluations for core agents."""

import json
from unittest.mock import Mock

from agents.finance.agent import FinanceAgent
from agents.it.agent import ITAgent
from agents.risk_restructuring.agent import RiskRestructuringAgent
from agents.sales.agent import SalesAgent
from core.agent_registry import AgentRegistry
from core.orchestrator import AgentOrchestrator
from core.schemas.agent_contracts import Department
from evaluation.report import build_report, report_to_dict
from evaluation.runner import EvaluationRunner
from evaluation.scenarios.core_scenarios import CORE_SCENARIOS


def build_orchestrator() -> AgentOrchestrator:
    """Register agents with empty retrieval results for abstention tests."""
    registry = AgentRegistry()

    agents = {
        Department.RISK_RESTRUCTURING: RiskRestructuringAgent,
        Department.FINANCE: FinanceAgent,
        Department.SALES: SalesAgent,
        Department.IT: ITAgent,
    }

    for department, agent_class in agents.items():
        retriever = Mock()
        retriever.search.return_value = []
        gateway = Mock()

        registry.register(
            department,
            agent_class(retriever=retriever, gateway=gateway),
        )

    return AgentOrchestrator(registry)


def main() -> None:
    orchestrator = build_orchestrator()
    runner = EvaluationRunner(orchestrator)

    results = runner.run(CORE_SCENARIOS)
    report = report_to_dict(build_report(results))

    print(json.dumps(report, indent=2))

    if report["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
