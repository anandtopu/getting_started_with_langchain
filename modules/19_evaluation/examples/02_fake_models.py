"""Separate scripted transport tests from model-quality evidence.

Run: uv run --extra agents python modules/19_evaluation/examples/02_fake_models.py --offline
Expected: A real ownership denial and two fake vectors.
Cost: No API calls; deterministic local checks. Requires: agents
"""

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model, get_embeddings
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    settings = lesson_settings().model_copy(update={"course_offline": True})
    model = get_chat_model(
        settings=settings, responses=[tool_request("lookup_order", {"order_id": "BW1001"})]
    )
    call = model.invoke("Check my order.").tool_calls[0]
    # KEY IDEA: the fixture supplies the call, but the tool executes real ownership checks.
    result = make_order_tools("C002")[0].invoke(call["args"])
    assert "error" in result
    print_text(str(result))
    vectors = get_embeddings(settings=settings).embed_documents(
        ["Brightwave tent", "Brightwave pack"]
    )
    print_text(str({"vectors": len(vectors), "semantic_quality_claim": False}))


if __name__ == "__main__":
    run_cli(main)
