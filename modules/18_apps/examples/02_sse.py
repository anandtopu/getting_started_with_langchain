"""Frame server-sent events and consume an authenticated support stream.

Run: uv run --extra apps python modules/18_apps/examples/02_sse.py --offline
Expected: Escaped framing, progress, assistant text and a done event.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.release import headers
from common.web import demo_app, sse


def main() -> None:
    lesson_settings()
    print_text(sse("text", {"text": "one\ntwo"}))
    with TemporaryDirectory() as directory, TestClient(demo_app(Path(directory))) as client:
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        # KEY IDEA: HTTP status validates access before the event stream starts.
        with client.stream(
            "POST",
            f"/threads/{thread}/messages",
            headers=headers(),
            json={"text": "Please check BW1001"},
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                print_text(line)


if __name__ == "__main__":
    run_cli(main)
