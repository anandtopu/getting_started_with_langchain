"""Optional LangSmith tracing with explicit, scoped credentials and offline protection."""

from collections.abc import Iterator
from contextlib import contextmanager

from langsmith import Client, tracing_context

from common.config import ConfigurationError, Settings


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
