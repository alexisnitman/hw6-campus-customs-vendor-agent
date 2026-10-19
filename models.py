from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class VendorDecision(BaseModel):
    vendor: str
    sku: str
    unit_price: float = Field(ge=0)
    lead_time_days: int = Field(ge=0)
    minimum_order: int = Field(ge=0)
    decision: Literal["recommend", "do_not_recommend"]
    reason: str = Field(min_length=1)


class AuditEntry(BaseModel):
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event: Literal["tool_call", "final_answer"]
    tool_name: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    short_result: str = ""
    answer: VendorDecision | None = None


class UsageLog(BaseModel):
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    document: str
    model: str
    setup: str = "single"
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cache_write_tokens: int = 0
    cache_read_tokens: int = 0
    cost_dollars: float = 0.0
