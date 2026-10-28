"""Insert supplied messages into a chat template; the template stores no memory.

Run: uv run python modules/02_prompt_templates/examples/02_chat_history.py --offline
Expected: system, human, ai, human message order.
Cost: No model call.
"""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_message


def history_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", "Write brief Brightwave replies."),
            MessagesPlaceholder("history"),
            ("human", "{request}"),
        ]
    )


def main() -> None:
    lesson_settings()
    history = [HumanMessage("I need a tent."), AIMessage("How many people?")]
    # KEY IDEA: history is an input list; the application must supply it on every call.
    for message in history_prompt().invoke({"history": history, "request": "Two people."}).messages:
        print_message(message)


if __name__ == "__main__":
    run_cli(main)
