from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventReadSchema


class GetEventService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, event_id: int) -> EventReadSchema:
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        event = result.scalar_one_or_none()
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return EventReadSchema.model_validate(event)
