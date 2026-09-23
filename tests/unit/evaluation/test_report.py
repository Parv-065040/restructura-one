from evaluation.report import build_report, report_to_dict
from evaluation.runner import EvaluationResult


def test_build_report_counts_passed_and_failed_results():
    results = [
        EvaluationResult("case-1", True, {"status_matches": True}, ()),
        EvaluationResult("case-2", False, {"status_matches": False}, ("status_matches",)),
        EvaluationResult("case-3", True, {"status_matches": True}, ()),
    ]

    report = build_report(results)

    assert report.total == 3
    assert report.passed == 2
    assert report.failed == 1
    assert report.pass_rate == 66.67


def test_empty_results_produce_zero_pass_rate():
    report = build_report([])

    assert report.total == 0
    assert report.passed == 0
    assert report.failed == 0
    assert report.pass_rate == 0.0


def test_report_converts_to_json_compatible_dict():
    results = [
        EvaluationResult("case-1", False, {"source_ids_present": False}, ("source_ids_present",))
    ]

    payload = report_to_dict(build_report(results))

    assert payload["total"] == 1
    assert payload["results"][0]["scenario_id"] == "case-1"
    assert payload["results"][0]["messages"] == ["source_ids_present"]
