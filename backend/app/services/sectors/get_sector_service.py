from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sector import Sector
from app.schemas.sector import SectorReadSchema


class GetSectorService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, sector_id: int) -> SectorReadSchema:
        result = await self.db.execute(select(Sector).where(Sector.id == sector_id))
        sector = result.scalar_one_or_none()
        if sector is None:
            raise HTTPException(status_code=404, detail="Sector not found")
        return SectorReadSchema.model_validate(sector)
