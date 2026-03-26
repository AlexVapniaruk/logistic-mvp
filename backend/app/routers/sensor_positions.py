from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from app.db import get_db
from app.redis import get_redis
from app.schemas.sensor_position import SensorPositionCreateSchema, SensorPositionReadSchema
from app.services.sensor_positions.create_sensor_position_service import (
    CreateSensorPositionService,
)

router = APIRouter()


@router.post("/", response_model=SensorPositionReadSchema, status_code=201)
async def create_sensor_position(
    payload: SensorPositionCreateSchema,
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    return await CreateSensorPositionService(db, redis).execute(payload)
