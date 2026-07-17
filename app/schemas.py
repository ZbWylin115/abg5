"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class GenerateResult(BaseModel):
    opening_line: str | None = None
    follow_up: str | None = None
    topics: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)
    date_idea: str | None = None
    cultural_context: dict | None = None
