"""Bounded review map-reduce with measured evidence and a deterministic publication gate."""

import operator
from collections import defaultdict
from typing import Annotated, Any, Literal, NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field

from common.config import Settings
from common.data import load_csv
from common.fixtures import structured_fixture
from common.models import get_chat_model


def review_groups() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in load_csv("reviews.csv"):
        groups[row["category"]].append(row)
    return dict(sorted(groups.items()))


def category_facts(category: str, rows: list[dict]) -> dict:
    if not rows or any(row["category"] != category for row in rows):
        raise ValueError("Use a nonempty group containing only the named category.")
    ratings = [int(row["rating"]) for row in rows]
    if any(not 1 <= rating <= 5 for rating in ratings):
        raise ValueError("Ratings must be 1 through 5.")
    return {
        "category": category,
        "count": len(rows),
        "mean_rating": round(sum(ratings) / len(rows), 2),
        "source": "data/reviews.csv",
        "sample_ids": [row["review_id"] for row in rows[:2]],
    }


class ReviewState(TypedDict):
    categories: list[str]
    sections: Annotated[list[dict], operator.add]
    attempt: int
    report: NotRequired[str]
    feedback: NotRequired[str]
    accepted: NotRequired[bool]
    model_calls: Annotated[int, operator.add]


class WorkerState(TypedDict):
    category: str


class Assessment(BaseModel):
    approved: bool
    feedback: str = Field(max_length=500)


def report_gate(report: str, categories: list[str]) -> bool:
    """A structural gate, not a semantic factuality evaluator."""
    return (
        bool(categories)
        and "data/reviews.csv" in report
        and all(f"## {category}\n" in report for category in categories)
    )


def build_review_graph(settings: Settings, *, max_attempts: int = 2) -> Any:
    if not 1 <= max_attempts <= 3:
        raise ValueError("Choose one to three report attempts.")
    groups = review_groups()

    def dispatch(state: ReviewState) -> list[Send]:
        if state["attempt"] != 0 or state["sections"] or state["model_calls"] != 0:
            raise ValueError("Start a report with empty results and zero counters.")
        categories = state["categories"]
        if not categories or len(categories) > 6 or len(set(categories)) != len(categories):
            raise ValueError("Choose one to six unique categories.")
        if set(categories) - groups.keys():
            raise ValueError("Unknown review category.")
        return [Send("worker", {"category": category}) for category in categories]

    def worker(state: WorkerState) -> dict:
        facts = category_facts(state["category"], groups[state["category"]])
        # All numeric evidence is calculated in Python, never guessed by the model.
        summary = get_chat_model(
            settings=settings, responses=["Inspect clearer setup guidance."]
        ).invoke(
            f"Suggest one cautious action from this synthetic review sample. Facts: {facts}. "
            f"Two sample reviews: {[row['text'] for row in groups[state['category']][:2]]}"
        )
        return {"sections": [{**facts, "suggestion": str(summary.content)}], "model_calls": 1}

    def draft(state: ReviewState) -> dict:
        sections = sorted(state["sections"], key=lambda item: item["category"])
        fixture = "Synthetic review report\n" + "\n".join(
            f"## {s['category']}\nCount {s['count']}; mean {s['mean_rating']}; "
            f"{s['suggestion']} [data/reviews.csv: {', '.join(s['sample_ids'])}]"
            for s in sections
        )
        # First fixture intentionally fails the gate, so improvement executes in tests.
        response = "Incomplete synthetic draft" if state["attempt"] == 0 else fixture
        report = get_chat_model(settings=settings, responses=[response]).invoke(
            f"Write a synthetic review report. Use an exact ## category heading for each category, "
            f"then newline. Cite data/reviews.csv. Evidence: {sections}. "
            f"Previous feedback: {state.get('feedback', '')}. Do not invent market statistics."
        )
        return {"report": str(report.content), "attempt": state["attempt"] + 1, "model_calls": 1}

    def evaluate(state: ReviewState) -> dict:
        gate = report_gate(state["report"], state["categories"])
        values = {
            "approved": gate,
            "feedback": "Ready" if gate else "Include every category and source.",
        }
        assessment = (
            get_chat_model(settings=settings, responses=[structured_fixture(Assessment, values)])
            .with_structured_output(Assessment)
            .invoke(
                "Check category coverage, source citations and cautious synthetic-data wording. "
                + state["report"]
            )
        )
        return {
            "accepted": gate and assessment.approved,
            "feedback": assessment.feedback,
            "model_calls": 1,
        }

    def route(state: ReviewState) -> Literal["draft", "__end__"]:
        return END if state["accepted"] or state["attempt"] >= max_attempts else "draft"

    graph = StateGraph(ReviewState)
    for name, node in (("worker", worker), ("draft", draft), ("evaluate", evaluate)):
        graph.add_node(name, node)
    graph.add_conditional_edges(START, dispatch, ["worker"])
    graph.add_edge("worker", "draft")
    graph.add_edge("draft", "evaluate")
    graph.add_conditional_edges("evaluate", route)
    return graph.compile()
