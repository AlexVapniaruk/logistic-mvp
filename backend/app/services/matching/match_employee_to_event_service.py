from datetime import timedelta, timezone
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import TIME_WINDOW_SECONDS
from app.models.camera import Camera
from app.models.employee import Employee
from app.models.sensor_position import SensorPosition
from app.models.camera_event import CameraEvent


class MatchEmployeeToEventService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, event: CameraEvent) -> Employee | None:
        camera = await self._get_camera(event.camera_id)
        if camera is None or camera.zone_id is None:
            return None

        positions = await self._find_positions_in_window(event, camera.zone_id)
        if not positions:
            return None

        closest = min(positions, key=lambda p: abs(self._utc(p.timestamp) - self._utc(event.timestamp)))
        return await self._get_employee(closest.employee_id)

    async def _get_camera(self, camera_id: int) -> Camera | None:
        result = await self.db.execute(select(Camera).where(Camera.id == camera_id))
        return result.scalar_one_or_none()

    async def _find_positions_in_window(
        self, event: CameraEvent, zone_id: int
    ) -> list[SensorPosition]:
        window = timedelta(seconds=TIME_WINDOW_SECONDS)
        result = await self.db.execute(
            select(SensorPosition).where(
                and_(
                    SensorPosition.zone_id == zone_id,
                    SensorPosition.timestamp >= event.timestamp - window,
                    SensorPosition.timestamp <= event.timestamp + window,
                )
            )
        )
        return list(result.scalars())

    @staticmethod
    def _utc(dt) -> "datetime":
        from datetime import datetime
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt

    async def _get_employee(self, employee_id: int) -> Employee | None:
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        return result.scalar_one_or_none()
