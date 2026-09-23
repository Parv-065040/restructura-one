"""Aggregate evaluation results into a JSON-compatible report."""

from dataclasses import dataclass

from evaluation.runner import EvaluationResult


@dataclass(frozen=True)
class EvaluationReport:
    """Summary of a batch of evaluation results."""

    total: int
    passed: int
    failed: int
    pass_rate: float
    results: list[dict]


def build_report(
    results: list[EvaluationResult],
) -> EvaluationReport:
    """Build a summary report from evaluation results."""

    total = len(results)
    passed = sum(result.passed for result in results)
    failed = total - passed
    pass_rate = (passed / total * 100) if total else 0.0

    serialized_results = [
        {
            "scenario_id": result.scenario_id,
            "passed": result.passed,
            "checks": result.checks,
            "messages": list(result.messages),
        }
        for result in results
    ]

    return EvaluationReport(
        total=total,
        passed=passed,
        failed=failed,
        pass_rate=round(pass_rate, 2),
        results=serialized_results,
    )


def report_to_dict(report: EvaluationReport) -> dict:
    """Convert the report to a JSON-compatible dictionary."""

    return {
        "total": report.total,
        "passed": report.passed,
        "failed": report.failed,
        "pass_rate": report.pass_rate,
        "results": report.results,
    }
