from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.annotation import Annotation
from app.models.camera_event import CameraEvent
from app.schemas.annotation import AnnotationCreateSchema, AnnotationReadSchema
from app.services.actions.process_camera_event_service import ProcessCameraEventService


class CreateAnnotationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: AnnotationCreateSchema) -> AnnotationReadSchema:
        event = await self._get_event(payload.camera_event_id)

        annotation = Annotation(
            camera_event_id=payload.camera_event_id,
            annotator_id=payload.annotator_id,
            action_type=payload.action_type,
            notes=payload.notes,
        )
        self.db.add(annotation)

        event.action_type = payload.action_type
        event.confidence = 1.0
        event.needs_annotation = False
        await self.db.flush()

        await ProcessCameraEventService(self.db).execute(event.id)
        await self.db.commit()
        await self.db.refresh(annotation)
        return AnnotationReadSchema.model_validate(annotation)

    async def _get_event(self, camera_event_id: int) -> CameraEvent:
        result = await self.db.execute(
            select(CameraEvent).where(CameraEvent.id == camera_event_id)
        )
        event = result.scalar_one_or_none()
        if event is None:
            raise HTTPException(status_code=404, detail="CameraEvent not found")
        return event
