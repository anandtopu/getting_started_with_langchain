"""Parse a local HTML fixture; fetch one allowlisted documentation URL only on opt-in.

Run: uv run --extra rag python modules/06_loaders_splitters/examples/04_web_loader.py --offline
Expected: Visible text from the local Brightwave HTML fixture; comments/scripts are excluded.
Cost: No model fee. --fetch-docs explicitly uses network; default is a local fixture.
Requires: rag
"""

import argparse

import httpx

from common.config import ConfigurationError, get_settings
from common.data import data_path
from common.errors import run_cli
from common.knowledge import html_document
from common.pretty import print_text


def main() -> None:
    # KEY IDEA: Fetching is explicit; visible-text extraction is not an injection defence.
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--fetch-docs", action="store_true")
    args = parser.parse_args()
    source = "fixtures/policy.html"
    html = data_path(source).read_text(encoding="utf-8")
    if args.fetch_docs:
        if args.offline or get_settings().course_offline:
            raise ConfigurationError("--fetch-docs requires a live invocation without --offline.")
        source = "https://docs.langchain.com/oss/python/integrations/document_loaders"
        # Fixed URL, no arbitrary user-provided URL or redirects to private services.
        response = httpx.get(source, timeout=15, follow_redirects=False)
        response.raise_for_status()
        html = response.text[:200_000]
    print_text(html_document(html, source).page_content[:600])


if __name__ == "__main__":
    run_cli(main)
