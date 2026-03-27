from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.heatmap import (
    HeatmapResponseSchema,
    ZoneAnalyticsSchema,
    ZoneLiveResponseSchema,
    EmployeeAnalyticsSchema,
)
from app.services.analytics.get_heatmap_service import GetHeatmapService
from app.services.analytics.get_zone_analytics_service import GetZoneAnalyticsService
from app.services.analytics.get_live_zone_stats_service import GetLiveZoneStatsService
from app.services.analytics.get_employee_analytics_service import GetEmployeeAnalyticsService

router = APIRouter()


@router.get("/heatmap", response_model=HeatmapResponseSchema)
async def get_heatmap(
    from_ts: datetime | None = None,
    to_ts: datetime | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await GetHeatmapService(db).execute(from_ts, to_ts)


@router.get("/zones/live", response_model=ZoneLiveResponseSchema)
async def get_live_zone_stats(
    window_minutes: int = 5,
    terminal_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await GetLiveZoneStatsService(db).execute(window_minutes, terminal_id)


@router.get("/zones", response_model=list[ZoneAnalyticsSchema])
async def get_zone_analytics(db: AsyncSession = Depends(get_db)):
    return await GetZoneAnalyticsService(db).execute()


@router.get("/employees/{employee_id}", response_model=EmployeeAnalyticsSchema)
async def get_employee_analytics(employee_id: int, db: AsyncSession = Depends(get_db)):
    return await GetEmployeeAnalyticsService(db).execute(employee_id)
