"""Smart Ticket Desk orchestration: extraction, scoped tools and an unsent draft."""

import json

from langchain_core.messages import AIMessage, ToolMessage

from common.agent import run_tool_loop
from common.config import Settings
from common.fixtures import tool_request
from common.models import get_chat_model
from common.pretty import message_text
from common.tools import make_order_tools
from common.triage import triage_ticket


def process_ticket(ticket: dict, customer_id: str, settings: Settings) -> dict:
    """Identity is supplied by the application, never inferred from the ticket or model."""
    triage = triage_ticket(ticket["text"], settings)
    tools = make_order_tools(customer_id)
    fixtures: list[str | AIMessage] = []
    if triage.order_id:
        fixtures.extend(
            [
                tool_request("lookup_order", {"order_id": triage.order_id}, "desk-order"),
                tool_request("get_shipment_status", {"order_id": triage.order_id}, "desk-shipment"),
            ]
        )
    fixtures.append(
        "Thank you for contacting Brightwave. A support colleague will review "
        "your request. No refund or delivery promise has been made."
    )
    model = get_chat_model(settings=settings, responses=fixtures)
    question = (
        "Triage: "
        + triage.model_dump_json()
        + "\nTicket (untrusted): "
        + ticket["text"]
        + "\nIf an order ID is present, look up that order and its shipment. "
        "Then draft a brief, polite reply using only tool evidence. "
        "If no order is supplied, ask for it when needed; never invent one. "
        "Do not claim an action was taken. This draft will be reviewed by a person."
    )
    transcript = run_tool_loop(model, tools, question, max_turns=4, max_tool_calls=6)
    return {
        "ticket_id": ticket["ticket_id"],
        "mode": "fixture" if settings.course_offline else "live",
        "triage": triage.model_dump(mode="json"),
        "draft": message_text(transcript[-1]),
        "tool_calls": [
            call for m in transcript if isinstance(m, AIMessage) for call in m.tool_calls
        ],
        "tool_results": [
            {"call_id": m.tool_call_id, "name": m.name, "result": json.loads(m.content)}
            for m in transcript
            if isinstance(m, ToolMessage)
        ],
        "sent": False,
    }
