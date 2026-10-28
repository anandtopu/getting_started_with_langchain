"""Attach an in-process token-bucket request limiter to a model.

Run: uv run python modules/01_chat_models/examples/08_rate_limit.py --offline
Expected: Two replies paced at no more than two requests per second.
Cost: Two short calls; fixture/local modes have no API fee.
"""

from langchain_core.rate_limiters import InMemoryRateLimiter

from common.errors import run_cli
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message


def main() -> None:
    settings = lesson_settings()
    limiter = InMemoryRateLimiter(
        requests_per_second=2, check_every_n_seconds=0.05, max_bucket_size=1
    )
    model = get_chat_model(settings=settings)
    model.rate_limiter = limiter
    # KEY IDEA: concurrency caps simultaneous work; rate limiting caps starts over time.
    for message in model.batch(
        ["Greet a tent buyer.", "Greet a boot buyer."], config={"max_concurrency": 2}
    ):
        print_message(message)


if __name__ == "__main__":
    run_cli(main)
