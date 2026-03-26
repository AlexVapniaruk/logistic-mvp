from datetime import datetime
from pydantic import BaseModel


class AnnotationCreateSchema(BaseModel):
    camera_event_id: int
    annotator_id: str
    action_type: str
    notes: str | None = None


class AnnotationReadSchema(BaseModel):
    id: int
    camera_event_id: int
    annotator_id: str
    action_type: str
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
