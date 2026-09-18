# NEARHAND Database Layer

**"The right help. At the right time. For every senior."**

This folder contains the complete, reliable, production-ready database layer for **NEARHAND**, designed for SQLite (MVP) and ready for seamless PostgreSQL migration.

---

## 🏗️ Architecture & Entities

The database consists of **14 tables** supporting the complete NEARHAND emergency & care coordination workflow:

```text
Senior Request → AI Analysis → Urgency → Caretaker Notification → Response Monitoring → Caretaker Timeout → Volunteer Fallback → Family Notification → Resolution
```

### Tables Overview
1. `users`: System users with roles (`SENIOR`, `CARETAKER`, `VOLUNTEER`, `FAMILY`, `ADMIN`), hashed passwords, unique email constraints.
2. `seniors`: Senior profile, age, gender, preferred language, home coordinates, deviation threshold km.
3. `caretakers`: Caretaker status (`AVAILABLE`, `BUSY`, `OFFLINE`), location, `max_seniors` limit (default: 5), current load.
4. `caretaker_seniors`: Many-to-many historical & active primary caretaker assignment records.
5. `volunteers`: Independently enrolled emergency fallback volunteers, max distance radius, skills, first-aid certification.
6. `family_members`: Family contacts connected to seniors with explicit access control permissions (`can_receive_emergency_alerts`, `can_view_health`, `can_view_location`).
7. `medical_records`: Health conditions, allergies, blood group, critical notes.
8. `medications`: Prescription schedules, daily tracking (`taken_today`, `last_taken_at`).
9. `requests`: Core emergency/assistance table storing input type (`TEXT`, `AUDIO`, `SOS`), request type, urgency (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), AI priority risk score (0–100), AI boolean flags, target response window, and status.
10. `assignments`: Responder dispatch tracking (`CARETAKER`, `VOLUNTEER`, `ADDITIONAL_CARETAKER`), deadlines, ETA, and acceptance/rejection timestamps.
11. `notifications`: Alert records (`EMERGENCY`, `REQUEST`, `ESCALATION`, `LOCATION`, `MEDICATION`, `FAMILY`, `SYSTEM`) with read status.
12. `location_events`: Geolocation tracking, home distance calculations, and deviation flags.
13. `companionship_requests`: Non-emergency companionship request management.
14. `audit_logs`: Event auditing for security, escalations, and system actions.

---

## 🚀 Quickstart & CLI Commands

### 1. Installation
Install dependencies:
```bash
pip install -r database/requirements.txt
```

### 2. Initialize & Seed Database
To create all database tables and populate fictional demo data (Lakshmi, Caretaker Ravi Kumar with 5 seniors, Volunteer Priya Sharma, Anjali, Telugu fall request demo, medications, location events):
```bash
python -m app.seed
```
*(Or run `python database/app/seed.py` from project root)*

### 3. Development Database Reset
To wipe the SQLite database and re-seed clean demo data:
```bash
python reset_database.py
```

### 4. Run Unit Tests
Run the comprehensive test suite verifying constraints, relationships, and workflow transitions:
```bash
python -m pytest tests/
```

---

## 🔌 Integration Guide for Member 2 (FastAPI Backend)

Member 2 can easily connect to this database layer either by copying the `database/app/` folder into `backend/app/db/` or by referencing it directly.

### Copying into Backend Application:
```text
backend/
    app/
        db/
            __init__.py
            database.py
            models.py
            schemas.py
            crud.py
            seed.py
            config.py
            relationships.py
```

### 1. Database Connection & Session Setup
In `backend/app/db/database.py` (or main API entrypoint):
```python
from app.db.database import get_db, SessionLocal, engine, init_db
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Session dependency for route handlers
@app.get("/api/seniors/{senior_id}")
def get_senior_endpoint(senior_id: int, db: Session = Depends(get_db)):
    # ...
```

### 2. Importing Models & Schemas
```python
from app.db.models import User, Senior, Request, RequestStatus, UrgencyLevel
from app.db.schemas import UserOut, RequestCreate, RequestOut
import app.db.crud as crud
```

### 3. Typical API Usage Examples

#### Creating an AI-Analyzed Request:
```python
@app.post("/api/requests", response_model=RequestOut)
def create_senior_request(request_data: RequestCreate, db: Session = Depends(get_db)):
    new_request = crud.create_request(
        db,
        senior_id=request_data.senior_id,
        message=request_data.message,
        input_type=request_data.input_type,
        language=request_data.language,
        request_type=request_data.request_type,
        urgency=request_data.urgency,
        risk_score=request_data.risk_score,
        emergency=request_data.emergency,
        fall_detected=request_data.fall_detected,
        target_response_minutes=request_data.target_response_minutes,
        ai_analysis_json=request_data.ai_analysis_json
    )
    return new_request
```

#### Dispatching Notification & Tracking Caretaker Timeout:
```python
@app.post("/api/requests/{request_id}/notify-caretaker")
def notify_caretaker(request_id: int, db: Session = Depends(get_db)):
    req = crud.get_request(db, request_id)
    caretaker = crud.get_senior_caretaker(db, req.senior_id)
    if caretaker:
        # Create assignment & notification
        assignment = crud.create_assignment(
            db, request_id=req.id, responder_type="CARETAKER",
            responder_id=caretaker.user_id, assignment_status="PENDING"
        )
        crud.create_notification(
            db, user_id=caretaker.user_id, request_id=req.id,
            notification_type="EMERGENCY", title="CRITICAL ALERT", message=req.message
        )
        crud.update_request_status(db, req.id, status="CARETAKER_NOTIFIED")
    return {"status": "CARETAKER_NOTIFIED"}
```

#### Escalating to Volunteer on Caretaker Timeout:
```python
@app.post("/api/requests/{request_id}/timeout-escalate")
def timeout_escalate(request_id: int, db: Session = Depends(get_db)):
    req = crud.get_request(db, request_id)
    senior = crud.get_senior(db, req.senior_id)
    
    # Find nearby available volunteer
    volunteers = crud.get_volunteers_near_location(
        db, latitude=senior.latitude, longitude=senior.longitude, max_distance_km=10.0
    )
    if volunteers:
        chosen_vol = volunteers[0]
        crud.create_assignment(
            db, request_id=req.id, responder_type="VOLUNTEER",
            responder_id=chosen_vol.user_id, assignment_status="PENDING"
        )
        crud.update_request_status(db, req.id, status="VOLUNTEER_NOTIFIED")
    return {"status": "VOLUNTEER_NOTIFIED"}
```

---

## ⚙️ Environment Configuration

Set database URL in `.env`:
```env
DATABASE_URL=sqlite:///./nearthand.db
DEFAULT_MAX_CARETAKER_SENIORS=5
```

For production PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/nearhand_db
```
