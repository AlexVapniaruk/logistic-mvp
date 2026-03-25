from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.training import TrainingJobReadSchema


class GetTrainingStatusService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, job_id: int) -> TrainingJobReadSchema:
        # Placeholder: real implementation fetches TrainingJob from DB
        raise HTTPException(status_code=404, detail="Job not found")
