"""Read-only, customer-scoped tools. Identity comes from trusted application context."""

from langchain.tools import tool
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from common.data import orders_connection


class OrderInput(BaseModel):
    """A synthetic Brightwave order identifier."""

    order_id: str = Field(pattern=r"^BW\d{4}$")


class StockInput(BaseModel):
    """A Brightwave stock-keeping unit; SKU is a product's catalogue code."""

    sku: str = Field(pattern=r"^BW-\d{3}$")


def make_order_tools(customer_id: str) -> list[BaseTool]:
    """Close over authenticated identity; never expose customer_id as a model argument."""

    @tool(args_schema=OrderInput)
    def lookup_order(order_id: str) -> dict:
        """Read the current customer's order status and total; does not change orders."""
        with orders_connection() as db:
            row = db.execute(
                "SELECT order_id, status, total_cents FROM orders "
                "WHERE order_id = ? AND customer_id = ?",
                (order_id, customer_id),
            ).fetchone()
        return dict(row) if row else {"error": "Order not found for this customer."}

    @tool(args_schema=OrderInput)
    def get_shipment_status(order_id: str) -> dict:
        """Read shipment details only for an order owned by the current customer."""
        with orders_connection() as db:
            owned = db.execute(
                "SELECT order_id FROM orders WHERE order_id = ? AND customer_id = ?",
                (order_id, customer_id),
            ).fetchone()
            if not owned:
                return {"error": "Order not found for this customer."}
            row = db.execute("SELECT * FROM shipments WHERE order_id = ?", (order_id,)).fetchone()
        return dict(row) if row else {"order_id": order_id, "status": "Not shipped yet."}

    @tool(args_schema=StockInput)
    def check_stock(sku: str) -> dict:
        """Read current stock for a public product SKU; stock is not a reservation."""
        with orders_connection() as db:
            row = db.execute(
                "SELECT sku, name, stock FROM products WHERE sku = ?", (sku,)
            ).fetchone()
        return dict(row) if row else {"error": "Unknown SKU."}

    return [lookup_order, get_shipment_status, check_stock]
