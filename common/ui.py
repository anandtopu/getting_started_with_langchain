"""Streamlit UI: credentials remain in the local session; the API checks every action."""

import json
from typing import Any

import httpx
import streamlit as st

from common.config import get_settings


def render(client: Any = None) -> None:
    st.title("Brightwave support")
    st.caption("Synthetic course data. Refund records and notifications are local demonstrations.")
    token = st.text_input("Customer access token", type="password", key="customer_token")
    if st.session_state.get("identity_token") != token:
        st.session_state.update(identity_token=token, thread_id=None, conversation=[])
        st.session_state.pop("review_state", None)
        st.session_state.pop("manager_review", None)
    if not token:
        st.info("Enter the customer token configured by the local API operator.")
        return
    owned = client is None
    client = client or httpx.Client(base_url=get_settings().api_base_url, timeout=60)

    def call(
        method: str, path: str, *, reviewer: bool = False, payload: dict | None = None
    ) -> dict:
        selected = st.session_state.get("reviewer_token", "") if reviewer else token
        response = client.request(
            method, path, headers={"Authorization": "Bearer " + selected}, json=payload
        )
        response.raise_for_status()
        return response.json()

    try:
        if st.button("New conversation") or not st.session_state.get("thread_id"):
            st.session_state.thread_id = call("POST", "/threads")["thread_id"]
            st.session_state.conversation = []
            st.session_state.pop("review_state", None)
        thread = st.session_state.thread_id
        for entry in st.session_state.conversation:
            with st.chat_message(entry["role"]):
                st.markdown(entry["content"])
        if text := st.chat_input("How can we help?"):
            st.session_state.conversation.append({"role": "user", "content": text})
            with st.chat_message("user"):
                st.write(text)

            def chunks() -> Any:
                with client.stream(
                    "POST",
                    f"/threads/{thread}/messages",
                    headers={"Authorization": "Bearer " + token},
                    json={"text": text},
                ) as response:
                    response.raise_for_status()
                    event = ""
                    for line in response.iter_lines():
                        if line.startswith("event: "):
                            event = line[7:]
                        elif line.startswith("data: "):
                            item = json.loads(line[6:])
                            if event == "text":
                                yield item["text"]
                            elif event == "error":
                                yield item["message"]

            with st.chat_message("assistant"):
                answer = st.write_stream(chunks())
            st.session_state.conversation.append({"role": "assistant", "content": str(answer)})
        with st.expander("Request a return"):
            order = st.text_input("Order", value="BW1001")
            sku = st.text_input("Product SKU", value="BW-014")
            if st.button("Check return eligibility"):
                result = call(
                    "POST",
                    f"/threads/{thread}/returns",
                    payload={
                        "order_id": order,
                        "sku": sku,
                        "reason": "unused",
                        "idempotency_key": "web-" + thread,
                    },
                )
                st.session_state.review_state = result
            if state := st.session_state.get("review_state"):
                st.write(state["status"])
                st.write("Review reference: " + state["request_id"])
        with st.expander("Reviewer controls"):
            st.text_input("Reviewer access token", type="password", key="reviewer_token")
            reviewer_token = st.session_state.get("reviewer_token", "")
            if st.session_state.get("reviewer_identity") != reviewer_token:
                st.session_state.pop("manager_review", None)
                st.session_state.reviewer_identity = reviewer_token
            review_id = st.text_input("Review reference", value=thread)
            if st.button("Load review"):
                st.session_state.manager_review = call(
                    "GET", f"/reviews/{review_id}", reviewer=True
                )
            view = st.session_state.get("manager_review")
            if view and view["request_id"] == review_id and view["pending"]:
                st.json(view["review"])
                for label, decision in [("Approve", "approve"), ("Reject", "reject")]:
                    if st.button(label):
                        result = call(
                            "POST",
                            f"/reviews/{review_id}",
                            reviewer=True,
                            payload={"decision": decision, "interrupt_id": view["interrupt_id"]},
                        )
                        st.session_state.manager_review = result
                        st.success(result["status"])
            elif view and view["request_id"] == review_id:
                st.info("This review is no longer pending.")
    except (httpx.HTTPError, ValueError):
        st.error("Request could not be completed. Check access, refresh the review, or try later.")
    finally:
        if owned:
            client.close()
