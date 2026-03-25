# Logistics Terminal MVP

YOLO-based action detection system for logistics terminal monitoring.

## Stack
- **Frontend**: Nuxt 3 + TypeScript + Pinia + Tailwind (port 3000)
- **Backend**: FastAPI + SQLAlchemy async + Pydantic v2 + aioredis (port 8000)
- **DB**: PostgreSQL 15 (port 5432)
- **Cache/PubSub**: Redis 7 (port 6379)

## Principles
KISS · DRY · YAGNI · SOLID · Clean Code · Clean Architecture (Martin)

## Run
```bash
docker-compose up --build
```

## Env
Copy `.env.example` → `.env` and fill values.

## Layer docs
- Frontend rules → `frontend/CLAUDE.md`
- Backend rules → `backend/CLAUDE.md`
