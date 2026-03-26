from datetime import datetime
from pydantic import BaseModel


class SensorPositionCreateSchema(BaseModel):
    employee_id: int
    x: float
    y: float
    timestamp: datetime


class SensorPositionReadSchema(BaseModel):
    id: int
    employee_id: int
    x: float
    y: float
    zone_id: int | None
    sector_id: int | None
    timestamp: datetime

    model_config = {"from_attributes": True}
