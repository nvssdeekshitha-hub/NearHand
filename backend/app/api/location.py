from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Senior, LocationEvent
from app.schemas.location import LocationUpdate, LocationCheck
from app.schemas.common import success_response, error_response
from app.services.location_service import update_senior_location

router = APIRouter(prefix="/location", tags=["Location Deviation"])

@router.post("/update")
def post_location_update(payload: LocationUpdate, db: Session = Depends(get_db)):
    senior_id = payload.senior_id or 1
    event = update_senior_location(
        db=db,
        senior_id=senior_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        expected_trip=payload.expected_trip
    )

    return success_response(
        data={
            "event_id": event.id,
            "senior_id": event.senior_id,
            "latitude": event.latitude,
            "longitude": event.longitude,
            "is_deviation": event.is_deviation,
            "expected_trip": event.expected_trip,
            "timestamp": event.timestamp.isoformat() if event.timestamp else None
        },
        message="Location updated"
    )

@router.get("/{senior_id}")
def get_senior_location(senior_id: int, db: Session = Depends(get_db)):
    senior = db.query(Senior).filter(Senior.id == senior_id).first()
    if not senior:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Senior {senior_id} not found."))

    latest_event = db.query(LocationEvent).filter(
        LocationEvent.senior_id == senior_id
    ).order_by(LocationEvent.id.desc()).first()

    return success_response(
        data={
            "senior_id": senior.id,
            "current_latitude": senior.latitude,
            "current_longitude": senior.longitude,
            "home_latitude": senior.home_latitude,
            "home_longitude": senior.home_longitude,
            "location_deviation_threshold_km": senior.location_deviation_threshold_km,
            "latest_event": {
                "id": latest_event.id,
                "is_deviation": latest_event.is_deviation,
                "expected_trip": latest_event.expected_trip,
                "timestamp": latest_event.timestamp.isoformat()
            } if latest_event else None
        },
        message="Senior location retrieved"
    )

@router.post("/check-deviation")
def check_location_deviation(payload: LocationCheck, db: Session = Depends(get_db)):
    event = update_senior_location(
        db=db,
        senior_id=payload.senior_id,
        latitude=payload.current_latitude,
        longitude=payload.current_longitude,
        expected_trip=payload.expected_trip
    )

    return success_response(
        data={
            "is_deviation": event.is_deviation,
            "expected_trip": event.expected_trip,
            "action_taken": "Caregiver notified of deviation" if event.is_deviation and not event.expected_trip else "Normal tracking"
        },
        message="Location deviation status checked"
    )
