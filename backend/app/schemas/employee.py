from pydantic import BaseModel


class EmployeeCreateSchema(BaseModel):
    name: str
    badge_id: str
    terminal_id: int


class EmployeeReadSchema(BaseModel):
    id: int
    name: str
    badge_id: str
    terminal_id: int

    model_config = {"from_attributes": True}
