from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    stream_url: Mapped[str] = mapped_column(String(512))
    mac_address: Mapped[str | None] = mapped_column(String(17), nullable=True, unique=True, index=True)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    location: Mapped[str | None] = mapped_column(String(256), nullable=True)
    terminal_id: Mapped[int] = mapped_column(ForeignKey("terminals.id"), index=True)
    zone_id: Mapped[int | None] = mapped_column(ForeignKey("zones.id"), nullable=True, index=True)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Camera id={self.id} name={self.name}>"
