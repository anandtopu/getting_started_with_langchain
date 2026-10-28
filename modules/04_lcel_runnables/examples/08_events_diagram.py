"""Inspect runnable lifecycle events and a locally generated Mermaid graph.

Run: uv run python modules/04_lcel_runnables/examples/08_events_diagram.py --offline
Expected: Mermaid text plus on_chain_start/on_chain_stream/on_chain_end events.
Cost: No model or rendering-service calls; Mermaid text is generated locally.
"""

import asyncio

from langchain_core.runnables import Runnable, RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def pipeline() -> Runnable:
    return RunnableLambda(lambda text: text.strip(), name="trim") | RunnableLambda(
        str.upper, name="uppercase"
    )


async def show_events() -> None:
    async for event in pipeline().astream_events(" bw-001 ", version="v2"):
        print_text(f"{event['event']}: {event['name']}")


def main() -> None:
    lesson_settings()
    # KEY IDEA: lifecycle events describe execution; they are not all model text tokens.
    print_text(pipeline().get_graph().draw_mermaid())
    asyncio.run(show_events())


if __name__ == "__main__":
    run_cli(main)
