from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera import Camera
from app.schemas.camera import CameraCreateSchema, CameraReadSchema


class CreateCameraService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: CameraCreateSchema) -> CameraReadSchema:
        camera = Camera(
            name=payload.name,
            stream_url=payload.stream_url,
            terminal_id=payload.terminal_id,
            zone_id=payload.zone_id,
            sector_id=payload.sector_id,
        )
        self.db.add(camera)
        await self.db.commit()
        await self.db.refresh(camera)
        return CameraReadSchema.model_validate(camera)
