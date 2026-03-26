from datetime import datetime
from pydantic import BaseModel


class EmployeeActionReadSchema(BaseModel):
    id: int
    employee_id: int
    zone_id: int
    sector_id: int | None
    action_type: str
    confidence: float
    source_event_id: int | None
    timestamp: datetime

    model_config = {"from_attributes": True}
