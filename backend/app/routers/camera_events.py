from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.camera_event import (
    CameraEventCreateSchema,
    CameraEventFilterSchema,
    CameraEventReadSchema,
)
from app.services.camera_events.create_camera_event_service import CreateCameraEventService
from app.services.camera_events.list_camera_events_service import ListCameraEventsService

router = APIRouter()


@router.get("/", response_model=list[CameraEventReadSchema])
async def list_camera_events(
    filters: CameraEventFilterSchema = Depends(), db: AsyncSession = Depends(get_db)
):
    return await ListCameraEventsService(db).execute(filters)


@router.post("/", response_model=CameraEventReadSchema, status_code=201)
async def create_camera_event(
    payload: CameraEventCreateSchema, db: AsyncSession = Depends(get_db)
):
    return await CreateCameraEventService(db).execute(payload)
