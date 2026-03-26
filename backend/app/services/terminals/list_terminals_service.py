from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal import Terminal
from app.schemas.terminal import TerminalReadSchema


class ListTerminalsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self) -> list[TerminalReadSchema]:
        result = await self.db.execute(select(Terminal).order_by(Terminal.id))
        return [TerminalReadSchema.model_validate(row) for row in result.scalars()]
