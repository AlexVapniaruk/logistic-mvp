from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera import Camera
from app.schemas.camera import CameraReadSchema


class ListCamerasService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self) -> list[CameraReadSchema]:
        result = await self.db.execute(select(Camera).order_by(Camera.id))
        return [CameraReadSchema.model_validate(row) for row in result.scalars()]
