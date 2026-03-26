from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Zone(Base):
    __tablename__ = "zones"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    points: Mapped[list] = mapped_column(JSON)
    terminal_id: Mapped[int] = mapped_column(ForeignKey("terminals.id"), index=True)

    def __repr__(self) -> str:
        return f"<Zone id={self.id} name={self.name}>"
