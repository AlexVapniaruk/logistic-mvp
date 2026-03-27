from datetime import datetime
from pydantic import BaseModel, ConfigDict


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


class ActiveEmployeeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employee_id: int
    employee_name: str
    last_seen: datetime
    last_x: float
    last_y: float


class ZoneLiveStatsSchema(BaseModel):
    zone_id: int
    zone_name: str
    active_employee_count: int
    last_activity_at: datetime | None
    active_employees: list[ActiveEmployeeSchema]
    action_counts: dict[str, int]


class ZoneLiveResponseSchema(BaseModel):
    generated_at: datetime
    window_minutes: int
    zones: list[ZoneLiveStatsSchema]
