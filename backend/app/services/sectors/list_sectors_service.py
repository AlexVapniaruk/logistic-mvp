from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sector import Sector
from app.schemas.sector import SectorReadSchema


class ListSectorsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, zone_id: int) -> list[SectorReadSchema]:
        result = await self.db.execute(
            select(Sector).where(Sector.zone_id == zone_id).order_by(Sector.id)
        )
        return [SectorReadSchema.model_validate(row) for row in result.scalars()]
