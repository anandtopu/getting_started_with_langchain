"""Await I/O, bound concurrency, cancel work, and inspect model chunks.

Run: uv run --extra apps python modules/18_apps/examples/01_async_basics.py --offline
Expected: Three replies, cancellation acknowledgement and streamed chunks.
Cost: Four short model calls live; zero in offline mode. Requires: apps
"""

import asyncio

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_text


async def demonstrate(settings) -> None:
    semaphore = asyncio.Semaphore(2)

    async def reply(index: int) -> str:
        async with semaphore:
            model = get_chat_model(settings=settings, responses=[f"Brightwave reply {index}"])
            result = await model.ainvoke("Say a short Brightwave greeting.")
            return str(result.content)

    print_text(str(await asyncio.gather(*(reply(i) for i in range(3)))))
    waiting = asyncio.create_task(asyncio.sleep(60))
    waiting.cancel()
    try:
        await waiting
    except asyncio.CancelledError:
        print_text("Cancelled and awaited; resources can now be released.")
    # KEY IDEA: move blocking work off the event loop, not into an async def unchanged.
    print_text(await asyncio.to_thread(lambda: "Blocking preparation finished."))
    model = get_chat_model(settings=settings, responses=["Brightwave stream complete."])
    async for chunk in model.astream("Say a short Brightwave greeting."):
        print_text(str(chunk.content))


def main() -> None:
    asyncio.run(demonstrate(lesson_settings()))


if __name__ == "__main__":
    run_cli(main)
