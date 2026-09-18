import asyncio
import logging
from typing import Dict, List, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

# Reference to the main asyncio event loop
main_loop: Optional[asyncio.AbstractEventLoop] = None

def set_main_loop(loop: asyncio.AbstractEventLoop):
    global main_loop
    main_loop = loop
    logger.info("WebSocket main event loop reference configured.")

class ConnectionManager:
    """
    WebSocket connection manager supporting targeted messages per user_id.
    """
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"WebSocket client connected for User ID {user_id}. Active sockets for user: {len(self.active_connections[user_id])}")

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"WebSocket client disconnected for User ID {user_id}")

    async def send_personal_message(self, user_id: int, event_name: str, data: dict):
        """
        Sends formatted JSON event `{"event": event_name, "data": data}` to all open sockets for user_id.
        Fails silently if user is not connected or socket errors occur.
        """
        if user_id not in self.active_connections or not self.active_connections[user_id]:
            logger.info(f"[WS SEND SKIPPED] User ID {user_id} has no active WebSocket connections. Event '{event_name}' not delivered.")
            return

        payload = {
            "event": event_name,
            "data": data
        }

        logger.info(f"[WS SENDING] Delivering '{event_name}' to {len(self.active_connections[user_id])} socket(s) for User ID {user_id}...")

        dead_sockets = []
        for ws in list(self.active_connections[user_id]):
            try:
                await ws.send_json(payload)
                logger.info(f"[WS DELIVERED] Event '{event_name}' successfully sent to User ID {user_id}")
            except Exception as e:
                logger.warning(f"[WS SEND ERROR] Failed to send WS message to User ID {user_id}: {e}")
                dead_sockets.append(ws)

        for ws in dead_sockets:
            self.disconnect(user_id, ws)

manager = ConnectionManager()

def emit_ws_event(user_id: int, event_name: str, data: dict):
    """
    Thread-safe & async-safe helper to trigger WS event from sync or async code.
    Dispatches to main event loop via run_coroutine_threadsafe if called from worker thread pool.
    """
    logger.info(f"[WS EMIT TRIGGERED] Event: '{event_name}' -> Target User ID: {user_id}")
    
    # 1. Try to schedule on current running loop (if calling from main async thread)
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(manager.send_personal_message(user_id, event_name, data))
        logger.info(f"[WS EMIT SUCCESS] Task scheduled on active loop for User ID {user_id}")
        return
    except RuntimeError:
        pass

    # 2. If calling from a synchronous worker thread pool, schedule via main_loop reference
    global main_loop
    if main_loop and main_loop.is_running():
        asyncio.run_coroutine_threadsafe(
            manager.send_personal_message(user_id, event_name, data),
            main_loop
        )
        logger.info(f"[WS EMIT SUCCESS] Coroutine scheduled via threadsafe on main_loop for User ID {user_id}")
    else:
        # Fallback: attempt to get or create event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    manager.send_personal_message(user_id, event_name, data),
                    loop
                )
                logger.info(f"[WS EMIT SUCCESS] Coroutine scheduled via fallback loop for User ID {user_id}")
            else:
                logger.warning(f"[WS EMIT FAILED] Event loop is not running. Could not deliver '{event_name}' to User ID {user_id}")
        except Exception as e:
            logger.error(f"[WS EMIT ERROR] Failed to schedule WS event '{event_name}' for User ID {user_id}: {e}")

router = APIRouter(tags=["WebSockets"])

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Ensure main_loop reference is captured when first socket connects
    global main_loop
    if main_loop is None:
        try:
            set_main_loop(asyncio.get_running_loop())
        except Exception:
            pass

    await manager.connect(user_id, websocket)
    try:
        await websocket.send_json({
            "event": "CONNECTED",
            "data": {
                "user_id": user_id,
                "message": f"Successfully connected to NearHand real-time event stream as user {user_id}"
            }
        })
        while True:
            data = await websocket.receive_text()
            # Echo back ping/pong for connection verification
            await websocket.send_json({"event": "PONG", "data": {"received": data}})
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
    except Exception as e:
        logger.error(f"WebSocket error for User ID {user_id}: {e}")
        manager.disconnect(user_id, websocket)
