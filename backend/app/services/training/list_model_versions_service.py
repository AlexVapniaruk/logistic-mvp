from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.model_version import ModelVersion
from app.schemas.training import ModelVersionReadSchema


class ListModelVersionsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self) -> list[ModelVersionReadSchema]:
        result = await self.db.execute(select(ModelVersion).order_by(ModelVersion.created_at.desc()))
        return [ModelVersionReadSchema.model_validate(row) for row in result.scalars()]
