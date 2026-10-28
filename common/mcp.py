"""Read-only inventory MCP boundary using the official SDK and current LangChain adapter."""

import sys
from contextlib import ExitStack, asynccontextmanager
from tempfile import TemporaryFile
from typing import Any
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field

from common.config import ROOT
from common.data import orders_connection


class InventoryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sku: str = Field(pattern=r"^BW-\d{3}$")


class InventoryResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sku: str = Field(pattern=r"^BW-\d{3}$")
    stock: int = Field(ge=0, le=1000000)
    name: str = Field(min_length=1, max_length=200)


def inventory(sku: str) -> dict:
    request = InventoryInput(sku=sku)
    with orders_connection() as db:
        row = db.execute(
            "SELECT sku,stock,name FROM products WHERE sku=?", (request.sku,)
        ).fetchone()
    if row is None:
        raise ValueError("Unknown SKU.")
    return InventoryResult.model_validate(dict(row)).model_dump()


def inventory_server() -> Any:
    from typing import Annotated

    from mcp.server.mcpserver import MCPServer
    from mcp.types import ToolAnnotations

    server = MCPServer("brightwave-inventory", version="1.0.0")

    @server.tool(
        name="inventory_stock",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
    )
    def inventory_stock(sku: Annotated[str, Field(pattern=r"^BW-\d{3}$")]) -> InventoryResult:
        """Read public synthetic stock. No reservation or write permission."""
        return InventoryResult.model_validate(inventory(sku))

    return server


def validate_endpoint(url: str) -> str:
    """This lesson deliberately accepts only its loopback server; no arbitrary remote hosts."""
    parsed = urlsplit(url)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.port != 8765
        or parsed.path != "/mcp"
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Only http://127.0.0.1:8765/mcp is allowed in this lesson.")
    return url


def checked_tools(tools: list[Any]) -> list[Any]:
    if len(tools) != 1 or tools[0].name != "inventory_stock":
        raise ValueError("Unexpected server tools; review before exposing them to the agent.")
    schema = tools[0].args_schema
    schema = schema.model_json_schema() if isinstance(schema, type) else schema
    if set(schema.get("properties", {})) != {"sku"} or schema.get("required") != ["sku"]:
        raise ValueError("Inventory schema changed; refuse discovery until reviewed.")
    return tools


@asynccontextmanager
async def inventory_adapter(transport: str = "memory") -> Any:
    """Memory and ASGI HTTP perform real protocol exchanges without network sockets."""
    from fastmcp import Client
    from fastmcp.client.transports import StdioTransport, StreamableHttpTransport
    from langchain.mcp import MCPAdapter

    # Notebook stderr may lack fileno; the subprocess owns a real diagnostic file.
    with ExitStack() as resources:
        if transport == "stdio":
            connection = StdioTransport(
                sys.executable,
                [str(ROOT / "modules/13_mcp/use_case/inventory_server.py"), "--stdio"],
                cwd=str(ROOT),
                log_file=resources.enter_context(TemporaryFile(mode="w+", encoding="utf-8")),
                env={"COURSE_OFFLINE": "true", "LANGSMITH_TRACING": "false"},
            )
        elif transport == "memory":
            connection = inventory_server()
        elif transport == "http":
            import httpx2

            server = inventory_server()
            app = server.streamable_http_app(json_response=True, stateless_http=True)

            def client_factory(**kwargs: Any) -> Any:
                return httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), **kwargs)

            async with app.router.lifespan_context(app):
                client = Client(
                    StreamableHttpTransport(
                        validate_endpoint("http://127.0.0.1:8765/mcp"),
                        httpx_client_factory=client_factory,
                    ),
                    timeout=10,
                )
                async with MCPAdapter(client) as adapter:
                    yield adapter
            return
        else:
            raise ValueError("Choose memory, stdio or http.")
        async with MCPAdapter(Client(connection, timeout=10)) as adapter:
            yield adapter


async def call_inventory(adapter: Any, sku: str) -> dict:
    """Validate both the requested identity and result before using server-supplied data."""
    request = InventoryInput(sku=sku)
    tools = checked_tools(await adapter.list_tools())
    result = await tools[0].ainvoke({"sku": request.sku})
    # Adapter outputs content blocks; use the JSON text from the reviewed server.
    if isinstance(result, list):
        text = next(item["text"] for item in result if item.get("type") == "text")
    elif isinstance(result, str):
        text = result
    else:
        raise ValueError("Unexpected inventory response shape.")
    validated = InventoryResult.model_validate_json(text)
    if validated.sku != request.sku:
        raise ValueError("Server returned another SKU.")
    return validated.model_dump()
