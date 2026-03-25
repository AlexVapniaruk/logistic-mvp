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
