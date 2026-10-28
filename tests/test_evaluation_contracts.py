"""Held-out labels stay outside the target; failures must trip the release gate."""

import copy

import pytest

pytest.importorskip("rank_bm25")
pytest.importorskip("pypdf")

from common.config import Settings
from common.experiments import run_experiment
from common.release import evaluation_gate
from common.support_evaluation import load_cases, local_evaluate, score_answer


def test_all_support_answers_pass_the_unchanged_release_contracts():
    report = local_evaluate(load_cases(), Settings(course_offline=True))
    assert (report["passed"], report["total"]) == (6, 6)
    assert evaluation_gate(report)
    assert all(row["metrics"]["trajectory_exact"] for row in report["rows"])
    assert all(row["metrics"]["ownership_contract"] for row in report["rows"])


def test_changed_labels_do_not_change_answers():
    cases = load_cases()
    changed = copy.deepcopy(cases)
    for case in changed:
        case["must_contain"] = ["impossible-answer-key-marker"]
    first = local_evaluate(cases, Settings(course_offline=True))
    second = local_evaluate(changed, Settings(course_offline=True))
    assert [row["answer"] for row in first["rows"]] == [row["answer"] for row in second["rows"]]
    assert first["passed"] == 6 and second["passed"] == 0


@pytest.mark.parametrize("identifier", ["returns", "shipping"])
def test_missing_policy_fact_still_blocks_release(identifier):
    cases = load_cases()
    report = local_evaluate(cases, Settings(course_offline=True))
    row = next(row for row in report["rows"] if row["id"] == identifier)
    case = next(case for case in cases if case["id"] == identifier)
    row["answer"]["answer"] = "Please review the policy."
    row["metrics"] = score_answer(case, row["answer"])
    assert not row["metrics"]["keyword_correctness_proxy"]
    assert not evaluation_gate(report)


def test_real_langsmith_local_runner_needs_no_network():
    results = run_experiment(load_cases()[:2], Settings(course_offline=True))
    assert len(results) == 2
    assert all(row["scores"] == [True] for row in results)


def test_empty_report_and_unsafe_case_cannot_pass():
    with pytest.raises(ValueError):
        local_evaluate([], Settings(course_offline=True))
    assert not evaluation_gate({"rows": []})
    report = local_evaluate(load_cases()[:1], Settings(course_offline=True))
    assert evaluation_gate(report)
    report["rows"][0]["metrics"]["ownership_contract"] = False
    assert not evaluation_gate(report, minimum_correctness=0)


@pytest.mark.parametrize("metric", ["tone_rule_proxy", "exact_evidence_support_proxy"])
def test_grounding_and_tone_are_release_requirements(metric):
    report = local_evaluate(load_cases()[:1], Settings(course_offline=True))
    assert evaluation_gate(report)
    report["rows"][0]["metrics"][metric] = False
    assert not evaluation_gate(report)
