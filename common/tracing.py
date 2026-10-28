"""Optional LangSmith tracing with explicit, scoped credentials and offline protection."""

from collections.abc import Iterator
from contextlib import contextmanager

from langsmith import Client, traceable, tracing_context

from common.config import ConfigurationError, Settings
from common.security import scrub


def sanitized_trace(value: dict, settings: Settings) -> dict:
    """Sanitize before the traceable boundary; disable nested raw-model tracing separately."""
    safe = scrub(value, settings)

    @traceable(name="brightwave_redacted_event", run_type="chain")
    def record(payload: dict) -> dict:
        return {"recorded": payload}

    with tracing_scope(settings):
        return record(
            safe, langsmith_extra={"tags": ["course", "redacted"], "metadata": {"schema": "v1"}}
        )


@contextmanager
def tracing_scope(settings: Settings) -> Iterator[None]:
    """No account, background client or network is needed while tracing is disabled."""
    enabled = settings.langsmith_tracing and not settings.course_offline
    if not enabled:
        with tracing_context(enabled=False):
            yield
        return
    key = settings.langsmith_api_key.get_secret_value()
    if not key:
        raise ConfigurationError("Tracing is enabled; set LANGSMITH_API_KEY or turn tracing off.")
    client = Client(api_key=key, api_url=settings.langsmith_endpoint)
    try:
        with tracing_context(enabled=True, client=client, project_name=settings.langsmith_project):
            yield
        client.flush()
    finally:
        client.close()
