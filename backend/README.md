# NearHand Backend API & WebSockets

NearHand Backend API is a FastAPI-based backend for Senior Coordination, AI Urgency Analysis, and Emergency Escalation.

## Tech Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (HS256)
- **Real-Time**: WebSockets (`/ws/{user_id}`)

## Quick Start

### 1. Install Dependencies & Seed Database
```bash
pip install -r requirements.txt
python -m app.db.seed
```

### 2. Run API Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Swagger Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## WebSockets Integration (`/ws/{user_id}`)

NearHand supports real-time event streaming via WebSockets at `ws://localhost:8000/ws/{user_id}`.

### Event Format
All WebSocket events conform to the standard structure:
```json
{
  "event": "EVENT_NAME",
  "data": { ... }
}
```

### Supported Events
1. `REQUEST_CREATED` — Emitted to senior upon initial request submission.
2. `AI_ANALYSIS_COMPLETE` — Emitted to senior after AI urgency classification.
3. `CARETAKER_NOTIFIED` — Emitted to primary caretaker when assigned.
4. `CARETAKER_ACCEPTED` — Emitted to senior and family when caretaker accepts.
5. `CARETAKER_TIMEOUT` — Emitted to senior when caretaker response deadline expires.
6. `VOLUNTEERS_NOTIFIED` — Emitted to nearby matched volunteer(s).
7. `VOLUNTEER_ACCEPTED` — Emitted to senior and family when volunteer accepts.
8. `FAMILY_NOTIFIED` — Emitted to family members on escalation.
9. `REQUEST_RESOLVED` — Emitted to senior, caretaker, volunteer, and family upon completion.
10. `LOCATION_DEVIATION` — Emitted to caretaker on senior geofence deviation.

---

## Testing WebSockets via Python Client

Install `websockets`:
```bash
pip install websockets
```

Run test script `test_websocket.py`:
```python
import asyncio
import websockets
import json

async def listen():
    uri = "ws://localhost:8000/ws/2" # Listen as Senior Lakshmi (User ID 2)
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server as User 2...")
        while True:
            msg = await websocket.recv()
            print("Received WS Event:", json.dumps(json.loads(msg), indent=2))

if __name__ == "__main__":
    asyncio.run(listen())
```
