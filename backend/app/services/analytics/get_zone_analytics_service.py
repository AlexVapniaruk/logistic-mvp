from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_action import EmployeeAction
from app.models.zone import Zone
from app.schemas.heatmap import ZoneAnalyticsSchema


class GetZoneAnalyticsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self) -> list[ZoneAnalyticsSchema]:
        stmt = (
            select(EmployeeAction.zone_id, func.count(EmployeeAction.id))
            .where(EmployeeAction.zone_id.isnot(None))
            .group_by(EmployeeAction.zone_id)
        )
        rows = (await self.db.execute(stmt)).all()
        zone_ids = [r[0] for r in rows]
        zone_names = await self._load_zone_names(zone_ids)
        return [
            ZoneAnalyticsSchema(
                zone_id=zone_id,
                zone_name=zone_names.get(zone_id, str(zone_id)),
                action_count=count,
            )
            for zone_id, count in rows
        ]

    async def _load_zone_names(self, zone_ids: list[int]) -> dict[int, str]:
        if not zone_ids:
            return {}
        result = await self.db.execute(select(Zone).where(Zone.id.in_(zone_ids)))
        return {z.id: z.name for z in result.scalars()}
