from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sector import Sector
from app.schemas.sector import SectorCreateSchema, SectorReadSchema


class CreateSectorService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: SectorCreateSchema) -> SectorReadSchema:
        sector = Sector(name=payload.name, points=payload.points, zone_id=payload.zone_id)
        self.db.add(sector)
        await self.db.commit()
        await self.db.refresh(sector)
        return SectorReadSchema.model_validate(sector)
