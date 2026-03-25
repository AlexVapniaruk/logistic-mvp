import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_models_empty(client: AsyncClient):
    response = await client.get("/api/training/models")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_start_training_returns_pending(client: AsyncClient):
    response = await client.post("/api/training/start", json={"config": {"epochs": 10}})
    assert response.status_code == 202
    assert response.json()["status"] == "pending"
