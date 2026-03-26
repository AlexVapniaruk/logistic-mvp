from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    points: Mapped[list] = mapped_column(JSON)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"), index=True)

    def __repr__(self) -> str:
        return f"<Sector id={self.id} name={self.name}>"
