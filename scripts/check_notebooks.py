"""Execute committed notebooks without modifying their cleared source outputs.

Run: uv run --extra deep --extra deployment --group authoring python scripts/check_notebooks.py
Expected: each implemented notebook executes with explicit offline fixtures.
Cost: no model calls; requires the optional authoring environment.
"""

import json
import os
import subprocess
import sys

from common.config import ROOT
from common.pretty import print_text, redact


def main() -> None:
    output = ROOT / ".runtime/notebooks"
    output.mkdir(parents=True, exist_ok=True)
    kernel = output / "jupyter/kernels/brightwave-course"
    kernel.mkdir(parents=True, exist_ok=True)
    (kernel / "kernel.json").write_text(
        json.dumps(
            {
                "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                "display_name": "Brightwave course environment",
                "language": "python",
            }
        ),
        encoding="utf-8",
    )
    environment = {
        **os.environ,
        "COURSE_OFFLINE": "true",
        "LANGSMITH_TRACING": "false",
        "JUPYTER_PATH": str(output / "jupyter") + os.pathsep + os.environ.get("JUPYTER_PATH", ""),
    }
    notebooks = sorted((ROOT / "modules").glob("*/notebook.ipynb"))
    failures = []
    for notebook in notebooks:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--ExecutePreprocessor.timeout=120",
                "--ExecutePreprocessor.kernel_name=brightwave-course",
                "--output",
                notebook.parent.name,
                "--output-dir",
                str(output),
                str(notebook),
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=360,
        )
        if result.returncode:
            failures.append(notebook.parent.name)
            print_text(redact(result.stderr[-5000:]))
        print_text(f"{'FAIL' if result.returncode else 'PASS'}: {notebook.parent.name}")
    print_text(f"Notebooks: {len(notebooks) - len(failures)}/{len(notebooks)} passed.")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
