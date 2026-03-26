from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal import Terminal
from app.schemas.terminal import TerminalCreateSchema, TerminalReadSchema


class CreateTerminalService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: TerminalCreateSchema) -> TerminalReadSchema:
        terminal = Terminal(
            name=payload.name,
            description=payload.description,
            map_image_url=payload.map_image_url,
        )
        self.db.add(terminal)
        await self.db.commit()
        await self.db.refresh(terminal)
        return TerminalReadSchema.model_validate(terminal)
