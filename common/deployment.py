"""Explicit service integration helpers; no container, server or database starts on import."""

from typing import Any
from uuid import uuid4

from common.config import Settings


def postgres_probe(settings: Settings) -> dict[str, Any]:
    """Create SDK tables and write one synthetic namespace only after explicit service opt-in."""
    from langgraph.checkpoint.postgres import PostgresSaver
    from langgraph.store.postgres import PostgresStore

    from common.graphs import _studio_builder

    uri = settings.postgres_uri.get_secret_value()
    if settings.course_offline or not uri:
        raise ValueError("Postgres probe needs live service opt-in and POSTGRES_URI.")
    identity = "probe-" + uuid4().hex
    config = {"configurable": {"thread_id": identity}}
    with PostgresSaver.from_conn_string(uri) as saver:
        saver.setup()
        graph = _studio_builder.compile(checkpointer=saver)
        graph.invoke({"request": "refund"}, config)
    with PostgresSaver.from_conn_string(uri) as saver:
        state = _studio_builder.compile(checkpointer=saver).get_state(config).values
    namespace = ("brightwave-course", identity, "preferences")
    with PostgresStore.from_conn_string(uri) as store:
        store.setup()
        store.put(namespace, "shipping", {"method": "standard"})
    with PostgresStore.from_conn_string(uri) as store:
        item = store.get(namespace, "shipping")
        other = store.get(("brightwave-course", "other", "preferences"), "shipping")
        store.delete(namespace, "shipping")
    # This teaching probe retains its synthetic checkpoint for inspection in the disposable DB.
    return {
        "checkpoint_reopened": state["result"] == "Review required",
        "store_reopened": item.value == {"method": "standard"},
        "namespace_isolated": other is None,
    }
