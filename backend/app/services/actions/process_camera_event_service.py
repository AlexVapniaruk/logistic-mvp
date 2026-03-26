from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.camera import Camera
from app.models.camera_event import CameraEvent
from app.models.employee import Employee
from app.models.employee_action import EmployeeAction
from app.schemas.employee_action import EmployeeActionReadSchema
from app.services.matching.match_employee_to_event_service import MatchEmployeeToEventService


class ProcessCameraEventService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, camera_event_id: int) -> EmployeeActionReadSchema | None:
        event = await self._get_event(camera_event_id)
        if event is None:
            return None

        employee = await MatchEmployeeToEventService(self.db).execute(event)
        if employee is None:
            return None

        camera = await self._get_camera(event.camera_id)
        action = await self._create_action(event, employee, camera)
        event.employee_action_id = action.id
        event.needs_annotation = False
        await self.db.commit()
        await self.db.refresh(action)
        return EmployeeActionReadSchema.model_validate(action)

    async def _get_event(self, camera_event_id: int) -> CameraEvent | None:
        result = await self.db.execute(
            select(CameraEvent).where(CameraEvent.id == camera_event_id)
        )
        return result.scalar_one_or_none()

    async def _get_camera(self, camera_id: int) -> Camera | None:
        result = await self.db.execute(select(Camera).where(Camera.id == camera_id))
        return result.scalar_one_or_none()

    async def _create_action(
        self, event: CameraEvent, employee: Employee, camera: Camera | None
    ) -> EmployeeAction:
        action = EmployeeAction(
            employee_id=employee.id,
            zone_id=camera.zone_id if camera else None,
            sector_id=camera.sector_id if camera else None,
            action_type=event.action_type,
            confidence=event.confidence,
            source_event_id=event.id,
            timestamp=event.timestamp,
        )
        self.db.add(action)
        await self.db.flush()
        return action
