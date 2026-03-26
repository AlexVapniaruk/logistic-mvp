# Backend — FastAPI (Clean Architecture)

## Stack
FastAPI · SQLAlchemy async · Pydantic v2 · aioredis · Alembic

## Layer rules (dependency direction: inward only)

```
Routers (HTTP) → Services (use cases) → Models / Schemas
                                      ↑
                            db.py / redis.py (infrastructure, injected)
```

| Layer | Rule |
|---|---|
| `routers/` | HTTP parsing + response only. No `if`, no queries, no logic. |
| `services/` | All business logic. See `services/CLAUDE.md`. |
| `models/` | SQLAlchemy ORM mapping only. No methods beyond `__repr__`. |
| `schemas/` | Pydantic v2 validation only. No DB access. |
| `db.py` | Engine + session factory. Injected via `Depends(get_db)`. |
| `redis.py` | aioredis client + pub/sub helpers. Injected via `Depends`. |

## Run
```bash
# Tests (no docker needed)
pytest tests/ -v

# Migrations
alembic upgrade head
```

## Domains (worker tracking)

| Domain | Service dir | Router |
|---|---|---|
| terminals | `services/terminals/` | `routers/terminals.py` |
| zones | `services/zones/` | routes nested under terminals router |
| sectors | `services/sectors/` | routes nested under zones router |
| cameras | `services/cameras/` | `routers/cameras.py` |
| employees | `services/employees/` | `routers/employees.py` |
| sensor_positions | `services/sensor_positions/` | `routers/sensor_positions.py` |
| camera_events | `services/camera_events/` | `routers/camera_events.py` |
| matching | `services/matching/` | (internal, no router) |
| actions | `services/actions/` | (internal, no router) |
| annotations | `services/annotations/` | `routers/annotations.py` |

## Shared utilities
- `services/geo/point_in_polygon.py` — pure function, no DB dependency
- `app/config.py` — module-level constants (CONFIDENCE_THRESHOLD, TIME_WINDOW_SECONDS)

## REST URL conventions
- Nested resources use nested paths: `/api/terminals/{id}/zones/`, `/api/zones/{id}/sectors/`
- Flat collection operations: `/api/cameras/`, `/api/employees/`
- Ingestion endpoints (write-only): `/api/sensor-positions/`, `/api/camera-events/`
- Analytics: `/api/analytics/heatmap`, `/api/analytics/zones`, `/api/analytics/employees/{id}`
