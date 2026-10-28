"""Choose the smallest building block for a Brightwave task.

Run: uv run python modules/00_setup/examples/02_ecosystem.py --offline
Expected: Draft -> model; fixed pipeline -> LCEL; durable approval -> LangGraph.
Cost: No model calls.
"""

from importlib.metadata import version

from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text


def choose_block(
    *, fixed_steps: bool = False, durable: bool = False, tool_decisions: bool = False
) -> str:
    if durable:
        return "LangGraph"
    if tool_decisions:
        return "LangChain agent"
    return "LCEL" if fixed_steps else "model"


def main() -> None:
    lesson_settings()
    for package in ("langchain", "langchain-core", "langchain-openai", "langgraph", "langsmith"):
        print_text(f"{package}: {version(package)}")
    # KEY IDEA: a bigger framework is useful only when the task needs its behavior.
    print_text(
        f"Draft: {choose_block()}; fixed pipeline: {choose_block(fixed_steps=True)}; "
        f"durable approval: {choose_block(durable=True)}"
    )
    print_text(
        "core defines interfaces; providers translate requests; LangSmith observes; "
        "Deep Agents adds planning/filesystem patterns in an optional later tier."
    )


if __name__ == "__main__":
    run_cli(main)
