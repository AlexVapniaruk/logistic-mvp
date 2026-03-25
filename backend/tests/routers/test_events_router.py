from datetime import datetime, timezone
import pytest
from httpx import AsyncClient

from app.models.event import Event


@pytest.mark.asyncio
async def test_list_events_empty(client: AsyncClient):
    response = await client.get("/api/events/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_and_get_event(client: AsyncClient, db_session):
    payload = {
        "camera_id": "cam1",
        "action_class": "carry",
        "confidence": 0.9,
        "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc).isoformat(),
    }
    create_resp = await client.post("/api/events/", json=payload)
    assert create_resp.status_code == 201

    event_id = create_resp.json()["id"]
    get_resp = await client.get(f"/api/events/{event_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["action_class"] == "carry"


@pytest.mark.asyncio
async def test_get_event_not_found(client: AsyncClient):
    response = await client.get("/api/events/99999")
    assert response.status_code == 404
