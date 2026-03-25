from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.training import ModelVersionReadSchema, TrainingJobReadSchema, StartTrainingSchema
from app.services.training.list_model_versions_service import ListModelVersionsService
from app.services.training.start_training_service import StartTrainingService
from app.services.training.get_training_status_service import GetTrainingStatusService

router = APIRouter()


@router.get("/models", response_model=list[ModelVersionReadSchema])
async def list_models(db: AsyncSession = Depends(get_db)):
    return await ListModelVersionsService(db).execute()


@router.post("/start", response_model=TrainingJobReadSchema, status_code=202)
async def start_training(payload: StartTrainingSchema, db: AsyncSession = Depends(get_db)):
    return await StartTrainingService(db).execute(payload.config)


@router.get("/jobs/{job_id}", response_model=TrainingJobReadSchema)
async def get_job_status(job_id: int, db: AsyncSession = Depends(get_db)):
    return await GetTrainingStatusService(db).execute(job_id)
