"""Distinguish an explicit future lesson link from an accidental broken link."""

import json
from pathlib import Path

from scripts.check_links import check_local


def test_links_existing_or_explicitly_planned():
    failures, _ = check_local(allow_planned=True)
    assert failures == []


def test_link_checker_rejects_bad_anchor(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Start\n\n[broken](#absent)\n", encoding="utf-8")
    failures, _ = check_local(tmp_path)
    assert len(failures) == 1


def test_only_declared_future_links_can_be_deferred(tmp_path: Path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/course-plan.json").write_text(
        json.dumps({"planned_files": ["future.md"]}), encoding="utf-8"
    )
    (tmp_path / "README.md").write_text("[planned](future.md) [typo](missing.md)", encoding="utf-8")
    failures, deferred = check_local(tmp_path, allow_planned=True)
    assert deferred == 1
    assert len(failures) == 1
    strict, deferred = check_local(tmp_path)
    assert len(strict) == 2
    assert deferred == 0
