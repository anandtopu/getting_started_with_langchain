"""Flagship support service: the tested API adds policy RAG to scoped SQL and durable reviews."""

import re
from pathlib import Path
from typing import Any

from langchain.tools import tool

from common.config import ROOT, Settings, get_settings
from common.fixtures import tool_request
from common.knowledge import policy_documents
from common.rag import answer_question
from common.retrieval import LexicalRetriever
from common.security import Principal
from common.service import SupportService
from common.tools import make_order_tools


class CopilotService(SupportService):
    # Three agent calls plus two policy tools with one RAG call each; no SDK retries.
    request_call_reservation = 5

    def chat_plan(self, principal: Principal, text: str) -> tuple[list, Any]:
        records = []
        scoped = make_order_tools(principal.subject)

        @tool
        def lookup_order(order_id: str) -> dict:
            """Read only the authenticated customer's order, preserving access denials."""
            result = scoped[0].invoke({"order_id": order_id})
            records.append(result)
            return result

        @tool
        def search_policy(query: str) -> dict:
            """Retrieve public policy passages and return validated exact-quote citations."""
            found = LexicalRetriever(policy_documents()).search(query)
            result = answer_question(
                query, found, self.settings.model_copy(update={"model_max_retries": 0})
            )
            records.append(result)
            return result

        def responses():
            order = re.search(r"\bBW\d{4}\b", text)
            if order:
                yield tool_request("lookup_order", {"order_id": order[0]})
            elif any(word in text.lower() for word in ("return", "shipping", "warranty")):
                yield tool_request("search_policy", {"query": text})
            else:
                yield "Please clarify your Brightwave question."
                return
            result = records[-1]
            if "error" in result:
                yield "I cannot access that order for this customer. Please verify the order."
            elif "answer" in result:
                citations = " ".join(f"[{c['source']}]" for c in result["citations"])
                yield "Please review the policy evidence: " + result["answer"] + " " + citations
            else:
                yield f"Order {result['order_id']} is {result['status']}. Please ask for help."

        return [lookup_order, scoped[1], scoped[2], search_policy], responses()


def copilot_app(settings: Settings | None = None, *, directory: Path | None = None) -> Any:
    from common.web import create_app

    settings = settings or get_settings()
    customer = settings.api_customer_token.get_secret_value()
    manager = settings.api_manager_token.get_secret_value()
    if customer == manager or not settings.api_customer_id.isalnum():
        raise ValueError("Configure distinct API tokens and a valid synthetic customer ID.")
    return create_app(
        CopilotService(directory or ROOT / settings.runtime_dir / "copilot", settings),
        {
            customer: Principal(settings.api_customer_id, "customer"),
            manager: Principal("reviewer", "manager"),
        },
    )


def copilot_demo(directory: Path) -> Any:
    from common.release import CUSTOMER, OTHER, REVIEWER
    from common.web import create_app

    service = CopilotService(directory, Settings(course_offline=True, model_max_retries=0))
    service.attest("BW1001", "BW-014", inspected=True, proof=True)
    return create_app(
        service,
        {
            CUSTOMER: Principal("C001", "customer"),
            OTHER: Principal("C002", "customer"),
            REVIEWER: Principal("reviewer", "manager"),
        },
    )
