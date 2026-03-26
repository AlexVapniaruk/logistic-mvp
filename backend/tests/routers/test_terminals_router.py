import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_terminal(client: AsyncClient) -> None:
    response = await client.post("/api/terminals/", json={"name": "Warehouse A"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Warehouse A"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_list_terminals(client: AsyncClient) -> None:
    await client.post("/api/terminals/", json={"name": "T1"})
    await client.post("/api/terminals/", json={"name": "T2"})
    response = await client.get("/api/terminals/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_terminal(client: AsyncClient) -> None:
    created = (await client.post("/api/terminals/", json={"name": "T"})).json()
    response = await client.get(f"/api/terminals/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


@pytest.mark.asyncio
async def test_get_terminal_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/terminals/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_zone_under_terminal(client: AsyncClient) -> None:
    terminal = (await client.post("/api/terminals/", json={"name": "T"})).json()
    payload = {"name": "Zone A", "points": [[0, 0], [100, 0], [100, 100], [0, 100]]}
    response = await client.post(f"/api/terminals/{terminal['id']}/zones/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["terminal_id"] == terminal["id"]
    assert data["name"] == "Zone A"


@pytest.mark.asyncio
async def test_list_zones_under_terminal(client: AsyncClient) -> None:
    t = (await client.post("/api/terminals/", json={"name": "T"})).json()
    pts = [[0, 0], [100, 0], [100, 100], [0, 100]]
    await client.post(f"/api/terminals/{t['id']}/zones/", json={"name": "Z1", "points": pts})
    await client.post(f"/api/terminals/{t['id']}/zones/", json={"name": "Z2", "points": pts})

    response = await client.get(f"/api/terminals/{t['id']}/zones/")
    assert response.status_code == 200
    assert len(response.json()) == 2
