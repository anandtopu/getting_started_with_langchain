"""Pydantic data contracts introduced in module 03."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Category(StrEnum):
    SHIPPING = "shipping"
    RETURNS = "returns"
    WARRANTY = "warranty"
    PRODUCT = "product"
    PRIVACY = "privacy"


class TicketTriage(BaseModel):
    """Extract only facts in the ticket; absent identifiers must be null."""

    model_config = ConfigDict(extra="forbid")
    category: Category
    priority: Literal["low", "medium", "high"]
    sentiment: Literal["positive", "neutral", "negative"]
    order_id: str | None = Field(pattern=r"^BW\d{4}$")
    sku: str | None = Field(pattern=r"^BW-\d{3}$")


class TriageEnvelope(BaseModel):
    """Nested contract: the extraction plus a short evidence quote."""

    triage: TicketTriage
    evidence: str = Field(min_length=1, max_length=160)
