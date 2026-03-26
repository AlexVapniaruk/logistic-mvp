import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.terminal import TerminalCreateSchema
from app.services.terminals.create_terminal_service import CreateTerminalService


@pytest.mark.asyncio
async def test_create_terminal_returns_schema(db_session: AsyncSession) -> None:
    payload = TerminalCreateSchema(name="Terminal A")
    result = await CreateTerminalService(db_session).execute(payload)

    assert result.id is not None
    assert result.name == "Terminal A"
    assert result.description is None
    assert result.map_image_url is None


@pytest.mark.asyncio
async def test_create_terminal_with_all_fields(db_session: AsyncSession) -> None:
    payload = TerminalCreateSchema(
        name="Terminal B",
        description="Main warehouse",
        map_image_url="https://example.com/map.png",
    )
    result = await CreateTerminalService(db_session).execute(payload)

    assert result.name == "Terminal B"
    assert result.description == "Main warehouse"
    assert result.map_image_url == "https://example.com/map.png"
