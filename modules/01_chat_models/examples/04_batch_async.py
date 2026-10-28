"""Compare batch with async/await: concurrency overlaps waiting for responses.

Run: uv run python modules/01_chat_models/examples/04_batch_async.py --offline
Expected: Two ordered batch replies and one awaited reply.
Cost: Three short hosted calls, typically under $0.01 total; offline/local no API fee.
"""

import asyncio

from langchain_core.language_models import BaseChatModel

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message


async def greet_async(model: BaseChatModel) -> None:
    # await yields control while IO is pending; it does not create another paid request.
    print_message(await model.ainvoke("Welcome a Brightwave customer."))


def main() -> None:
    settings = lesson_settings()
    model = get_chat_model(settings=settings)
    for reply in model.batch(
        ["Greet a tent buyer.", "Greet a backpack buyer."], config={"max_concurrency": 2}
    ):
        print_message(reply)
    # KEY IDEA: asyncio owns the event loop in a script. In notebooks use await directly.
    asyncio.run(greet_async(model))


if __name__ == "__main__":
    run_cli(main)
