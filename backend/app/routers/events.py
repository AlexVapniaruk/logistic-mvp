from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.event import EventCreateSchema, EventFilterSchema, EventReadSchema
from app.services.events.get_events_list_service import GetEventsListService
from app.services.events.get_event_service import GetEventService
from app.services.events.create_event_service import CreateEventService

router = APIRouter()


@router.get("/", response_model=list[EventReadSchema])
async def list_events(filters: EventFilterSchema = Depends(), db: AsyncSession = Depends(get_db)):
    return await GetEventsListService(db).execute(filters)


@router.get("/{event_id}", response_model=EventReadSchema)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    return await GetEventService(db).execute(event_id)


@router.post("/", response_model=EventReadSchema, status_code=201)
async def create_event(payload: EventCreateSchema, db: AsyncSession = Depends(get_db)):
    return await CreateEventService(db).execute(payload)
