"""Teach an output style with small input/output demonstrations.

Run: uv run python modules/02_prompt_templates/examples/03_few_shot.py --offline
Expected: A prompt with two examples and a new customer request.
Cost: No model call.
"""

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def few_shot_prompt() -> ChatPromptTemplate:
    example = ChatPromptTemplate.from_messages([("human", "{rough}"), ("ai", "{polite}")])
    shots = FewShotChatMessagePromptTemplate(
        example_prompt=example,
        examples=[
            {
                "rough": "Your parcel is late.",
                "polite": "I'm sorry your parcel is delayed. Let's check its status.",
            },
            {
                "rough": "That tent is gone.",
                "polite": "That tent is currently unavailable. May I help find an alternative?",
            },
        ],
    )
    # KEY IDEA: examples are messages in the request, not training or persisted memory.
    return ChatPromptTemplate.from_messages(
        [("system", "Rewrite without inventing facts."), shots, ("human", "{rough}")]
    )


def main() -> None:
    lesson_settings()
    print_text(few_shot_prompt().invoke({"rough": "We need your order number."}).to_string())


if __name__ == "__main__":
    run_cli(main)
