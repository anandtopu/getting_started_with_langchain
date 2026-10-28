"""Carry tags/metadata/run names through a bounded batch and asynchronous call.

Run: uv run python modules/04_lcel_runnables/examples/07_config_batch.py --offline
Expected: Three normalized SKUs followed by one awaited SKU.
Cost: No API calls; do not place secrets or ticket text in trace metadata.
"""

import asyncio

from langchain_core.runnables import Runnable, RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


async def async_example(pipeline: Runnable) -> None:
    print_text(await pipeline.ainvoke(" bw-004 "))


def main() -> None:
    lesson_settings()
    pipeline = RunnableLambda(lambda sku: sku.strip().upper()).with_config(
        tags=["brightwave", "foundation"], metadata={"lesson": "04"}, run_name="normalize_sku"
    )
    # KEY IDEA: config controls execution/tracing; it is not a prompt variable.
    print_text(str(pipeline.batch(["bw-001", "bw-002", "bw-003"], config={"max_concurrency": 2})))
    asyncio.run(async_example(pipeline))


if __name__ == "__main__":
    run_cli(main)
