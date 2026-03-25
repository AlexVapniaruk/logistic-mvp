from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventFilterSchema
from app.services.events.get_events_list_service import GetEventsListService


@pytest.mark.asyncio
async def test_returns_empty_when_no_events(db_session: AsyncSession):
    result = await GetEventsListService(db_session).execute(EventFilterSchema())
    assert result == []


@pytest.mark.asyncio
async def test_returns_events_ordered_by_timestamp_desc(db_session: AsyncSession):
    for i in range(3):
        db_session.add(Event(
            camera_id="cam1",
            action_class="carry",
            confidence=0.9,
            timestamp=datetime(2024, 1, i + 1, tzinfo=timezone.utc),
            metadata_={},
        ))
    await db_session.commit()

    result = await GetEventsListService(db_session).execute(EventFilterSchema())

    assert len(result) == 3
    assert result[0].timestamp > result[1].timestamp


@pytest.mark.asyncio
async def test_filters_by_camera_id(db_session: AsyncSession):
    db_session.add(Event(
        camera_id="cam_a", action_class="carry", confidence=0.8,
        timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc), metadata_={},
    ))
    db_session.add(Event(
        camera_id="cam_b", action_class="carry", confidence=0.8,
        timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc), metadata_={},
    ))
    await db_session.commit()

    result = await GetEventsListService(db_session).execute(EventFilterSchema(camera_id="cam_a"))

    assert len(result) == 1
    assert result[0].camera_id == "cam_a"
