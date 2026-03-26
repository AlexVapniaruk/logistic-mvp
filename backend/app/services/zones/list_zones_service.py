from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.zone import Zone
from app.schemas.zone import ZoneReadSchema


class ListZonesService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, terminal_id: int) -> list[ZoneReadSchema]:
        result = await self.db.execute(
            select(Zone).where(Zone.terminal_id == terminal_id).order_by(Zone.id)
        )
        return [ZoneReadSchema.model_validate(row) for row in result.scalars()]
