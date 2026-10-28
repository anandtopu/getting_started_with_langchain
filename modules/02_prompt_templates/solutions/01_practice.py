"""Bind a brand constant.

Task: Return a PromptTemplate with brand partially bound to Brightwave and required
product/facts inputs.
Run: uv run python modules/02_prompt_templates/solutions/01_practice.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.prompts import PromptTemplate

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def template() -> PromptTemplate:
    return PromptTemplate.from_template(
        "Write a factual {brand} description for {product}. Facts: {facts}"
    ).partial(brand="Brightwave")


def main() -> None:
    lesson_settings()
    print_text(template().invoke({"product": "Ridge Tent", "facts": "2-person"}).to_string())


if __name__ == "__main__":
    run_cli(main)
