"""Check the inventory honestly: completed modules must be complete; future work is reported."""

import argparse
import json
from pathlib import Path

from common.config import ROOT

SECTIONS = [
    "Prerequisites",
    "Learning objectives",
    "The big idea",
    "How it works",
    "Key APIs at a glance",
    "Walkthrough",
    "Real-world use case",
    "Common mistakes",
    "Exercises",
    "Quiz",
    "Key takeaways",
    "Go deeper",
    "Next:",
]


def check(root: Path = ROOT, *, require_complete: bool = False) -> tuple[list[str], int]:
    plan = json.loads((root / "docs/course-plan.json").read_text(encoding="utf-8"))
    progress = json.loads((root / "docs/progress.json").read_text(encoding="utf-8"))
    completed = set(progress["implemented_modules"])
    known = {m["slug"] for m in plan["modules"]}
    failures = [f"Unknown completed module: {name}" for name in completed - known]
    present = {p.name for p in (root / "modules").glob("*") if p.is_dir()}
    failures.extend(f"Unregistered module directory: {name}" for name in present - completed)
    for module in plan["modules"]:
        if module["slug"] not in completed:
            continue
        prefix = f"modules/{module['slug']}/"
        failures.extend(
            f"Missing implemented file: {name}"
            for name in plan["planned_files"]
            if name.startswith(prefix) and not (root / name).is_file()
        )
        readme = root / prefix / "README.md"
        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            failures.extend(
                f"{prefix}: missing README section {section}"
                for section in SECTIONS
                if f"## {section}" not in text
            )
            for required in ["```mermaid", "Assistant version", "**Cost:", "<details>"]:
                if required not in text:
                    failures.append(f"{prefix}: missing {required}")
        notebook = root / prefix / "notebook.ipynb"
        if notebook.exists():
            for cell in json.loads(notebook.read_text(encoding="utf-8"))["cells"]:
                if cell.get("outputs") or cell.get("execution_count") is not None:
                    failures.append(f"{prefix}: notebook outputs are not cleared")
    deferred = len(known - completed)
    if require_complete:
        failures.extend(f"Incomplete planned module: {slug}" for slug in sorted(known - completed))
        failures.extend(
            f"Missing final inventory file: {name}"
            for name in plan["planned_files"]
            if not (root / name).is_file()
        )
    return failures, deferred


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Final release gate; fails during phased construction.",
    )
    args = parser.parse_args()
    failures, deferred = check(require_complete=args.require_complete)
    for failure in failures:
        print(failure)
    print(
        f"Coverage: {len(failures)} violation(s); {deferred} future module(s) not yet implemented."
    )
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
