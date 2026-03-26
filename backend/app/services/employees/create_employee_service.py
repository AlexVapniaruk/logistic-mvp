from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreateSchema, EmployeeReadSchema


class CreateEmployeeService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, payload: EmployeeCreateSchema) -> EmployeeReadSchema:
        employee = Employee(
            name=payload.name,
            badge_id=payload.badge_id,
            terminal_id=payload.terminal_id,
        )
        self.db.add(employee)
        await self.db.commit()
        await self.db.refresh(employee)
        return EmployeeReadSchema.model_validate(employee)
