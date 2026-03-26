from datetime import datetime
from pydantic import BaseModel


class HeatmapEntrySchema(BaseModel):
    zone_id: int
    zone_name: str
    count: int
    sector_breakdown: dict[str, int]


class HeatmapResponseSchema(BaseModel):
    entries: list[HeatmapEntrySchema]
    from_ts: datetime | None
    to_ts: datetime | None


class ZoneAnalyticsSchema(BaseModel):
    zone_id: int
    zone_name: str
    action_count: int


class EmployeeAnalyticsSchema(BaseModel):
    employee_id: int
    action_counts: dict[str, int]
    total: int
