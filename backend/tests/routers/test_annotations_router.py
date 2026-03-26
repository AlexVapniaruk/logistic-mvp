from datetime import datetime, timezone
import pytest
from httpx import AsyncClient

from app.models.camera_event import CameraEvent
from sqlalchemy.ext.asyncio import AsyncSession

NOW_ISO = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()


@pytest.mark.asyncio
async def test_create_annotation(client: AsyncClient, db_session: AsyncSession) -> None:
    # Set up: terminal + camera + queued event
    terminal = (await client.post("/api/terminals/", json={"name": "T"})).json()
    camera = (await client.post("/api/cameras/", json={
        "name": "C", "stream_url": "rtsp://x", "terminal_id": terminal["id"]
    })).json()

    event = CameraEvent(
        camera_id=camera["id"],
        timestamp=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        action_type="unknown",
        confidence=0.4,
        needs_annotation=True,
    )
    db_session.add(event)
    await db_session.commit()
    await db_session.refresh(event)

    payload = {
        "camera_event_id": event.id,
        "annotator_id": "trainer1",
        "action_type": "picking",
    }
    response = await client.post("/api/annotations/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["action_type"] == "picking"
    assert data["annotator_id"] == "trainer1"

    # Verify the event is cleared from annotation queue
    queue_response = await client.get("/api/camera-events/?needs_annotation=true")
    queued_ids = [e["id"] for e in queue_response.json()]
    assert event.id not in queued_ids
