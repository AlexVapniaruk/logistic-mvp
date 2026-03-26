from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.employee import EmployeeCreateSchema
from app.schemas.terminal import TerminalCreateSchema
from app.schemas.zone import ZoneCreateSchema
from app.schemas.sector import SectorCreateSchema
from app.schemas.sensor_position import SensorPositionCreateSchema
from app.services.terminals.create_terminal_service import CreateTerminalService
from app.services.zones.create_zone_service import CreateZoneService
from app.services.sectors.create_sector_service import CreateSectorService
from app.services.employees.create_employee_service import CreateEmployeeService
from app.services.sensor_positions.create_sensor_position_service import CreateSensorPositionService

SQUARE_ZONE = [[0, 0], [100, 0], [100, 100], [0, 100]]
SQUARE_SECTOR = [[10, 10], [50, 10], [50, 50], [10, 50]]
NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_creates_position_with_zone_resolved(db_session: AsyncSession, mock_redis) -> None:
    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    zone = await CreateZoneService(db_session).execute(
        ZoneCreateSchema(name="Z", points=SQUARE_ZONE, terminal_id=terminal.id)
    )
    employee = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Alice", badge_id="B001", terminal_id=terminal.id)
    )

    payload = SensorPositionCreateSchema(employee_id=employee.id, x=50, y=50, timestamp=NOW)
    result = await CreateSensorPositionService(db_session, mock_redis).execute(payload)

    assert result.zone_id == zone.id
    assert result.employee_id == employee.id
    assert result.x == 50
    assert result.y == 50


@pytest.mark.asyncio
async def test_creates_position_with_sector_resolved(db_session: AsyncSession, mock_redis) -> None:
    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    zone = await CreateZoneService(db_session).execute(
        ZoneCreateSchema(name="Z", points=SQUARE_ZONE, terminal_id=terminal.id)
    )
    sector = await CreateSectorService(db_session).execute(
        SectorCreateSchema(name="S", points=SQUARE_SECTOR, zone_id=zone.id)
    )
    employee = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Bob", badge_id="B002", terminal_id=terminal.id)
    )

    # Point inside sector
    payload = SensorPositionCreateSchema(employee_id=employee.id, x=30, y=30, timestamp=NOW)
    result = await CreateSensorPositionService(db_session, mock_redis).execute(payload)

    assert result.zone_id == zone.id
    assert result.sector_id == sector.id


@pytest.mark.asyncio
async def test_creates_position_outside_zone_sets_null(db_session: AsyncSession, mock_redis) -> None:
    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    await CreateZoneService(db_session).execute(
        ZoneCreateSchema(name="Z", points=SQUARE_ZONE, terminal_id=terminal.id)
    )
    employee = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Carol", badge_id="B003", terminal_id=terminal.id)
    )

    # Point outside zone
    payload = SensorPositionCreateSchema(employee_id=employee.id, x=200, y=200, timestamp=NOW)
    result = await CreateSensorPositionService(db_session, mock_redis).execute(payload)

    assert result.zone_id is None
    assert result.sector_id is None


@pytest.mark.asyncio
async def test_publishes_to_redis(db_session: AsyncSession, mock_redis) -> None:
    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    employee = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Dave", badge_id="B004", terminal_id=terminal.id)
    )

    payload = SensorPositionCreateSchema(employee_id=employee.id, x=5, y=5, timestamp=NOW)
    await CreateSensorPositionService(db_session, mock_redis).execute(payload)

    mock_redis.publish.assert_called_once()
    channel = mock_redis.publish.call_args[0][0]
    assert channel == "positions"
