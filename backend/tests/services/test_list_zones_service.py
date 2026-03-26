import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.terminal import TerminalCreateSchema
from app.schemas.zone import ZoneCreateSchema
from app.services.terminals.create_terminal_service import CreateTerminalService
from app.services.zones.create_zone_service import CreateZoneService
from app.services.zones.list_zones_service import ListZonesService

SQUARE = [[0, 0], [100, 0], [100, 100], [0, 100]]


@pytest.mark.asyncio
async def test_list_zones_returns_only_terminal_zones(db_session: AsyncSession) -> None:
    t1 = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T1"))
    t2 = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T2"))

    await CreateZoneService(db_session).execute(ZoneCreateSchema(name="Z1", points=SQUARE, terminal_id=t1.id))
    await CreateZoneService(db_session).execute(ZoneCreateSchema(name="Z2", points=SQUARE, terminal_id=t1.id))
    await CreateZoneService(db_session).execute(ZoneCreateSchema(name="Z3", points=SQUARE, terminal_id=t2.id))

    result = await ListZonesService(db_session).execute(t1.id)

    assert len(result) == 2
    assert all(z.terminal_id == t1.id for z in result)


@pytest.mark.asyncio
async def test_list_zones_empty_for_unknown_terminal(db_session: AsyncSession) -> None:
    result = await ListZonesService(db_session).execute(terminal_id=999)
    assert result == []
