from datetime import datetime, timezone
import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.services.events.get_event_service import GetEventService


@pytest.mark.asyncio
async def test_returns_event_by_id(db_session: AsyncSession):
    event = Event(
        camera_id="cam1", action_class="carry", confidence=0.95,
        timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc), metadata_={},
    )
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)

    result = await GetEventService(db_session).execute(event.id)

    assert result.id == event.id
    assert result.action_class == "carry"


@pytest.mark.asyncio
async def test_raises_404_when_not_found(db_session: AsyncSession):
    with pytest.raises(HTTPException) as exc:
        await GetEventService(db_session).execute(999)

    assert exc.value.status_code == 404
