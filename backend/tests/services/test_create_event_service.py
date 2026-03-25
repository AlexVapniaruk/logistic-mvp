from datetime import datetime, timezone
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreateSchema
from app.services.events.create_event_service import CreateEventService


@pytest.mark.asyncio
async def test_persists_event_to_db(db_session: AsyncSession):
    payload = EventCreateSchema(
        camera_id="cam1",
        action_class="unload",
        confidence=0.88,
        timestamp=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )

    result = await CreateEventService(db_session).execute(payload)

    assert result.id is not None
    assert result.action_class == "unload"

    db_row = (await db_session.execute(select(Event).where(Event.id == result.id))).scalar_one()
    assert db_row.camera_id == "cam1"
