from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.schemas.employee import EmployeeReadSchema


class ListEmployeesService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self) -> list[EmployeeReadSchema]:
        result = await self.db.execute(select(Employee).order_by(Employee.id))
        return [EmployeeReadSchema.model_validate(row) for row in result.scalars()]
