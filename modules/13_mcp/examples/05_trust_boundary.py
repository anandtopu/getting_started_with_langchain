"""Reject unknown endpoints, tool sets and malformed inventory results.

Run from the repository root (join wrapped command lines):
uv run --extra agents python modules/13_mcp/examples/05_trust_boundary.py --offline
Expected: Three explicit validation failures; trusted annotations are not assumed.
Cost: No model calls or external connections.
Requires: agents
"""

from common.errors import run_cli
from common.lesson import lesson_settings
from common.mcp import InventoryResult, checked_tools, validate_endpoint
from common.pretty import print_text


def main() -> None:
    lesson_settings()
    # KEY IDEA: protocol compatibility does not grant execution permission or establish truth.
    for operation in [
        lambda: validate_endpoint("https://unreviewed.example.test/mcp"),
        lambda: checked_tools([]),
        lambda: InventoryResult(sku="BW-001", stock=-1, name="Ridge Tent"),
    ]:
        try:
            operation()
        except ValueError as error:
            print_text(f"Rejected: {type(error).__name__}: {error}")


if __name__ == "__main__":
    run_cli(main)
