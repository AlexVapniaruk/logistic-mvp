from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.training import TrainingJobReadSchema


class StartTrainingService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, config: dict) -> TrainingJobReadSchema:
        # Placeholder: real implementation persists a TrainingJob ORM row
        # and dispatches to a background worker / Celery task.
        return TrainingJobReadSchema(
            id=0,
            status="pending",
            model_version_id=None,
            started_at=datetime.now(timezone.utc),
            finished_at=None,
            config=config,
            error=None,
        )
