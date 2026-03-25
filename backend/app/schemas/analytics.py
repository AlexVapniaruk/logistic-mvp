from datetime import datetime
from pydantic import BaseModel


class AnalyticsSummarySchema(BaseModel):
    total_events: int
    events_by_class: dict[str, int]
    events_by_camera: dict[str, int]
    avg_confidence: float
    period_start: datetime
    period_end: datetime
