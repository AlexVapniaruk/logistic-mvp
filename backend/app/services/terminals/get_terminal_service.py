from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal import Terminal
from app.schemas.terminal import TerminalReadSchema


class GetTerminalService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, terminal_id: int) -> TerminalReadSchema:
        result = await self.db.execute(select(Terminal).where(Terminal.id == terminal_id))
        terminal = result.scalar_one_or_none()
        if terminal is None:
            raise HTTPException(status_code=404, detail="Terminal not found")
        return TerminalReadSchema.model_validate(terminal)
