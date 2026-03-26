from datetime import datetime, timezone
import pytest
from httpx import AsyncClient


NOW_ISO = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc).isoformat()


async def _create_terminal_and_camera(client: AsyncClient) -> dict:
    terminal = (await client.post("/api/terminals/", json={"name": "T"})).json()
    camera = (await client.post("/api/cameras/", json={
        "name": "Cam1", "stream_url": "rtsp://x", "terminal_id": terminal["id"]
    })).json()
    return camera


@pytest.mark.asyncio
async def test_create_camera_event_low_confidence(client: AsyncClient) -> None:
    camera = await _create_terminal_and_camera(client)
    payload = {
        "camera_id": camera["id"],
        "timestamp": NOW_ISO,
        "action_type": "idle",
        "confidence": 0.5,
    }
    response = await client.post("/api/camera-events/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["needs_annotation"] is True
    assert data["employee_action_id"] is None


@pytest.mark.asyncio
async def test_list_camera_events_filter_needs_annotation(client: AsyncClient) -> None:
    camera = await _create_terminal_and_camera(client)

    # Create one low-confidence (queued) and one high-confidence event
    await client.post("/api/camera-events/", json={
        "camera_id": camera["id"], "timestamp": NOW_ISO,
        "action_type": "idle", "confidence": 0.3,
    })
    await client.post("/api/camera-events/", json={
        "camera_id": camera["id"], "timestamp": NOW_ISO,
        "action_type": "picking", "confidence": 0.95,
    })

    response = await client.get("/api/camera-events/?needs_annotation=true")
    assert response.status_code == 200
    events = response.json()
    assert len(events) >= 1
    assert all(e["needs_annotation"] for e in events)


@pytest.mark.asyncio
async def test_list_camera_events_no_filter(client: AsyncClient) -> None:
    camera = await _create_terminal_and_camera(client)
    await client.post("/api/camera-events/", json={
        "camera_id": camera["id"], "timestamp": NOW_ISO,
        "action_type": "walking", "confidence": 0.7,
    })
    response = await client.get("/api/camera-events/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
