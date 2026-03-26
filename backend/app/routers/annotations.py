from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.annotation import AnnotationCreateSchema, AnnotationReadSchema
from app.services.annotations.create_annotation_service import CreateAnnotationService

router = APIRouter()


@router.post("/", response_model=AnnotationReadSchema, status_code=201)
async def create_annotation(payload: AnnotationCreateSchema, db: AsyncSession = Depends(get_db)):
    return await CreateAnnotationService(db).execute(payload)
