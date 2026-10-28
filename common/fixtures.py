"""Explicit scripted model fixtures; never a substitute for live model evaluation."""

from collections.abc import Callable, Sequence
from typing import Any

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool


class ScriptedChatModel(GenericFakeChatModel):
    """Use LangChain's fake generation with real structured-output parsing.

    Binding records schemas but does not make decisions or enforce provider-native
    constraints. Only explicitly supplied AIMessage fixtures request tools.
    """

    def bind_tools(
        self,
        tools: Sequence[dict[str, Any] | type | Callable | BaseTool],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ) -> Any:
        return self.bind(
            tools=[convert_to_openai_tool(tool) for tool in tools],
            tool_choice=tool_choice,
            **kwargs,
        )


def structured_fixture(schema: type | dict, values: dict) -> AIMessage:
    """A predetermined tool envelope feeds LangChain's real Pydantic/dict parser."""
    name = convert_to_openai_tool(schema)["function"]["name"]
    return AIMessage(content="", tool_calls=[{"name": name, "args": values, "id": "fixture-1"}])


def tool_request(name: str, args: dict, call_id: str = "call-1") -> AIMessage:
    """Make the transport fixture visible in examples that teach dispatch."""
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": call_id}])
