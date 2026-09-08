from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from app.config import (
    DEFAULT_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
    MIN_DURATION_SECONDS,
)


class AffectiveState(BaseModel):
    arousal: float = Field(..., ge=0.0, le=1.0)
    valence: float = Field(..., ge=0.0, le=1.0)
    stress: float = Field(..., ge=0.0, le=1.0)
    engagement: float = Field(..., ge=0.0, le=1.0)


class GenerateRequest(BaseModel):
    session_name: str | None = Field(default=None, max_length=120)
    duration_seconds: int = Field(
        default=DEFAULT_DURATION_SECONDS,
        ge=MIN_DURATION_SECONDS,
        le=MAX_DURATION_SECONDS,
    )
    seed: int | None = None
    current_state: AffectiveState
    target_state: AffectiveState


class MusicalParameters(BaseModel):
    bpm: float
    mode: str
    note_density: float
    brightness: float
    volume: float
    rhythmic_complexity: float
    pad_intensity: float
    melody_activity: float

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, value: str) -> str:
        allowed = {"major", "minor", "dorian", "lydian"}
        if value not in allowed:
            raise ValueError(f"mode must be one of {sorted(allowed)}")
        return value


class SessionMetadata(BaseModel):
    input_state: dict[str, Any]
    target_state: dict[str, Any]
    raw_parameters: dict[str, Any]
    safe_parameters: dict[str, Any]
    safety_actions: list[str]
    generation_notes: list[str]
    technical_details: dict[str, Any]


class GenerateResponse(BaseModel):
    session_id: str
    audio_url: str
    metadata: SessionMetadata


class SessionRecord(BaseModel):
    session_id: str
    timestamp: datetime
    session_name: str | None
    input_state: dict[str, Any]
    target_state: dict[str, Any]
    raw_parameters: dict[str, Any]
    safe_parameters: dict[str, Any]
    safety_actions: list[str]
    generation_notes: list[str]
    technical_details: dict[str, Any]
    output_wav_path: str


class SessionSummary(BaseModel):
    session_id: str
    timestamp: datetime
    session_name: str | None
    output_wav_path: str


def generate_session_id() -> str:
    return uuid4().hex
