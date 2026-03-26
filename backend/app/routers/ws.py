from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.redis import subscribe

router = APIRouter()


@router.websocket("/live")
async def live_feed(websocket: WebSocket):
    await websocket.accept()
    try:
        async for message in subscribe("events"):
            await websocket.send_text(message)
    except WebSocketDisconnect:
        pass


@router.websocket("/positions")
async def positions_feed(websocket: WebSocket):
    await websocket.accept()
    try:
        async for message in subscribe("positions"):
            await websocket.send_text(message)
    except WebSocketDisconnect:
        pass
