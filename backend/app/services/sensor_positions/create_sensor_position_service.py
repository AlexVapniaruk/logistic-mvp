import json
from datetime import timezone

import redis.asyncio as aioredis
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.models.sensor_position import SensorPosition
from app.models.zone import Zone
from app.models.sector import Sector
from app.schemas.sensor_position import SensorPositionCreateSchema, SensorPositionReadSchema
from app.services.geo.point_in_polygon import is_point_in_polygon


class CreateSensorPositionService:
    def __init__(self, db: AsyncSession, redis: aioredis.Redis) -> None:
        self.db = db
        self.redis = redis

    async def execute(self, payload: SensorPositionCreateSchema) -> SensorPositionReadSchema:
        employee = await self._get_employee(payload.employee_id)
        zone_id = await self._resolve_zone(payload.x, payload.y, employee.terminal_id)
        sector_id = await self._resolve_sector(payload.x, payload.y, zone_id)

        position = SensorPosition(
            employee_id=payload.employee_id,
            x=payload.x,
            y=payload.y,
            zone_id=zone_id,
            sector_id=sector_id,
            timestamp=payload.timestamp,
        )
        self.db.add(position)
        await self.db.commit()
        await self.db.refresh(position)

        await self._publish_position(position)
        return SensorPositionReadSchema.model_validate(position)

    async def _get_employee(self, employee_id: int) -> Employee:
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        employee = result.scalar_one_or_none()
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    async def _resolve_zone(self, x: float, y: float, terminal_id: int) -> int | None:
        result = await self.db.execute(select(Zone).where(Zone.terminal_id == terminal_id))
        for zone in result.scalars():
            if is_point_in_polygon(x, y, zone.points):
                return zone.id
        return None

    async def _resolve_sector(self, x: float, y: float, zone_id: int | None) -> int | None:
        if zone_id is None:
            return None
        result = await self.db.execute(select(Sector).where(Sector.zone_id == zone_id))
        for sector in result.scalars():
            if is_point_in_polygon(x, y, sector.points):
                return sector.id
        return None

    async def _publish_position(self, position: SensorPosition) -> None:
        ts = position.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        message = json.dumps({
            "type": "position_update",
            "payload": {
                "id": position.id,
                "employee_id": position.employee_id,
                "x": position.x,
                "y": position.y,
                "zone_id": position.zone_id,
                "sector_id": position.sector_id,
                "timestamp": ts.isoformat(),
            },
        })
        await self.redis.publish("positions", message)
