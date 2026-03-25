from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventFilterSchema, EventReadSchema


class GetEventsListService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, filters: EventFilterSchema) -> list[EventReadSchema]:
        conditions = self._build_conditions(filters)
        stmt = select(Event).order_by(Event.timestamp.desc())
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.limit(filters.limit).offset(filters.offset)
        result = await self.db.execute(stmt)
        return [EventReadSchema.model_validate(row) for row in result.scalars()]

    def _build_conditions(self, filters: EventFilterSchema) -> list:
        conditions = []
        if filters.camera_id:
            conditions.append(Event.camera_id == filters.camera_id)
        if filters.action_class:
            conditions.append(Event.action_class == filters.action_class)
        if filters.from_ts:
            conditions.append(Event.timestamp >= filters.from_ts)
        if filters.to_ts:
            conditions.append(Event.timestamp <= filters.to_ts)
        return conditions
