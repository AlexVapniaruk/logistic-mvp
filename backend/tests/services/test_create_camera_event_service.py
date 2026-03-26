from datetime import datetime, timezone
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_action import EmployeeAction
from app.schemas.camera_event import CameraEventCreateSchema
from app.schemas.camera import CameraCreateSchema
from app.schemas.employee import EmployeeCreateSchema
from app.schemas.terminal import TerminalCreateSchema
from app.schemas.zone import ZoneCreateSchema
from app.services.cameras.create_camera_service import CreateCameraService
from app.services.camera_events.create_camera_event_service import CreateCameraEventService
from app.services.employees.create_employee_service import CreateEmployeeService
from app.services.terminals.create_terminal_service import CreateTerminalService
from app.services.zones.create_zone_service import CreateZoneService

SQUARE = [[0, 0], [100, 0], [100, 100], [0, 100]]
NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_high_confidence_triggers_processing(db_session: AsyncSession) -> None:
    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    zone = await CreateZoneService(db_session).execute(
        ZoneCreateSchema(name="Z", points=SQUARE, terminal_id=terminal.id)
    )
    camera = await CreateCameraService(db_session).execute(
        CameraCreateSchema(name="C", stream_url="rtsp://x", terminal_id=terminal.id, zone_id=zone.id)
    )
    payload = CameraEventCreateSchema(
        camera_id=camera.id, timestamp=NOW, action_type="picking", confidence=0.9
    )
    result = await CreateCameraEventService(db_session).execute(payload)

    # No employee in zone → needs_annotation=True (ProcessCameraEventService found no match)
    assert result.needs_annotation is True
    assert result.confidence == 0.9


@pytest.mark.asyncio
async def test_low_confidence_sets_needs_annotation(db_session: AsyncSession) -> None:
    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    camera = await CreateCameraService(db_session).execute(
        CameraCreateSchema(name="C", stream_url="rtsp://x", terminal_id=terminal.id)
    )
    payload = CameraEventCreateSchema(
        camera_id=camera.id, timestamp=NOW, action_type="idle", confidence=0.5
    )
    result = await CreateCameraEventService(db_session).execute(payload)

    assert result.needs_annotation is True
    assert result.employee_action_id is None


@pytest.mark.asyncio
async def test_high_confidence_with_matching_employee_creates_action(
    db_session: AsyncSession,
) -> None:
    from datetime import timedelta
    from app.models.sensor_position import SensorPosition

    terminal = await CreateTerminalService(db_session).execute(TerminalCreateSchema(name="T"))
    zone = await CreateZoneService(db_session).execute(
        ZoneCreateSchema(name="Z", points=SQUARE, terminal_id=terminal.id)
    )
    camera = await CreateCameraService(db_session).execute(
        CameraCreateSchema(name="C", stream_url="rtsp://x", terminal_id=terminal.id, zone_id=zone.id)
    )
    employee = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Alice", badge_id="B001", terminal_id=terminal.id)
    )
    # Place employee in zone at event time
    pos = SensorPosition(
        employee_id=employee.id, x=50, y=50,
        zone_id=zone.id, sector_id=None, timestamp=NOW,
    )
    db_session.add(pos)
    await db_session.commit()

    payload = CameraEventCreateSchema(
        camera_id=camera.id, timestamp=NOW, action_type="picking", confidence=0.9
    )
    result = await CreateCameraEventService(db_session).execute(payload)

    assert result.needs_annotation is False
    assert result.employee_action_id is not None

    actions = (await db_session.execute(select(EmployeeAction))).scalars().all()
    assert len(actions) == 1
    assert actions[0].employee_id == employee.id
