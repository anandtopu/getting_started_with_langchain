"""Demonstrate a bounded retry and a fallback with deliberate failures.

Run: uv run python modules/04_lcel_runnables/examples/06_resilience.py --offline
Expected: Retry succeeds on attempt 2; a permanent failure uses the alternate path.
Cost: No API calls; only deliberate local failures.
"""

from collections.abc import Callable

from langchain_core.runnables import RunnableLambda

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def transient_request() -> Callable[[str], str]:
    attempts = 0

    def request(text: str) -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise TimeoutError("Synthetic temporary timeout")
        return f"Recovered on attempt {attempts}: {text}"

    return request


def unavailable(text: str) -> str:
    raise TimeoutError("Synthetic service outage")


def main() -> None:
    lesson_settings()
    retry = RunnableLambda(transient_request()).with_retry(
        retry_if_exception_type=(TimeoutError,), stop_after_attempt=2, wait_exponential_jitter=False
    )
    print_text(retry.invoke("Brightwave review"))
    # KEY IDEA: retries repeat one path; fallbacks invoke an alternative implementation.
    alternate = RunnableLambda(unavailable).with_fallbacks(
        [RunnableLambda(lambda _: "Queue for human review")], exceptions_to_handle=(TimeoutError,)
    )
    print_text(alternate.invoke("Brightwave review"))


if __name__ == "__main__":
    run_cli(main)
