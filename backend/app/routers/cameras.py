from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.camera import CameraCreateSchema, CameraUpdateSchema, CameraReadSchema
from app.services.cameras.create_camera_service import CreateCameraService
from app.services.cameras.list_cameras_service import ListCamerasService
from app.services.cameras.update_camera_service import UpdateCameraService

router = APIRouter()


@router.get("/", response_model=list[CameraReadSchema])
async def list_cameras(db: AsyncSession = Depends(get_db)):
    return await ListCamerasService(db).execute()


@router.post("/", response_model=CameraReadSchema, status_code=201)
async def create_camera(payload: CameraCreateSchema, db: AsyncSession = Depends(get_db)):
    return await CreateCameraService(db).execute(payload)


@router.patch("/{camera_id}", response_model=CameraReadSchema)
async def update_camera(
    camera_id: int, payload: CameraUpdateSchema, db: AsyncSession = Depends(get_db)
):
    return await UpdateCameraService(db).execute(camera_id, payload)
