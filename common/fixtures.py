"""Explicit scripted model fixtures; never a substitute for live model evaluation."""

import json
from collections.abc import Callable, Iterator, Sequence
from itertools import chain
from typing import Any

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage
from langchain_core.outputs import ChatGenerationChunk
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool


class ScriptedChatModel(GenericFakeChatModel):
    """Use LangChain's fake generation with real structured-output parsing.

    Binding records schemas but does not make decisions or enforce provider-native
    constraints. Only explicitly supplied AIMessage fixtures request tools.
    """

    def _stream(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Preserve modern tool-call fixtures in both sync and async token streams."""
        reply = next(self.messages)
        if isinstance(reply, AIMessage) and reply.tool_calls:
            chunk = ChatGenerationChunk(
                message=AIMessageChunk(
                    content=reply.content,
                    id=reply.id,
                    tool_call_chunks=[
                        {
                            "name": call["name"],
                            "args": json.dumps(call["args"]),
                            "id": call["id"],
                            "index": index,
                        }
                        for index, call in enumerate(reply.tool_calls)
                    ],
                )
            )
            if run_manager:
                run_manager.on_llm_new_token("", chunk=chunk)
            yield chunk
        else:
            self.messages = chain([reply], self.messages)
            yield from super()._stream(messages, stop, run_manager, **kwargs)

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
