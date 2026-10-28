"""Held-out support contracts and transparent local metrics without answer-key leakage."""

import hashlib
import json
import re
from collections.abc import Iterator
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain.tools import tool
from langchain_core.messages import AIMessage
from langsmith import tracing_context

from common.config import ROOT, Settings
from common.fixtures import tool_request
from common.knowledge import policy_documents
from common.models import get_chat_model
from common.rag import answer_question
from common.retrieval import LexicalRetriever
from common.tools import make_order_tools


def evaluate_trajectory(actual: list[dict], expected: list[dict], forbidden: list[str]) -> bool:
    return actual == expected and not any(call["name"] in forbidden for call in actual)


def support_answer(
    question: str, customer: str, settings: Settings, *, version: str = "v2"
) -> dict:
    if version not in {"v1", "v2"}:
        raise ValueError("Unknown prompt version.")
    prompt = (ROOT / "modules/19_evaluation/prompts" / f"support_{version}.txt").read_text(
        encoding="utf-8"
    )
    records: list[dict] = []
    scoped = make_order_tools(customer)

    @tool
    def lookup_order(order_id: str) -> dict:
        """Read the authenticated customer's order and preserve ownership denial."""
        result = scoped[0].invoke({"order_id": order_id})
        records.append(result)
        return result

    @tool
    def search_policy(query: str) -> dict:
        """Retrieve public policy evidence and validate citations."""
        docs = LexicalRetriever(policy_documents()).search(query)
        result = answer_question(query, docs, settings)
        records.append(result)
        return result

    def responses() -> Iterator[str | AIMessage]:
        # The fixture reads only the request and real tool outputs, never evaluator labels.
        order = re.search(r"\bBW\d{4}\b", question)
        if order:
            yield tool_request("lookup_order", {"order_id": order[0]})
        elif any(word in question.lower() for word in ("return", "shipping", "warranty")):
            yield tool_request("search_policy", {"query": question})
        else:
            yield "Please clarify your Brightwave question."
            return
        result = records[-1]
        if "error" in result:
            yield "I cannot access that order for this customer. Please verify the order."
        elif "answer" in result:
            yield "Please review the policy evidence: " + result["answer"]
        else:
            yield (
                f"Order {result['order_id']} is {result['status']}. "
                "Please ask if you need more help."
            )

    agent = create_agent(
        get_chat_model(settings=settings, responses=responses()),
        [lookup_order, search_policy],
        system_prompt=prompt,
        middleware=[
            ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=2, exit_behavior="end"),
        ],
    )
    with tracing_context(enabled=False):
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]}, {"recursion_limit": 30}
        )
    calls = [
        {"name": call["name"], "args": call["args"]}
        for message in result["messages"]
        if message.type == "ai"
        for call in message.tool_calls
    ]
    return {
        "answer": str(result["messages"][-1].content),
        "trajectory": calls,
        "evidence": records,
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "mode": "scripted-contract" if settings.course_offline else "live",
    }


def score_answer(case: dict, answer: dict) -> dict:
    text = answer["answer"].lower()
    trajectory = evaluate_trajectory(
        answer["trajectory"],
        case["expected_tools"],
        ["create_return", "approve_refund", "send_email"],
    )
    denied = any("error" in item for item in answer["evidence"])
    support = []
    for item in answer["evidence"]:
        if "citations" in item:
            support.append(
                bool(item["citations"])
                and any(item["answer"] in c["quote"] for c in item["citations"])
            )
        elif "error" not in item:
            support.append(
                str(item.get("status", "")) in text and item.get("order_id", "") in answer["answer"]
            )
    return {
        "trajectory_exact": trajectory,
        "ownership_contract": denied == case.get("expect_denied", False),
        "keyword_correctness_proxy": all(term.lower() in text for term in case["must_contain"]),
        "exact_evidence_support_proxy": all(support) if support else None,
        "tone_rule_proxy": not any(word in text for word in ("stupid", "idiot", "shut up"))
        and "please" in text,
    }


def local_evaluate(cases: list[dict], settings: Settings, *, version: str = "v2") -> dict:
    if not cases:
        raise ValueError("An empty evaluation cannot pass a release gate.")
    rows = []
    for case in cases:
        answer = support_answer(case["question"], case["customer"], settings, version=version)
        metrics = score_answer(case, answer)
        rows.append(
            {
                "id": case["id"],
                "answer": answer,
                "metrics": metrics,
                "passed": all(value for value in metrics.values() if value is not None),
            }
        )
    return {
        "mode": "scripted-contract" if settings.course_offline else "live",
        "version": version,
        "passed": sum(row["passed"] for row in rows),
        "total": len(rows),
        "limits": (
            "Developer-visible held-out inputs excluded from prompts. "
            "Proxies are not semantic quality or blind generalization scores."
        ),
        "rows": rows,
    }


def load_cases(path: Path | None = None) -> list[dict]:
    path = path or ROOT / "modules/19_evaluation/use_case/eval.jsonl"
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
