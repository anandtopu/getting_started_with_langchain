"""Separate reusable instructions from product variables and partial constants.

Run: uv run python modules/02_prompt_templates/examples/01_variables.py --offline
Expected: A formatted prompt containing Brightwave and Ridge Tent.
Cost: Formatting only; no model call.
"""

from langchain_core.prompts import PromptTemplate

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def product_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        "Write one factual {brand} sentence for {product}. Use only these facts: {facts}."
    ).partial(brand="Brightwave")


def main() -> None:
    lesson_settings()
    prompt = product_prompt()
    # KEY IDEA: partial binds the constant once; the product stays a required input.
    print_text(str(prompt.input_variables))
    print_text(
        prompt.invoke(
            {"product": "Ridge Tent", "facts": "2-person; 3000 mm waterproof rating"}
        ).to_string()
    )


if __name__ == "__main__":
    run_cli(main)
