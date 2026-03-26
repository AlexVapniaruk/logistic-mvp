from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee_action import EmployeeAction
from app.schemas.heatmap import EmployeeAnalyticsSchema


class GetEmployeeAnalyticsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, employee_id: int) -> EmployeeAnalyticsSchema:
        stmt = (
            select(EmployeeAction.action_type, func.count(EmployeeAction.id))
            .where(EmployeeAction.employee_id == employee_id)
            .group_by(EmployeeAction.action_type)
        )
        rows = (await self.db.execute(stmt)).all()
        action_counts = {action_type: count for action_type, count in rows}
        return EmployeeAnalyticsSchema(
            employee_id=employee_id,
            action_counts=action_counts,
            total=sum(action_counts.values()),
        )
