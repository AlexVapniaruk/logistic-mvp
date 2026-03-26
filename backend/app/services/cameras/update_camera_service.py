from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera import Camera
from app.schemas.camera import CameraUpdateSchema, CameraReadSchema


class UpdateCameraService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, camera_id: int, payload: CameraUpdateSchema) -> CameraReadSchema:
        result = await self.db.execute(select(Camera).where(Camera.id == camera_id))
        camera = result.scalar_one_or_none()
        if camera is None:
            raise HTTPException(status_code=404, detail="Camera not found")
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(camera, field, value)
        await self.db.commit()
        await self.db.refresh(camera)
        return CameraReadSchema.model_validate(camera)
