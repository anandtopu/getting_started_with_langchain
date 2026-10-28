"""Do not equate a passing phase check with a complete course."""

import json

from common.config import ROOT
from scripts.check_coverage import check


def test_phase_coverage():
    progress = json.loads((ROOT / "docs/progress.json").read_text(encoding="utf-8"))
    plan = json.loads((ROOT / "docs/course-plan.json").read_text(encoding="utf-8"))
    failures, deferred = check()
    assert failures == []
    assert deferred == len(plan["modules"]) - len(progress["implemented_modules"])
    if deferred:
        final_failures, _ = check(require_complete=True)
        assert final_failures
