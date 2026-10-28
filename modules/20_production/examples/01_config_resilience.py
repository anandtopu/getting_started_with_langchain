"""Bound retries and fallback, rate-limit calls, and validate startup secrets.

Run: uv run --extra apps python modules/20_production/examples/01_config_resilience.py --offline
Expected: Exactly two attempts, a bounded fallback and rejected invalid startup.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.web import configured_app


def main() -> None:
    settings = lesson_settings()
    attempts = 0

    def transient(text: str) -> str:
        nonlocal attempts
        attempts += 1
        raise TimeoutError("Synthetic transport timeout")

    # KEY IDEA: only transient failures retry; bounded fallback does not grant new permissions.
    chain = (
        RunnableLambda(transient)
        .with_retry(
            retry_if_exception_type=(TimeoutError,),
            stop_after_attempt=2,
            wait_exponential_jitter=False,
        )
        .with_fallbacks([RunnableLambda(lambda text: "Please try again later.")])
    )
    limiter = InMemoryRateLimiter(requests_per_second=1000, check_every_n_seconds=0.001)
    limiter.acquire()
    print_text(
        str(
            {
                "answer": chain.invoke("BW1001"),
                "attempts": attempts,
                "model_timeout": settings.model_timeout,
            }
        )
    )
    try:
        configured_app(settings.model_copy(update={"api_customer_id": "invalid id"}))
    except ValueError:
        print_text("Invalid startup identity rejected.")


if __name__ == "__main__":
    run_cli(main)
