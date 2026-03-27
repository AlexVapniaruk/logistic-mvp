from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.redis import init_redis, close_redis
from app.routers import events, analytics, training, ws
from app.routers import (
    terminals,
    zones,
    sectors,
    cameras,
    employees,
    sensor_positions,
    camera_events,
    annotations,
    worker_analytics,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    yield
    await close_redis()


app = FastAPI(title="Logistics Terminal API", lifespan=lifespan)

app.mount("/uploads", StaticFiles(directory="/app/uploads", check_dir=False), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(training.router, prefix="/api/training", tags=["training"])
app.include_router(ws.router, prefix="/ws", tags=["websocket"])
app.include_router(terminals.router, prefix="/api/terminals", tags=["terminals"])
app.include_router(zones.router, prefix="/api/zones", tags=["zones"])
app.include_router(sectors.router, prefix="/api/sectors", tags=["sectors"])
app.include_router(cameras.router, prefix="/api/cameras", tags=["cameras"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(sensor_positions.router, prefix="/api/sensor-positions", tags=["sensor-positions"])
app.include_router(camera_events.router, prefix="/api/camera-events", tags=["camera-events"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["annotations"])
app.include_router(worker_analytics.router, prefix="/api/analytics", tags=["worker-analytics"])


@app.get("/health")
async def health():
    return {"status": "ok"}
