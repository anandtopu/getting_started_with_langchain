"""Use a synthetic offline search corpus; make Tavily an explicit opt-in.

Run: uv run --extra agents python modules/17_deep_agents/examples/05_search_sources.py --offline
Expected: Retrieved source paths and synthetic labels; no default web call.
Cost: No model calls. --web uses one Tavily search and may consume search credits. Offline
fixtures incur no API fee.
Requires: agents
"""

import argparse

from common.config import get_settings
from common.errors import run_cli
from common.pretty import print_text
from common.research import research_sources


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument(
        "--web",
        action="store_true",
        help="Opt in to one Tavily search; requires search extra and key",
    )
    args = parser.parse_args()
    settings = get_settings()
    if args.offline:
        settings = settings.model_copy(update={"course_offline": True})
    # KEY IDEA: absence of --web selects local evidence even with a live model profile.
    docs = research_sources("repairable gear tent setup trends", settings, web=args.web)
    for doc in docs:
        print_text(
            str(
                {
                    "source": doc.metadata["source"],
                    "synthetic": doc.metadata["synthetic"],
                    "text": doc.page_content,
                }
            )
        )


if __name__ == "__main__":
    run_cli(main)
