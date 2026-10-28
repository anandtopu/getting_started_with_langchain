"""Explicit offline execution and network denial for course tests and smoke scripts."""

import os
import runpy
import socket
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from unittest.mock import patch

_creating_socketpair: ContextVar[bool] = ContextVar("creating_socketpair", default=False)


def deny_network(*args: object, **kwargs: object) -> None:
    """Fail loudly if an offline path accidentally reaches a service."""
    raise RuntimeError("Network disabled in offline mode; use an explicit live run.")


@contextmanager
def offline_environment() -> Iterator[None]:
    """Disable tracing and outbound sockets without changing the user's .env file."""
    original_connect = socket.socket.connect
    original_pair = socket.socketpair

    def connect(sock: socket.socket, address: object) -> None:
        # Windows asyncio uses an internal loopback socket pair for wakeups. Allow only
        # connections created inside socketpair itself, never arbitrary localhost services.
        if (
            _creating_socketpair.get()
            and isinstance(address, tuple)
            and address[0] in {"127.0.0.1", "::1"}
        ):
            return original_connect(sock, address)
        deny_network()

    def socketpair(*args: object, **kwargs: object) -> tuple[socket.socket, socket.socket]:
        token = _creating_socketpair.set(True)
        try:
            return original_pair(*args, **kwargs)
        finally:
            _creating_socketpair.reset(token)

    with (
        patch.dict(os.environ, {"COURSE_OFFLINE": "true", "LANGSMITH_TRACING": "false"}),
        patch.object(socket.socket, "connect", connect),
        patch.object(socket, "socketpair", socketpair),
        patch.object(socket.socket, "connect_ex", deny_network),
        patch.object(socket, "getaddrinfo", deny_network),
        patch.object(socket, "create_connection", deny_network),
    ):
        yield


def execute_script(path: Path, arguments: list[str], *, offline: bool = True) -> None:
    """Execute a smoke target with a normal __main__ guard and explicit argv."""
    with patch.object(sys, "argv", [str(path), *arguments]):
        if offline:
            with offline_environment():
                runpy.run_path(str(path), run_name="__main__")
        else:
            runpy.run_path(str(path), run_name="__main__")
