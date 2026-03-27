from pydantic import BaseModel


class TerminalCreateSchema(BaseModel):
    name: str
    description: str | None = None
    map_image_url: str | None = None


class TerminalUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    map_image_url: str | None = None


class TerminalReadSchema(BaseModel):
    id: int
    name: str
    description: str | None
    map_image_url: str | None

    model_config = {"from_attributes": True}
