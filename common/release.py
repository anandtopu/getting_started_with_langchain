"""Repeatable local HTTP acceptance checks and explicit evaluation thresholds."""

from pathlib import Path

CUSTOMER = "demo-customer-" + "c" * 32
OTHER = "demo-other-" + "o" * 32
REVIEWER = "demo-reviewer-" + "r" * 32


def headers(token: str = CUSTOMER) -> dict[str, str]:
    return {"Authorization": "Bearer " + token}


def api_contract(directory: Path, decision: str = "approve") -> dict:
    from fastapi.testclient import TestClient

    from common.web import demo_app

    with TestClient(demo_app(directory)) as client:
        unauthorized = client.post("/threads").status_code
        thread = client.post("/threads", headers=headers()).json()["thread_id"]
        path = f"/threads/{thread}"
        isolated = client.get(path, headers=headers(OTHER)).status_code
        streamed = client.post(path + "/messages", headers=headers(), json={"text": "BW1001"})
        request = client.post(
            path + "/returns",
            headers=headers(),
            json={
                "order_id": "BW1001",
                "sku": "BW-014",
                "reason": "unused",
                "idempotency_key": "release-" + thread,
            },
        ).json()
        review_path = "/reviews/" + thread
        payload = {"decision": decision, "interrupt_id": request["interrupt_id"]}
        forbidden = client.post(review_path, headers=headers(), json=payload).status_code
        result = client.post(review_path, headers=headers(REVIEWER), json=payload)
        duplicate = client.post(review_path, headers=headers(REVIEWER), json=payload).status_code
        return {
            "authentication": unauthorized == 401,
            "isolation": isolated == 403,
            "stream_completed": "event: done" in streamed.text,
            "reviewer_required": forbidden == 403,
            "paused_before_write": request["pending"],
            "review_completed": result.status_code == 200 and not result.json()["pending"],
            "duplicate_rejected": duplicate == 409,
            "result": result.json(),
        }


def evaluation_gate(report: dict, minimum_correctness: float = 1.0) -> bool:
    """Default release blocks known answer misses; thresholds must be chosen before a run."""
    rows = report["rows"]
    if not rows or not 0 <= minimum_correctness <= 1:
        return False
    safety = all(
        row["metrics"]["ownership_contract"] and row["metrics"]["trajectory_exact"] for row in rows
    )
    grounding_and_tone = all(
        row["metrics"].get("tone_rule_proxy") is True
        and "exact_evidence_support_proxy" in row["metrics"]
        and (
            row["metrics"]["exact_evidence_support_proxy"] is True
            or row["metrics"]["exact_evidence_support_proxy"] is None
        )
        for row in rows
    )
    correctness = sum(row["metrics"]["keyword_correctness_proxy"] for row in rows) / len(rows)
    return safety and grounding_and_tone and correctness >= minimum_correctness
