from datetime import datetime
from typing import Literal
from pydantic import BaseModel

TrainingStatus = Literal["pending", "running", "completed", "failed"]


class ModelVersionReadSchema(BaseModel):
    id: int
    name: str
    path: str
    is_active: bool
    created_at: datetime
    metrics: dict

    model_config = {"from_attributes": True}


class TrainingJobReadSchema(BaseModel):
    id: int
    status: TrainingStatus
    model_version_id: int | None
    started_at: datetime
    finished_at: datetime | None
    config: dict
    error: str | None


class StartTrainingSchema(BaseModel):
    config: dict
