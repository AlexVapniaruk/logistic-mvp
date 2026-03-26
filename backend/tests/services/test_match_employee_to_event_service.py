from datetime import datetime, timedelta, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_event import CameraEvent
from app.schemas.employee import EmployeeCreateSchema
from app.schemas.terminal import TerminalCreateSchema
from app.schemas.zone import ZoneCreateSchema
from app.schemas.camera import CameraCreateSchema
from app.models.sensor_position import SensorPosition
from app.services.terminals.create_terminal_service import CreateTerminalService
from app.services.zones.create_zone_service import CreateZoneService
from app.services.cameras.create_camera_service import CreateCameraService
from app.services.employees.create_employee_service import CreateEmployeeService
from app.services.matching.match_employee_to_event_service import MatchEmployeeToEventService

SQUARE = [[0, 0], [100, 0], [100, 100], [0, 100]]
BASE_TS = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


async def _setup(db):
    terminal = await CreateTerminalService(db).execute(TerminalCreateSchema(name="T"))
    zone = await CreateZoneService(db).execute(
        ZoneCreateSchema(name="Z", points=SQUARE, terminal_id=terminal.id)
    )
    camera = await CreateCameraService(db).execute(
        CameraCreateSchema(name="C", stream_url="rtsp://x", terminal_id=terminal.id, zone_id=zone.id)
    )
    employee = await CreateEmployeeService(db).execute(
        EmployeeCreateSchema(name="Alice", badge_id="B001", terminal_id=terminal.id)
    )
    return terminal, zone, camera, employee


@pytest.mark.asyncio
async def test_returns_employee_when_position_in_window(db_session: AsyncSession) -> None:
    terminal, zone, camera, employee = await _setup(db_session)

    pos = SensorPosition(
        employee_id=employee.id, x=50, y=50,
        zone_id=zone.id, sector_id=None,
        timestamp=BASE_TS,
    )
    db_session.add(pos)
    await db_session.commit()

    event = CameraEvent(
        camera_id=camera.id, timestamp=BASE_TS,
        action_type="picking", confidence=0.9,
        needs_annotation=False,
    )
    db_session.add(event)
    await db_session.commit()

    result = await MatchEmployeeToEventService(db_session).execute(event)
    assert result is not None
    assert result.id == employee.id


@pytest.mark.asyncio
async def test_returns_none_when_no_positions_in_window(db_session: AsyncSession) -> None:
    terminal, zone, camera, employee = await _setup(db_session)

    # Position is 10 seconds away — outside ±2s window
    pos = SensorPosition(
        employee_id=employee.id, x=50, y=50,
        zone_id=zone.id, sector_id=None,
        timestamp=BASE_TS - timedelta(seconds=10),
    )
    db_session.add(pos)
    await db_session.commit()

    event = CameraEvent(
        camera_id=camera.id, timestamp=BASE_TS,
        action_type="picking", confidence=0.9,
        needs_annotation=False,
    )
    db_session.add(event)
    await db_session.commit()

    result = await MatchEmployeeToEventService(db_session).execute(event)
    assert result is None


@pytest.mark.asyncio
async def test_returns_closest_employee_when_multiple_positions(db_session: AsyncSession) -> None:
    terminal, zone, camera, employee = await _setup(db_session)
    employee2 = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Bob", badge_id="B002", terminal_id=terminal.id)
    )

    # employee1 is 1s away, employee2 is 2s away
    pos1 = SensorPosition(
        employee_id=employee.id, x=50, y=50,
        zone_id=zone.id, sector_id=None,
        timestamp=BASE_TS - timedelta(seconds=1),
    )
    pos2 = SensorPosition(
        employee_id=employee2.id, x=60, y=60,
        zone_id=zone.id, sector_id=None,
        timestamp=BASE_TS - timedelta(seconds=2),
    )
    db_session.add_all([pos1, pos2])
    await db_session.commit()

    event = CameraEvent(
        camera_id=camera.id, timestamp=BASE_TS,
        action_type="picking", confidence=0.9,
        needs_annotation=False,
    )
    db_session.add(event)
    await db_session.commit()

    result = await MatchEmployeeToEventService(db_session).execute(event)
    assert result is not None
    assert result.id == employee.id  # closer (1s vs 2s)
