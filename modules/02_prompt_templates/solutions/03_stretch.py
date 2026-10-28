"""Build a few-shot rewriter.

Task: Include one rough/polite example pair before the new rough input and retain a no-
invented-facts system rule.
Run: uv run python modules/02_prompt_templates/solutions/03_stretch.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def template() -> ChatPromptTemplate:
    pair = ChatPromptTemplate.from_messages([("human", "{rough}"), ("ai", "{polite}")])
    examples = FewShotChatMessagePromptTemplate(
        example_prompt=pair,
        examples=[{"rough": "Need receipt.", "polite": "Please share your receipt."}],
    )
    return ChatPromptTemplate.from_messages(
        [("system", "Use Brightwave tone; do not invent facts."), examples, ("human", "{rough}")]
    )


def main() -> None:
    lesson_settings()
    print_text(template().invoke({"rough": "Need order number."}).to_string())


if __name__ == "__main__":
    run_cli(main)
