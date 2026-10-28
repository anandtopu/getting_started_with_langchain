"""Create a factual catalogue draft and rewrite an email with versioned voice rules.

Run: uv run python modules/02_prompt_templates/use_case/brand_writer.py --offline
Expected: Two labelled drafts; publishing and sending remain outside this app.
Cost: Two short hosted calls, usually under $0.01 total; offline/local free of API fees.
"""

import json

from langchain_core.prompts import ChatPromptTemplate

from common.config import ROOT
from common.data import load_csv
from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message, print_text


def main() -> None:
    settings = lesson_settings()
    product = load_csv("products.csv")[0]
    jobs = [
        ("brand_voice", "product", json.dumps(product)),
        ("tone_rewrite", "email", "Please send your receipt so we can review your return request."),
    ]
    for filename, delimiter, source in jobs:
        rules = (ROOT / f"modules/02_prompt_templates/prompts/{filename}.txt").read_text(
            encoding="utf-8"
        )
        prompt = ChatPromptTemplate.from_messages(
            [("system", rules), ("human", f"<{delimiter}>{{source}}</{delimiter}>")]
        )
        model = get_chat_model(
            settings=settings,
            responses=[
                "Ridge Tent: practical shelter for two."
                if filename == "brand_voice"
                else "Please share your receipt so we can review your return request."
            ],
        )
        print_text(filename + " draft:")
        print_message(model.invoke(prompt.invoke({"source": source})))


if __name__ == "__main__":
    run_cli(main)
