from datetime import datetime
from sqlalchemy import Float, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class EmployeeAction(Base):
    __tablename__ = "employee_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"))
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"), nullable=True)
    action_type: Mapped[str] = mapped_column(String(128))
    confidence: Mapped[float] = mapped_column(Float)
    source_event_id: Mapped[int | None] = mapped_column(
        ForeignKey("camera_events.id"), nullable=True
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    def __repr__(self) -> str:
        return f"<EmployeeAction id={self.id} employee={self.employee_id} action={self.action_type}>"
