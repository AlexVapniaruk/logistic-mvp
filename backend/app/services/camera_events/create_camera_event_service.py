from sqlalchemy.ext.asyncio import AsyncSession

from app.config import CONFIDENCE_THRESHOLD
from app.models.camera_event import CameraEvent
from app.schemas.camera_event import CameraEventCreateSchema, CameraEventReadSchema
from app.services.actions.process_camera_event_service import ProcessCameraEventService


class CreateCameraEventService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: CameraEventCreateSchema) -> CameraEventReadSchema:
        event = CameraEvent(
            camera_id=payload.camera_id,
            timestamp=payload.timestamp,
            action_type=payload.action_type,
            confidence=payload.confidence,
            bounding_box=payload.bounding_box,
            video_clip_url=payload.video_clip_url,
            needs_annotation=False,
        )
        self.db.add(event)
        await self.db.flush()

        if payload.confidence >= CONFIDENCE_THRESHOLD:
            action = await ProcessCameraEventService(self.db).execute(event.id)
            if action is None:
                event.needs_annotation = True
        else:
            event.needs_annotation = True

        await self.db.commit()
        await self.db.refresh(event)
        return CameraEventReadSchema.model_validate(event)
