from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.terminal import TerminalCreateSchema, TerminalReadSchema
from app.schemas.zone import ZoneBodySchema, ZoneCreateSchema, ZoneReadSchema
from app.schemas.sector import SectorBodySchema, SectorCreateSchema, SectorReadSchema
from app.services.terminals.create_terminal_service import CreateTerminalService
from app.services.terminals.get_terminal_service import GetTerminalService
from app.services.terminals.list_terminals_service import ListTerminalsService
from app.services.zones.create_zone_service import CreateZoneService
from app.services.zones.list_zones_service import ListZonesService
from app.services.sectors.create_sector_service import CreateSectorService
from app.services.sectors.list_sectors_service import ListSectorsService

router = APIRouter()


@router.get("/", response_model=list[TerminalReadSchema])
async def list_terminals(db: AsyncSession = Depends(get_db)):
    return await ListTerminalsService(db).execute()


@router.post("/", response_model=TerminalReadSchema, status_code=201)
async def create_terminal(payload: TerminalCreateSchema, db: AsyncSession = Depends(get_db)):
    return await CreateTerminalService(db).execute(payload)


@router.get("/{terminal_id}", response_model=TerminalReadSchema)
async def get_terminal(terminal_id: int, db: AsyncSession = Depends(get_db)):
    return await GetTerminalService(db).execute(terminal_id)


@router.get("/{terminal_id}/zones/", response_model=list[ZoneReadSchema])
async def list_zones(terminal_id: int, db: AsyncSession = Depends(get_db)):
    return await ListZonesService(db).execute(terminal_id)


@router.post("/{terminal_id}/zones/", response_model=ZoneReadSchema, status_code=201)
async def create_zone(
    terminal_id: int, payload: ZoneBodySchema, db: AsyncSession = Depends(get_db)
):
    schema = ZoneCreateSchema(name=payload.name, points=payload.points, terminal_id=terminal_id)
    return await CreateZoneService(db).execute(schema)


@router.get("/{terminal_id}/zones/{zone_id}/sectors/", response_model=list[SectorReadSchema])
async def list_sectors_for_zone(
    terminal_id: int, zone_id: int, db: AsyncSession = Depends(get_db)
):
    return await ListSectorsService(db).execute(zone_id)


@router.post(
    "/{terminal_id}/zones/{zone_id}/sectors/",
    response_model=SectorReadSchema,
    status_code=201,
)
async def create_sector_for_zone(
    terminal_id: int, zone_id: int, payload: SectorBodySchema, db: AsyncSession = Depends(get_db)
):
    schema = SectorCreateSchema(name=payload.name, points=payload.points, zone_id=zone_id)
    return await CreateSectorService(db).execute(schema)
