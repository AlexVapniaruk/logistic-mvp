from datetime import datetime
from pydantic import BaseModel, Field


class EventReadSchema(BaseModel):
    id: int
    camera_id: str
    action_class: str
    confidence: float
    timestamp: datetime
    frame_path: str | None
    metadata: dict = Field(default_factory=dict)

    model_config = {"from_attributes": True}


class EventCreateSchema(BaseModel):
    camera_id: str
    action_class: str
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime
    frame_path: str | None = None
    metadata: dict = Field(default_factory=dict)


class EventFilterSchema(BaseModel):
    camera_id: str | None = None
    action_class: str | None = None
    from_ts: datetime | None = None
    to_ts: datetime | None = None
    limit: int = Field(50, ge=1, le=500)
    offset: int = Field(0, ge=0)
