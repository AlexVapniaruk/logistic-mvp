from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    badge_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    terminal_id: Mapped[int] = mapped_column(ForeignKey("terminals.id"), index=True)

    def __repr__(self) -> str:
        return f"<Employee id={self.id} badge={self.badge_id}>"
