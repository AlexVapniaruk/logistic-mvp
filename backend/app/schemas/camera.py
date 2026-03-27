from pydantic import BaseModel


class CameraCreateSchema(BaseModel):
    name: str
    stream_url: str
    terminal_id: int
    mac_address: str | None = None
    version: str | None = None
    location: str | None = None
    zone_id: int | None = None
    sector_id: int | None = None


class CameraUpdateSchema(BaseModel):
    name: str | None = None
    stream_url: str | None = None
    mac_address: str | None = None
    version: str | None = None
    location: str | None = None
    zone_id: int | None = None
    sector_id: int | None = None


class CameraReadSchema(BaseModel):
    id: int
    name: str
    stream_url: str
    mac_address: str | None
    version: str | None
    location: str | None
    terminal_id: int
    zone_id: int | None
    sector_id: int | None

    model_config = {"from_attributes": True}
