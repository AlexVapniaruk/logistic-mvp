from pydantic import BaseModel


class SectorBodySchema(BaseModel):
    """Body for POST /zones/{id}/sectors/ — zone_id comes from path."""
    name: str
    points: list[list[float]]


class SectorCreateSchema(BaseModel):
    name: str
    points: list[list[float]]
    zone_id: int


class SectorReadSchema(BaseModel):
    id: int
    name: str
    points: list[list[float]]
    zone_id: int

    model_config = {"from_attributes": True}
