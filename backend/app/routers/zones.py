from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.zone import ZoneReadSchema
from app.schemas.sector import SectorBodySchema, SectorCreateSchema, SectorReadSchema
from app.services.zones.get_zone_service import GetZoneService
from app.services.sectors.create_sector_service import CreateSectorService
from app.services.sectors.list_sectors_service import ListSectorsService

router = APIRouter()


@router.get("/{zone_id}", response_model=ZoneReadSchema)
async def get_zone(zone_id: int, db: AsyncSession = Depends(get_db)):
    return await GetZoneService(db).execute(zone_id)


@router.get("/{zone_id}/sectors/", response_model=list[SectorReadSchema])
async def list_sectors(zone_id: int, db: AsyncSession = Depends(get_db)):
    return await ListSectorsService(db).execute(zone_id)


@router.post("/{zone_id}/sectors/", response_model=SectorReadSchema, status_code=201)
async def create_sector(
    zone_id: int, payload: SectorBodySchema, db: AsyncSession = Depends(get_db)
):
    schema = SectorCreateSchema(name=payload.name, points=payload.points, zone_id=zone_id)
    return await CreateSectorService(db).execute(schema)
