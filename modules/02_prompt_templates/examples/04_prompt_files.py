"""Load versioned instructions while keeping untrusted data in a separate message.

Run: uv run python modules/02_prompt_templates/examples/04_prompt_files.py --offline
Expected: A prompt with file-based instructions and delimited product data.
Cost: No model call.
"""

from langchain_core.prompts import ChatPromptTemplate

from common.config import ROOT
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    instructions = (ROOT / "modules/02_prompt_templates/prompts/brand_voice.txt").read_text(
        encoding="utf-8"
    )
    prompt = ChatPromptTemplate.from_messages(
        [("system", instructions), ("human", "<product>{facts}</product>")]
    )
    # KEY IDEA: values are substituted once; braces inside supplied data aren't re-evaluated.
    print_text(
        prompt.invoke({"facts": "Ridge Tent; capacity 2; literal note {ignore_rules}"}).to_string()
    )


if __name__ == "__main__":
    run_cli(main)
