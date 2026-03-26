from pydantic import BaseModel


class ZoneBodySchema(BaseModel):
    """Body for POST /terminals/{id}/zones/ — terminal_id comes from path."""
    name: str
    points: list[list[float]]


class ZoneCreateSchema(BaseModel):
    name: str
    points: list[list[float]]
    terminal_id: int


class ZoneReadSchema(BaseModel):
    id: int
    name: str
    points: list[list[float]]
    terminal_id: int

    model_config = {"from_attributes": True}
