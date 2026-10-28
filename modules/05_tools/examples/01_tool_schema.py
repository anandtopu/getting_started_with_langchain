"""Turn a typed function and its docstring into a tool contract.

Run: uv run python modules/05_tools/examples/01_tool_schema.py --offline
Expected: A JSON input schema and a stock record from the read-only database.
Cost: No model calls; database reads only.
"""

import json

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.tools import make_order_tools


def main() -> None:
    lesson_settings()
    stock = make_order_tools("C001")[2]
    # KEY IDEA: the model sees a schema, not the Python function's implementation.
    print_text(stock.description)
    print_text(json.dumps(stock.args_schema.model_json_schema(), indent=2))
    print_text(str(stock.invoke({"sku": "BW-001"})))


if __name__ == "__main__":
    run_cli(main)
