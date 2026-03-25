from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreateSchema, EventReadSchema


class CreateEventService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: EventCreateSchema) -> EventReadSchema:
        event = Event(
            camera_id=payload.camera_id,
            action_class=payload.action_class,
            confidence=payload.confidence,
            timestamp=payload.timestamp,
            frame_path=payload.frame_path,
            metadata_=payload.metadata,
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return EventReadSchema.model_validate(event)
