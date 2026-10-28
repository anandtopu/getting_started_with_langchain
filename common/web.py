"""Local FastAPI host with authenticated sessions and framed, redacted SSE output."""

import asyncio
import json
from collections.abc import AsyncIterator
from contextlib import aclosing
from pathlib import Path
from typing import Annotated, Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field
from starlette.background import BackgroundTask

from common.config import ROOT, Settings, get_settings
from common.returns import ReturnRequest
from common.security import Principal, authenticate, log_event
from common.service import SupportService


def sse(event: str, data: dict) -> str:
    if event not in {"step", "text", "done", "error"}:
        raise ValueError("Unknown event type.")
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


class ChatInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=4000)


class ReviewInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Literal["approve", "reject"]
    interrupt_id: str = Field(min_length=1, max_length=100)


def create_app(service: SupportService, registry: dict[str, Principal]) -> FastAPI:
    if not registry or any(len(token) < 32 for token in registry):
        raise ValueError("Configure nonempty, distinct bearer tokens of at least 32 characters.")
    app = FastAPI(title="Brightwave support", docs_url=None, redoc_url=None)
    bearer = HTTPBearer(auto_error=False)
    app.state.service = service
    app.state.events = []

    def identity(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    ) -> Principal:
        try:
            return authenticate(credentials.credentials if credentials else "", registry)
        except PermissionError:
            raise HTTPException(401, "Authentication required.") from None

    @app.exception_handler(PermissionError)
    async def denied(request: Request, error: PermissionError) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": "Access denied."})

    @app.exception_handler(ValueError)
    async def invalid(request: Request, error: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": "Request conflict; refresh or start a new conversation."},
        )

    @app.exception_handler(BlockingIOError)
    async def busy(request: Request, error: BlockingIOError) -> JSONResponse:
        return JSONResponse(
            status_code=429, content={"detail": "Busy; retry later."}, headers={"Retry-After": "5"}
        )

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "mode": "offline" if service.settings.course_offline else "live"}

    @app.post("/threads", status_code=201)
    def new_thread(principal: Annotated[Principal, Depends(identity)]) -> dict:
        return {"thread_id": service.new_thread(principal)}

    @app.get("/threads/{thread}")
    def history(thread: str, principal: Annotated[Principal, Depends(identity)]) -> dict:
        return service.session(thread, principal)

    @app.post("/threads/{thread}/messages")
    async def chat(
        thread: str,
        body: ChatInput,
        request: Request,
        principal: Annotated[Principal, Depends(identity)],
    ) -> StreamingResponse:
        service.session(thread, principal)
        slot = service.admission.slot(thread, principal.subject)
        slot.__enter__()
        released = False
        correlation = uuid4().hex

        def release() -> None:
            nonlocal released
            if not released:
                released = True
                slot.__exit__(None, None, None)

        async def events() -> AsyncIterator[str]:
            try:
                async with asyncio.timeout(service.settings.api_request_timeout):
                    async with aclosing(service.chat(thread, principal, body.text)) as source:
                        async for event, data in source:
                            if await request.is_disconnected():
                                return
                            yield sse(event, data)
            except asyncio.CancelledError:
                raise
            except Exception as error:
                app.state.events.append(
                    log_event(
                        "stream_failed",
                        correlation,
                        {"error_type": type(error).__name__},
                        service.settings,
                    )
                )
                app.state.events[:] = app.state.events[-100:]
                yield sse(
                    "error",
                    {
                        "message": "Request stopped. Retry or ask for help.",
                        "request_id": correlation,
                    },
                )
            finally:
                release()

        return StreamingResponse(
            events(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
            background=BackgroundTask(release),
        )

    @app.post("/threads/{thread}/returns")
    def returns(
        thread: str, body: ReturnRequest, principal: Annotated[Principal, Depends(identity)]
    ) -> dict:
        return service.request_return(thread, principal, body)

    @app.get("/reviews/{request_id}")
    def review_state(request_id: str, principal: Annotated[Principal, Depends(identity)]) -> dict:
        return service.review(request_id, principal)

    @app.post("/reviews/{request_id}")
    def review(
        request_id: str, body: ReviewInput, principal: Annotated[Principal, Depends(identity)]
    ) -> dict:
        return service.review(request_id, principal, body.decision, body.interrupt_id)

    return app


def configured_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    customer, manager = (
        settings.api_customer_token.get_secret_value(),
        settings.api_manager_token.get_secret_value(),
    )
    if customer == manager or not settings.api_customer_id.isalnum():
        raise ValueError("Configure distinct customer/reviewer tokens and a valid customer ID.")
    registry = {
        customer: Principal(settings.api_customer_id, "customer"),
        manager: Principal("reviewer", "manager"),
    }
    return create_app(
        SupportService(ROOT / settings.runtime_dir / "support-web", settings), registry
    )


def demo_app(directory: Path) -> FastAPI:
    """Explicit offline test fixture. Demo tokens are never accepted by configured_app."""
    settings = Settings(course_offline=True, model_max_retries=0)
    service = SupportService(directory, settings)
    service.attest("BW1001", "BW-014", inspected=True, proof=True)
    return create_app(
        service,
        {
            "demo-customer-" + "c" * 32: Principal("C001", "customer"),
            "demo-other-" + "o" * 32: Principal("C002", "customer"),
            "demo-reviewer-" + "r" * 32: Principal("reviewer", "manager"),
        },
    )
