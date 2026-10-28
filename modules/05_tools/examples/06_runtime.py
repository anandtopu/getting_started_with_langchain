"""Inspect ToolRuntime context and state using an explicit injection harness.

Run: uv run python modules/05_tools/examples/06_runtime.py --offline
Expected: Customer C001 and two supplied messages; runtime is absent from the public tool schema.
Cost: No model call. Module 10 replaces the harness with agent-managed injection.
"""

from dataclasses import dataclass

from langchain.tools import ToolRuntime, tool
from langchain_core.messages import HumanMessage

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


@dataclass(frozen=True)
class CustomerContext:
    customer_id: str


@tool
def session_summary(runtime: ToolRuntime[CustomerContext]) -> str:
    """Read the trusted session identity and current message count."""
    return f"Customer {runtime.context.customer_id}; messages={len(runtime.state['messages'])}"


def main() -> None:
    lesson_settings()
    runtime = ToolRuntime(
        state={"messages": [HumanMessage("Hello"), HumanMessage("Order status?")]},
        context=CustomerContext("C001"),
        config={},
        stream_writer=lambda _: None,
        tool_call_id="runtime-1",
        store=None,
    )
    # KEY IDEA: normally the agent injects runtime. This harness supplies it explicitly.
    print_text(session_summary.invoke({"runtime": runtime}))
    print_text(str(session_summary.tool_call_schema.model_json_schema()))


if __name__ == "__main__":
    run_cli(main)
