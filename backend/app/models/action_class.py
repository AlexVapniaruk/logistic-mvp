from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class ActionClass(Base):
    __tablename__ = "action_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    label: Mapped[str] = mapped_column(String(256))
    confidence_threshold: Mapped[float] = mapped_column(Float, default=0.5)

    def __repr__(self) -> str:
        return f"<ActionClass id={self.id} name={self.name}>"
