from datetime import datetime
from sqlalchemy import Float, DateTime, Boolean, JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class CameraEvent(Base):
    __tablename__ = "camera_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    action_type: Mapped[str] = mapped_column(String(128))
    confidence: Mapped[float] = mapped_column(Float)
    bounding_box: Mapped[list | None] = mapped_column(JSON, nullable=True)
    video_clip_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    needs_annotation: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    # Deferred FK to break circular dependency with employee_actions
    employee_action_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "employee_actions.id",
            use_alter=True,
            name="fk_camera_events_employee_action_id",
        ),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<CameraEvent id={self.id} action={self.action_type} confidence={self.confidence}>"
