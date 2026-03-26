from pydantic import BaseModel


class CameraCreateSchema(BaseModel):
    name: str
    stream_url: str
    terminal_id: int
    zone_id: int | None = None
    sector_id: int | None = None


class CameraUpdateSchema(BaseModel):
    name: str | None = None
    stream_url: str | None = None
    zone_id: int | None = None
    sector_id: int | None = None


class CameraReadSchema(BaseModel):
    id: int
    name: str
    stream_url: str
    terminal_id: int
    zone_id: int | None
    sector_id: int | None

    model_config = {"from_attributes": True}
