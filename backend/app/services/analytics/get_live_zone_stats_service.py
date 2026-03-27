from datetime import datetime, timedelta, timezone
from collections import defaultdict

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.models.employee_action import EmployeeAction
from app.models.sensor_position import SensorPosition
from app.models.zone import Zone
from app.schemas.heatmap import (
    ActiveEmployeeSchema,
    ZoneLiveResponseSchema,
    ZoneLiveStatsSchema,
)


class GetLiveZoneStatsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def execute(self, window_minutes: int = 5, terminal_id: int | None = None) -> ZoneLiveResponseSchema:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)

        terminal_zone_ids = await self._load_terminal_zone_ids(terminal_id) if terminal_id else None
        position_rows = await self._query_positions(cutoff, terminal_zone_ids)
        action_rows = await self._query_actions(cutoff, terminal_zone_ids)

        zone_ids = {r.zone_id for r in position_rows} | {r.zone_id for r in action_rows}
        employee_ids = {r.employee_id for r in position_rows}

        zone_names = await self._load_zone_names(zone_ids)
        employee_names = await self._load_employee_names(employee_ids)

        # Build per-zone employee map: (zone_id, employee_id) → latest row
        latest: dict[tuple[int, int], object] = {}
        for row in position_rows:
            key = (row.zone_id, row.employee_id)
            if key not in latest or row.last_seen > latest[key].last_seen:
                latest[key] = row

        # Build action_counts per zone
        action_counts_by_zone: dict[int, dict[str, int]] = defaultdict(dict)
        for row in action_rows:
            action_counts_by_zone[row.zone_id][row.action_type] = row.cnt

        zones = []
        for zone_id in zone_ids:
            employees_in_zone = [v for (z, _), v in latest.items() if z == zone_id]
            last_activity_at = max((e.last_seen for e in employees_in_zone), default=None)

            active_employees = [
                ActiveEmployeeSchema(
                    employee_id=row.employee_id,
                    employee_name=employee_names.get(row.employee_id, str(row.employee_id)),
                    last_seen=row.last_seen,
                    last_x=row.last_x,
                    last_y=row.last_y,
                )
                for row in employees_in_zone
            ]

            zones.append(
                ZoneLiveStatsSchema(
                    zone_id=zone_id,
                    zone_name=zone_names.get(zone_id, str(zone_id)),
                    active_employee_count=len(active_employees),
                    last_activity_at=last_activity_at,
                    active_employees=active_employees,
                    action_counts=action_counts_by_zone.get(zone_id, {}),
                )
            )

        return ZoneLiveResponseSchema(
            generated_at=datetime.now(timezone.utc),
            window_minutes=window_minutes,
            zones=zones,
        )

    async def _load_terminal_zone_ids(self, terminal_id: int) -> set[int]:
        result = await self.db.execute(select(Zone.id).where(Zone.terminal_id == terminal_id))
        return set(result.scalars())

    async def _query_positions(self, cutoff: datetime, zone_ids: set[int] | None = None):
        stmt = (
            select(
                SensorPosition.zone_id,
                SensorPosition.employee_id,
                func.max(SensorPosition.timestamp).label("last_seen"),
                func.max(SensorPosition.x).label("last_x"),
                func.max(SensorPosition.y).label("last_y"),
            )
            .where(
                SensorPosition.zone_id.isnot(None),
                SensorPosition.timestamp >= cutoff,
            )
            .group_by(SensorPosition.zone_id, SensorPosition.employee_id)
        )
        if zone_ids is not None:
            stmt = stmt.where(SensorPosition.zone_id.in_(zone_ids))
        result = await self.db.execute(stmt)
        return result.all()

    async def _query_actions(self, cutoff: datetime, zone_ids: set[int] | None = None):
        stmt = (
            select(
                EmployeeAction.zone_id,
                EmployeeAction.action_type,
                func.count(EmployeeAction.id).label("cnt"),
            )
            .where(
                EmployeeAction.zone_id.isnot(None),
                EmployeeAction.timestamp >= cutoff,
            )
            .group_by(EmployeeAction.zone_id, EmployeeAction.action_type)
        )
        if zone_ids is not None:
            stmt = stmt.where(EmployeeAction.zone_id.in_(zone_ids))
        result = await self.db.execute(stmt)
        return result.all()

    async def _load_zone_names(self, zone_ids: set[int]) -> dict[int, str]:
        if not zone_ids:
            return {}
        result = await self.db.execute(select(Zone).where(Zone.id.in_(zone_ids)))
        return {z.id: z.name for z in result.scalars()}

    async def _load_employee_names(self, employee_ids: set[int]) -> dict[int, str]:
        if not employee_ids:
            return {}
        result = await self.db.execute(select(Employee).where(Employee.id.in_(employee_ids)))
        return {e.id: e.name for e in result.scalars()}
