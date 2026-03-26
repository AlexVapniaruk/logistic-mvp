from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.sector import SectorReadSchema
from app.services.sectors.get_sector_service import GetSectorService

router = APIRouter()


@router.get("/{sector_id}", response_model=SectorReadSchema)
async def get_sector(sector_id: int, db: AsyncSession = Depends(get_db)):
    return await GetSectorService(db).execute(sector_id)
