from datetime import datetime
from pydantic import BaseModel, Field


class CameraEventCreateSchema(BaseModel):
    camera_id: int
    timestamp: datetime
    action_type: str
    confidence: float = Field(ge=0.0, le=1.0)
    bounding_box: list[float] | None = None
    video_clip_url: str | None = None


class CameraEventFilterSchema(BaseModel):
    needs_annotation: bool | None = None
    camera_id: int | None = None
    limit: int = Field(50, ge=1, le=500)
    offset: int = Field(0, ge=0)


class CameraEventReadSchema(BaseModel):
    id: int
    camera_id: int
    timestamp: datetime
    action_type: str
    confidence: float
    bounding_box: list[float] | None
    video_clip_url: str | None
    needs_annotation: bool
    employee_action_id: int | None

    model_config = {"from_attributes": True}
