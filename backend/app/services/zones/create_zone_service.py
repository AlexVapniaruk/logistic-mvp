from sqlalchemy.ext.asyncio import AsyncSession

from app.models.zone import Zone
from app.schemas.zone import ZoneCreateSchema, ZoneReadSchema


class CreateZoneService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: ZoneCreateSchema) -> ZoneReadSchema:
        zone = Zone(name=payload.name, points=payload.points, terminal_id=payload.terminal_id)
        self.db.add(zone)
        await self.db.commit()
        await self.db.refresh(zone)
        return ZoneReadSchema.model_validate(zone)
