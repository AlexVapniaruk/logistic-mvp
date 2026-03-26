from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera_event import CameraEvent
from app.schemas.camera_event import CameraEventFilterSchema, CameraEventReadSchema


class ListCameraEventsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, filters: CameraEventFilterSchema) -> list[CameraEventReadSchema]:
        conditions = self._build_conditions(filters)
        stmt = select(CameraEvent).order_by(CameraEvent.timestamp.desc())
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.limit(filters.limit).offset(filters.offset)
        result = await self.db.execute(stmt)
        return [CameraEventReadSchema.model_validate(row) for row in result.scalars()]

    def _build_conditions(self, filters: CameraEventFilterSchema) -> list:
        conditions = []
        if filters.needs_annotation is not None:
            conditions.append(CameraEvent.needs_annotation == filters.needs_annotation)
        if filters.camera_id is not None:
            conditions.append(CameraEvent.camera_id == filters.camera_id)
        return conditions
