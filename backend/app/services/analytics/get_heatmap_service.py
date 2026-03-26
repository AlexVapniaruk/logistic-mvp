from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor_position import SensorPosition
from app.models.zone import Zone
from app.models.sector import Sector
from app.schemas.heatmap import HeatmapEntrySchema, HeatmapResponseSchema


class GetHeatmapService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(
        self, from_ts: datetime | None = None, to_ts: datetime | None = None
    ) -> HeatmapResponseSchema:
        zone_counts = await self._count_by_zone(from_ts, to_ts)
        sector_counts = await self._count_by_sector(from_ts, to_ts)
        zone_names = await self._load_zone_names(list(zone_counts.keys()))

        entries = [
            HeatmapEntrySchema(
                zone_id=zone_id,
                zone_name=zone_names.get(zone_id, str(zone_id)),
                count=count,
                sector_breakdown=sector_counts.get(zone_id, {}),
            )
            for zone_id, count in zone_counts.items()
        ]
        return HeatmapResponseSchema(entries=entries, from_ts=from_ts, to_ts=to_ts)

    async def _count_by_zone(
        self, from_ts: datetime | None, to_ts: datetime | None
    ) -> dict[int, int]:
        conditions = [SensorPosition.zone_id.isnot(None)]
        if from_ts:
            conditions.append(SensorPosition.timestamp >= from_ts)
        if to_ts:
            conditions.append(SensorPosition.timestamp <= to_ts)
        stmt = (
            select(SensorPosition.zone_id, func.count(SensorPosition.id))
            .where(*conditions)
            .group_by(SensorPosition.zone_id)
        )
        rows = (await self.db.execute(stmt)).all()
        return {r[0]: r[1] for r in rows}

    async def _count_by_sector(
        self, from_ts: datetime | None, to_ts: datetime | None
    ) -> dict[int, dict[str, int]]:
        conditions = [
            SensorPosition.zone_id.isnot(None),
            SensorPosition.sector_id.isnot(None),
        ]
        if from_ts:
            conditions.append(SensorPosition.timestamp >= from_ts)
        if to_ts:
            conditions.append(SensorPosition.timestamp <= to_ts)
        stmt = (
            select(SensorPosition.zone_id, SensorPosition.sector_id, func.count(SensorPosition.id))
            .where(*conditions)
            .group_by(SensorPosition.zone_id, SensorPosition.sector_id)
        )
        rows = (await self.db.execute(stmt)).all()
        result: dict[int, dict[str, int]] = {}
        for zone_id, sector_id, count in rows:
            result.setdefault(zone_id, {})[str(sector_id)] = count
        return result

    async def _load_zone_names(self, zone_ids: list[int]) -> dict[int, str]:
        if not zone_ids:
            return {}
        result = await self.db.execute(select(Zone).where(Zone.id.in_(zone_ids)))
        return {z.id: z.name for z in result.scalars()}
