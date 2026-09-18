import logging
from sqlalchemy.orm import Session
from app.db.models import Senior, LocationEvent
from app.utils.distance import haversine_distance
from app.services.notification_service import create_notification
from app.services.escalation_service import notify_family_members

logger = logging.getLogger(__name__)

def update_senior_location(
    db: Session,
    senior_id: int,
    latitude: float,
    longitude: float,
    expected_trip: bool = False
) -> LocationEvent:
    senior = db.query(Senior).filter(Senior.id == senior_id).first()
    if not senior:
        raise ValueError(f"Senior with ID {senior_id} not found.")

    # Update senior's current position
    senior.latitude = latitude
    senior.longitude = longitude

    # Check deviation from home location
    is_deviation = False
    if senior.home_latitude and senior.home_longitude:
        dist_from_home = haversine_distance(latitude, longitude, senior.home_latitude, senior.home_longitude)
        threshold = senior.location_deviation_threshold_km or 1.0
        if dist_from_home > threshold:
            is_deviation = True

    event = LocationEvent(
        senior_id=senior_id,
        latitude=latitude,
        longitude=longitude,
        is_deviation=is_deviation,
        expected_trip=expected_trip
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # If deviation detected and NOT an expected trip, raise notification
    if is_deviation and not expected_trip:
        logger.warning(f"LOCATION DEVIATION DETECTED for Senior {senior_id} ({dist_from_home:.2f}km from home)")
        
        # Notify caretaker
        from app.db.models import CaretakerSenior, Caretaker
        assoc = db.query(CaretakerSenior).filter(CaretakerSenior.senior_id == senior_id, CaretakerSenior.is_primary == True).first()
        if assoc:
            caretaker = db.query(Caretaker).filter(Caretaker.id == assoc.caretaker_id).first()
            if caretaker:
                create_notification(
                    db=db,
                    user_id=caretaker.user_id,
                    notification_type="LOCATION_DEVIATION",
                    title="Location Deviation Alert",
                    message=f"Senior ID {senior.id} has moved outside safe boundary ({dist_from_home:.2f}km from home).",
                    request_id=None
                )
        
        # Notify family
        notify_family_members(
            db=db,
            senior_id=senior_id,
            request_id=None,
            title="Location Boundary Alert",
            message=f"Senior ID {senior.id} location deviation detected."
        )

    return event
