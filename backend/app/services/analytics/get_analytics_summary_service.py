from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.analytics import AnalyticsSummarySchema


class GetAnalyticsSummaryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(
        self, from_ts: datetime, to_ts: datetime, camera_id: str | None = None
    ) -> AnalyticsSummarySchema:
        base_filter = [Event.timestamp >= from_ts, Event.timestamp <= to_ts]
        if camera_id:
            base_filter.append(Event.camera_id == camera_id)

        total, avg_conf = await self._aggregate(base_filter)
        by_class = await self._group_by(Event.action_class, base_filter)
        by_camera = await self._group_by(Event.camera_id, base_filter)

        return AnalyticsSummarySchema(
            total_events=total,
            events_by_class=by_class,
            events_by_camera=by_camera,
            avg_confidence=avg_conf,
            period_start=from_ts,
            period_end=to_ts,
        )

    async def _aggregate(self, filters: list) -> tuple[int, float]:
        stmt = select(func.count(Event.id), func.avg(Event.confidence)).where(*filters)
        row = (await self.db.execute(stmt)).one()
        return row[0] or 0, float(row[1] or 0.0)

    async def _group_by(self, column, filters: list) -> dict[str, int]:
        stmt = select(column, func.count(Event.id)).where(*filters).group_by(column)
        rows = (await self.db.execute(stmt)).all()
        return {str(r[0]): r[1] for r in rows}
