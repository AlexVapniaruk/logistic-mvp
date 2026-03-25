from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.analytics import AnalyticsSummarySchema
from app.services.analytics.get_analytics_summary_service import GetAnalyticsSummaryService

router = APIRouter()


@router.get("/summary", response_model=AnalyticsSummarySchema)
async def get_summary(
    from_ts: datetime = Query(...),
    to_ts: datetime = Query(...),
    camera_id: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await GetAnalyticsSummaryService(db).execute(from_ts, to_ts, camera_id)
