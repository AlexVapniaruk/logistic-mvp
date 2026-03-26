from datetime import datetime, timezone
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_event import CameraEvent
from app.models.employee_action import EmployeeAction
from app.schemas.annotation import AnnotationCreateSchema
from app.schemas.camera import CameraCreateSchema
from app.schemas.employee import EmployeeCreateSchema
from app.schemas.terminal import TerminalCreateSchema
from app.schemas.zone import ZoneCreateSchema
from app.services.cameras.create_camera_service import CreateCameraService
from app.services.employees.create_employee_service import CreateEmployeeService
from app.services.annotations.create_annotation_service import CreateAnnotationService
from app.services.terminals.create_terminal_service import CreateTerminalService
from app.services.zones.create_zone_service import CreateZoneService

SQUARE = [[0, 0], [100, 0], [100, 100], [0, 100]]
NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


async def _create_queued_event(db):
    terminal = await CreateTerminalService(db).execute(TerminalCreateSchema(name="T"))
    zone = await CreateZoneService(db).execute(
        ZoneCreateSchema(name="Z", points=SQUARE, terminal_id=terminal.id)
    )
    camera = await CreateCameraService(db).execute(
        CameraCreateSchema(name="C", stream_url="rtsp://x", terminal_id=terminal.id, zone_id=zone.id)
    )
    event = CameraEvent(
        camera_id=camera.id, timestamp=NOW,
        action_type="unknown", confidence=0.5,
        needs_annotation=True,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return terminal, zone, camera, event


@pytest.mark.asyncio
async def test_annotation_clears_needs_annotation(db_session: AsyncSession) -> None:
    terminal, zone, camera, event = await _create_queued_event(db_session)

    payload = AnnotationCreateSchema(
        camera_event_id=event.id,
        annotator_id="trainer1",
        action_type="picking",
    )
    annotation = await CreateAnnotationService(db_session).execute(payload)

    assert annotation.id is not None
    assert annotation.action_type == "picking"

    await db_session.refresh(event)
    assert event.needs_annotation is False
    assert event.action_type == "picking"
    assert event.confidence == 1.0


@pytest.mark.asyncio
async def test_annotation_with_employee_creates_action(db_session: AsyncSession) -> None:
    from datetime import timedelta
    from app.models.sensor_position import SensorPosition

    terminal, zone, camera, event = await _create_queued_event(db_session)
    employee = await CreateEmployeeService(db_session).execute(
        EmployeeCreateSchema(name="Alice", badge_id="B001", terminal_id=terminal.id)
    )
    pos = SensorPosition(
        employee_id=employee.id, x=50, y=50,
        zone_id=zone.id, sector_id=None, timestamp=NOW,
    )
    db_session.add(pos)
    await db_session.commit()

    payload = AnnotationCreateSchema(
        camera_event_id=event.id, annotator_id="trainer1", action_type="picking"
    )
    await CreateAnnotationService(db_session).execute(payload)

    actions = (await db_session.execute(select(EmployeeAction))).scalars().all()
    assert len(actions) == 1
    assert actions[0].action_type == "picking"
    assert actions[0].employee_id == employee.id
