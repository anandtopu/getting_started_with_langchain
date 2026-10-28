"""Build the model-tool loop by hand using ToolNode.

Run: uv run --extra agents python modules/14_langgraph/examples/04_manual_agent_graph.py --offline
Expected: One stock tool result and a final model answer.
Cost: At most three short model calls; a tool-calling model is required. Offline fixtures incur
no API fee.
Requires: agents
"""

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.prebuilt import ToolNode

from common.errors import run_cli
from common.fixtures import tool_request
from common.lesson import lesson_settings
from common.models import get_chat_model
from common.pretty import print_message
from common.tools import make_order_tools


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    calls: int


def main() -> None:
    settings = lesson_settings()
    tools = [make_order_tools("C001")[2]]
    model = get_chat_model(
        settings=settings,
        responses=[tool_request("check_stock", {"sku": "BW-001"}), "Stock checked."],
    ).bind_tools(tools)

    def call(state: State) -> dict:
        return {"messages": [model.invoke(state["messages"])], "calls": state["calls"] + 1}

    def route(state: State) -> Literal["tools", "__end__"]:
        if state["messages"][-1].tool_calls:
            if state["calls"] >= 3:
                raise ValueError("Three-call budget exhausted before another tool dispatch.")
            return "tools"
        return END

    # KEY IDEA: the loop is ordinary graph routing with an explicit call ceiling.
    graph = StateGraph(State)
    graph.add_node("model", call)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "model")
    graph.add_conditional_edges("model", route)
    graph.add_edge("tools", "model")
    result = graph.compile().invoke(
        {"messages": [HumanMessage("Check BW-001 stock")], "calls": 0}, {"recursion_limit": 10}
    )
    for message in result["messages"]:
        print_message(message)


if __name__ == "__main__":
    run_cli(main)
