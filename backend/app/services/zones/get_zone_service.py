from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.zone import Zone
from app.schemas.zone import ZoneReadSchema


class GetZoneService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, zone_id: int) -> ZoneReadSchema:
        result = await self.db.execute(select(Zone).where(Zone.id == zone_id))
        zone = result.scalar_one_or_none()
        if zone is None:
            raise HTTPException(status_code=404, detail="Zone not found")
        return ZoneReadSchema.model_validate(zone)
