"""Evaluation sets are independent, nonempty, uniquely identified and explicitly scoped."""

import json

from common.config import ROOT


def test_all_capstone_case_identifiers_are_unique():
    paths = sorted((ROOT / "capstones").glob("*/eval.jsonl"))
    assert len(paths) == 5
    for path in paths:
        cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        assert len(cases) >= 3
        assert len({case["id"] for case in cases}) == len(cases)


def test_reference_labels_are_not_in_pdf_or_policy_indexes():
    from common.knowledge import policy_documents

    docs = policy_documents(handbook=False)
    assert all("eval" not in doc.metadata["source"] for doc in docs)
