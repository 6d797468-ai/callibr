from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TrainingIntent = Literal["yes", "maybe", "no"]


class SimulationFeedback(BaseModel):
    session_id: str = Field(min_length=1)
    tenant_id: str = Field(default="tenant_demo")
    learner_id: str = Field(default="learner_demo")
    satisfaction: int = Field(ge=1, le=5)
    perceived_realism: int = Field(ge=1, le=5)
    difficulty: int = Field(ge=1, le=5)
    usefulness: int = Field(ge=1, le=5)
    would_use_for_training: TrainingIntent
    free_text: str = ""
    submitted_at: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )
