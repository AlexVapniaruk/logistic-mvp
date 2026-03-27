from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal import Terminal
from app.schemas.terminal import TerminalUpdateSchema, TerminalReadSchema


class UpdateTerminalService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, terminal_id: int, payload: TerminalUpdateSchema) -> TerminalReadSchema:
        result = await self.db.execute(select(Terminal).where(Terminal.id == terminal_id))
        terminal = result.scalar_one_or_none()
        if terminal is None:
            raise HTTPException(status_code=404, detail="Terminal not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(terminal, field, value)

        await self.db.commit()
        await self.db.refresh(terminal)
        return TerminalReadSchema.model_validate(terminal)
