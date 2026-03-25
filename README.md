# Logistics Terminal MVP

YOLO-based action detection and monitoring for logistics terminals.

## Quick start

```bash
cp .env.example .env
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

## Development

```bash
# Backend tests (no docker needed)
cd backend
pip install -r requirements-dev.txt
pytest tests/ -v

# Frontend dev server
cd frontend
npm install
npm run dev

# Run DB migrations
cd backend
alembic upgrade head
```

## Architecture

See `CLAUDE.md`, `frontend/CLAUDE.md`, and `backend/CLAUDE.md` for layer rules and conventions.
