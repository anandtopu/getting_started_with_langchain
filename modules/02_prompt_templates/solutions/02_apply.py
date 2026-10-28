"""Supply chat history.

Task: Build a chat template with system, supplied history, then current human request. History
is not storage.
Run: uv run python modules/02_prompt_templates/solutions/02_apply.py --offline
Expected: a runnable complete solution demonstration.
Cost: offline is free; any model demo uses at most three short calls.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", "Help Brightwave shoppers."),
            MessagesPlaceholder("history"),
            ("human", "{request}"),
        ]
    )


def main() -> None:
    lesson_settings()
    print_text(template().invoke({"history": [], "request": "Need a tent."}).to_string())


if __name__ == "__main__":
    run_cli(main)
