from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.employee import EmployeeCreateSchema, EmployeeReadSchema
from app.services.employees.create_employee_service import CreateEmployeeService
from app.services.employees.list_employees_service import ListEmployeesService

router = APIRouter()


@router.get("/", response_model=list[EmployeeReadSchema])
async def list_employees(db: AsyncSession = Depends(get_db)):
    return await ListEmployeesService(db).execute()


@router.post("/", response_model=EmployeeReadSchema, status_code=201)
async def create_employee(payload: EmployeeCreateSchema, db: AsyncSession = Depends(get_db)):
    return await CreateEmployeeService(db).execute(payload)
