"""Compare baseline and candidate retrieval without inventing a quality gain.

Run: uv run --extra rag python modules/09_advanced_rag/use_case/rag_benchmark.py --offline
Expected: A saved before/after report; identical hit rates are reported honestly.
Cost: Offline no API calls. Live: up to 16 generations plus embeddings, budget $0.10.
Requires: rag
"""

from common.config import ROOT
from common.errors import run_cli
from common.evaluation import benchmark, save_report
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    settings = lesson_settings()
    report = benchmark(settings)
    output = ROOT / settings.runtime_dir / "rag_benchmark.json"
    save_report(report, output)
    for name, metrics in report["systems"].items():
        print_text(
            str({"system": name, **{key: value for key, value in metrics.items() if key != "rows"}})
        )
    print_text(str(output))
    print_text(report["limits"])


if __name__ == "__main__":
    run_cli(main)
