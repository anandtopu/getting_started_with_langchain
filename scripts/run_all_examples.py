"""Smoke-test implemented examples; fakes and network denial are the default.

Run: uv run python scripts/run_all_examples.py
Expected in Phase 2: first-call and environment smoke targets pass; 139 lessons deferred.
--live explicitly enables selected real providers and possible API cost.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from common.config import ROOT
from common.pretty import print_text, redact


def targets(root: Path, live: bool) -> list[tuple[Path, list[str]]]:
    arguments = [] if live else ["--offline"]
    result = [
        (root / "scripts/check_env.py", arguments),
        (root / "scripts/first_call.py", arguments),
    ]
    result.extend((path, []) for path in sorted((root / "modules").glob("*/examples/*.py")))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Real provider calls; may incur costs.")
    parser.add_argument("--timeout", type=int, default=90, help="Seconds allowed per script.")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    selected = targets(ROOT, args.live)
    runtime = ROOT / ".runtime"
    runtime.mkdir(exist_ok=True)
    failures = []
    with tempfile.TemporaryDirectory(prefix="smoke-", dir=runtime) as temporary:
        if not Path(temporary).resolve().is_relative_to(runtime.resolve()):
            raise ValueError("Smoke directory escaped .runtime/.")
        for index, (path, arguments) in enumerate(selected):
            environment = dict(os.environ)
            environment.update(
                COURSE_OFFLINE="false" if args.live else "true", LANGSMITH_TRACING="false"
            )
            environment["RUNTIME_DIR"] = str(Path(temporary) / str(index))
            command = [sys.executable, str(ROOT / "scripts/_smoke_worker.py")]
            if args.live:
                command.append("--live")
            command.extend([str(path), *arguments])
            try:
                completed = subprocess.run(
                    command,
                    cwd=ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=args.timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                failures.append(path)
                print_text(f"TIMEOUT: {path.relative_to(ROOT)}")
                continue
            if completed.returncode:
                failures.append(path)
                print_text(f"FAIL: {path.relative_to(ROOT)}")
                # Child exception text can include settings; redaction happens before output.
                print_text(redact(completed.stdout + completed.stderr))
            else:
                print_text(f"PASS: {path.relative_to(ROOT)}")
    plan = json.loads((ROOT / "docs/course-plan.json").read_text(encoding="utf-8"))
    expected = sum(len(module["examples"]) for module in plan["modules"])
    implemented = len(selected) - 2
    print_text(f"{len(selected) - len(failures)}/{len(selected)} implemented targets passed.")
    print_text(
        f"Course examples implemented: {implemented}/{expected}; remaining lessons are deferred."
    )
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
