from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_, or_, desc
import app.models as models
import app.relationships  # Ensure relationships are registered


# ==========================================
# USER CRUD
# ==========================================

def create_user(
    db: Session,
    name: str,
    email: str,
    password_hash: str,
    role: models.UserRole,
    phone: Optional[str] = None
) -> models.User:
    user = models.User(
        name=name,
        email=email.lower().strip(),
        phone=phone,
        password_hash=password_hash,
        role=role,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email.lower().strip()).first()


# ==========================================
# SENIOR CRUD
# ==========================================

def create_senior(
    db: Session,
    user_id: int,
    age: int,
    gender: Optional[str] = None,
    preferred_language: str = "English",
    address: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    home_latitude: Optional[float] = None,
    home_longitude: Optional[float] = None,
    location_deviation_threshold_km: float = 0.5,
    emergency_contact: Optional[str] = None
) -> models.Senior:
    senior = models.Senior(
        user_id=user_id,
        age=age,
        gender=gender,
        preferred_language=preferred_language,
        address=address,
        latitude=latitude,
        longitude=longitude,
        home_latitude=home_latitude if home_latitude is not None else latitude,
        home_longitude=home_longitude if home_longitude is not None else longitude,
        location_deviation_threshold_km=location_deviation_threshold_km,
        emergency_contact=emergency_contact
    )
    db.add(senior)
    db.commit()
    db.refresh(senior)
    return senior


def get_senior(db: Session, senior_id: int) -> Optional[models.Senior]:
    return db.query(models.Senior).filter(models.Senior.id == senior_id).first()


def get_senior_by_user_id(db: Session, user_id: int) -> Optional[models.Senior]:
    return db.query(models.Senior).filter(models.Senior.user_id == user_id).first()


def get_senior_health(db: Session, senior_id: int) -> dict:
    senior = get_senior(db, senior_id)
    if not senior:
        return {}
    records = db.query(models.MedicalRecord).filter(models.MedicalRecord.senior_id == senior_id).all()
    medications = db.query(models.Medication).filter(models.Medication.senior_id == senior_id).all()
    return {
        "senior_id": senior_id,
        "medical_records": records,
        "medications": medications
    }


def get_senior_caretaker(db: Session, senior_id: int) -> Optional[models.Caretaker]:
    link = db.query(models.CaretakerSenior).filter(
        models.CaretakerSenior.senior_id == senior_id,
        models.CaretakerSenior.ended_at.is_(None)
    ).first()
    if link:
        return db.query(models.Caretaker).filter(models.Caretaker.id == link.caretaker_id).first()
    return None


def get_senior_family(db: Session, senior_id: int) -> List[models.FamilyMember]:
    return db.query(models.FamilyMember).filter(models.FamilyMember.senior_id == senior_id).all()


# ==========================================
# CARETAKER CRUD & ASSIGNMENTS
# ==========================================

def create_caretaker(
    db: Session,
    user_id: int,
    availability_status: models.AvailabilityStatus = models.AvailabilityStatus.AVAILABLE,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    max_seniors: int = 5
) -> models.Caretaker:
    caretaker = models.Caretaker(
        user_id=user_id,
        availability_status=availability_status,
        latitude=latitude,
        longitude=longitude,
        max_seniors=max_seniors,
        current_load=0
    )
    db.add(caretaker)
    db.commit()
    db.refresh(caretaker)
    return caretaker


def assign_senior_to_caretaker(
    db: Session,
    caretaker_id: int,
    senior_id: int,
    is_primary: bool = True
) -> models.CaretakerSenior:
    caretaker = db.query(models.Caretaker).filter(models.Caretaker.id == caretaker_id).first()
    if not caretaker:
        raise ValueError("Caretaker not found")
    
    # Close any existing active caretaker links for this senior if setting primary
    if is_primary:
        db.query(models.CaretakerSenior).filter(
            models.CaretakerSenior.senior_id == senior_id,
            models.CaretakerSenior.ended_at.is_(None)
        ).update({"ended_at": datetime.now(timezone.utc)})
    
    link = models.CaretakerSenior(
        caretaker_id=caretaker_id,
        senior_id=senior_id,
        is_primary=is_primary,
        assigned_at=datetime.now(timezone.utc)
    )
    db.add(link)
    
    # Recalculate caretaker active load
    active_count = db.query(models.CaretakerSenior).filter(
        models.CaretakerSenior.caretaker_id == caretaker_id,
        models.CaretakerSenior.ended_at.is_(None)
    ).count() + 1
    caretaker.current_load = active_count
    
    db.commit()
    db.refresh(link)
    return link


def get_caretaker_seniors(db: Session, caretaker_id: int) -> List[models.Senior]:
    links = db.query(models.CaretakerSenior).filter(
        models.CaretakerSenior.caretaker_id == caretaker_id,
        models.CaretakerSenior.ended_at.is_(None)
    ).all()
    senior_ids = [link.senior_id for link in links]
    if not senior_ids:
        return []
    return db.query(models.Senior).filter(models.Senior.id.in_(senior_ids)).all()


def get_available_caretakers(db: Session) -> List[models.Caretaker]:
    return db.query(models.Caretaker).filter(
        models.Caretaker.availability_status == models.AvailabilityStatus.AVAILABLE,
        models.Caretaker.current_load < models.Caretaker.max_seniors
    ).all()


# ==========================================
# VOLUNTEER CRUD
# ==========================================

def create_volunteer(
    db: Session,
    user_id: int,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    availability_status: models.AvailabilityStatus = models.AvailabilityStatus.AVAILABLE,
    max_distance_km: float = 10.0,
    skills: Optional[str] = None,
    first_aid_trained: bool = False
) -> models.Volunteer:
    volunteer = models.Volunteer(
        user_id=user_id,
        latitude=latitude,
        longitude=longitude,
        availability_status=availability_status,
        max_distance_km=max_distance_km,
        skills=skills,
        first_aid_trained=first_aid_trained,
        current_active_requests=0
    )
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer


def get_available_volunteers(db: Session) -> List[models.Volunteer]:
    return db.query(models.Volunteer).filter(
        models.Volunteer.availability_status == models.AvailabilityStatus.AVAILABLE
    ).all()


def get_volunteers_near_location(
    db: Session,
    latitude: float,
    longitude: float,
    max_distance_km: float = 10.0
) -> List[models.Volunteer]:
    # Query available volunteers (in a real DB, spatial extension can be used; here we filter by status and active threshold)
    volunteers = get_available_volunteers(db)
    # Filter volunteers within bounds (simple approximation: 1 deg lat/lng ~ 111 km)
    nearby = []
    for vol in volunteers:
        if vol.latitude is not None and vol.longitude is not None:
            d_lat = abs(vol.latitude - latitude) * 111.0
            d_lng = abs(vol.longitude - longitude) * 111.0
            approx_dist = (d_lat**2 + d_lng**2)**0.5
            if approx_dist <= max_distance_km and approx_dist <= vol.max_distance_km:
                nearby.append(vol)
    return nearby


# ==========================================
# REQUEST CRUD
# ==========================================

def create_request(
    db: Session,
    senior_id: int,
    message: str,
    input_type: models.InputType = models.InputType.TEXT,
    language: Optional[str] = "English",
    request_type: models.RequestType = models.RequestType.GENERAL_HELP,
    urgency: models.UrgencyLevel = models.UrgencyLevel.LOW,
    risk_score: int = 0,
    emergency: bool = False,
    potential_emergency: bool = False,
    fall_detected: bool = False,
    mobility_issue: bool = False,
    medical_attention_possible: bool = False,
    required_support: Optional[str] = None,
    location_relevant: bool = False,
    location_context: Optional[str] = None,
    companionship: bool = False,
    status: models.RequestStatus = models.RequestStatus.CREATED,
    target_response_minutes: int = 10,
    ai_analysis_json: Optional[str] = None
) -> models.Request:
    # Ensure risk_score is within 0-100
    risk_score = max(0, min(100, risk_score))
    
    req = models.Request(
        senior_id=senior_id,
        message=message,
        input_type=input_type,
        language=language,
        request_type=request_type,
        urgency=urgency,
        risk_score=risk_score,
        emergency=emergency,
        potential_emergency=potential_emergency,
        fall_detected=fall_detected,
        mobility_issue=mobility_issue,
        medical_attention_possible=medical_attention_possible,
        required_support=required_support,
        location_relevant=location_relevant,
        location_context=location_context,
        companionship=companionship,
        status=status,
        target_response_minutes=target_response_minutes,
        ai_analysis_json=ai_analysis_json
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


def get_request(db: Session, request_id: int) -> Optional[models.Request]:
    return db.query(models.Request).filter(models.Request.id == request_id).first()


def update_request_status(
    db: Session,
    request_id: int,
    status: models.RequestStatus,
    resolved: bool = False
) -> Optional[models.Request]:
    req = get_request(db, request_id)
    if not req:
        return None
    req.status = status
    if resolved or status == models.RequestStatus.RESOLVED:
        req.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(req)
    return req


def get_senior_requests(db: Session, senior_id: int) -> List[models.Request]:
    return db.query(models.Request).filter(
        models.Request.senior_id == senior_id
    ).order_by(desc(models.Request.created_at)).all()


# ==========================================
# ASSIGNMENT CRUD
# ==========================================

def create_assignment(
    db: Session,
    request_id: int,
    responder_type: models.ResponderType,
    responder_id: int,
    assignment_status: models.AssignmentStatus = models.AssignmentStatus.PENDING,
    distance_km: Optional[float] = None,
    eta_minutes: Optional[int] = None,
    response_deadline: Optional[datetime] = None
) -> models.Assignment:
    assignment = models.Assignment(
        request_id=request_id,
        responder_type=responder_type,
        responder_id=responder_id,
        assignment_status=assignment_status,
        distance_km=distance_km,
        eta_minutes=eta_minutes,
        response_deadline=response_deadline,
        assigned_at=datetime.now(timezone.utc)
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def get_request_assignments(db: Session, request_id: int) -> List[models.Assignment]:
    return db.query(models.Assignment).filter(
        models.Assignment.request_id == request_id
    ).order_by(desc(models.Assignment.created_at)).all()


def update_assignment(
    db: Session,
    assignment_id: int,
    assignment_status: models.AssignmentStatus
) -> Optional[models.Assignment]:
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        return None
    assignment.assignment_status = assignment_status
    if assignment_status == models.AssignmentStatus.ACCEPTED:
        assignment.accepted_at = datetime.now(timezone.utc)
    elif assignment_status == models.AssignmentStatus.REJECTED:
        assignment.rejected_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(assignment)
    return assignment


# ==========================================
# NOTIFICATION CRUD
# ==========================================

def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: models.NotificationType = models.NotificationType.SYSTEM,
    request_id: Optional[int] = None
) -> models.Notification:
    notif = models.Notification(
        user_id=user_id,
        request_id=request_id,
        type=notification_type,
        title=title,
        message=message,
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def get_user_notifications(db: Session, user_id: int, unread_only: bool = False) -> List[models.Notification]:
    query = db.query(models.Notification).filter(models.Notification.user_id == user_id)
    if unread_only:
        query = query.filter(models.Notification.is_read == False)
    return query.order_by(desc(models.Notification.created_at)).all()


def mark_notification_read(db: Session, notification_id: int) -> Optional[models.Notification]:
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if notif:
        notif.is_read = True
        notif.read_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(notif)
    return notif


# ==========================================
# LOCATION EVENT CRUD
# ==========================================

def create_location_event(
    db: Session,
    senior_id: int,
    latitude: float,
    longitude: float,
    distance_from_home_km: float = 0.0,
    deviation_detected: bool = False,
    expected_trip: bool = False
) -> models.LocationEvent:
    event = models.LocationEvent(
        senior_id=senior_id,
        latitude=latitude,
        longitude=longitude,
        distance_from_home_km=distance_from_home_km,
        deviation_detected=deviation_detected,
        expected_trip=expected_trip
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_latest_location(db: Session, senior_id: int) -> Optional[models.LocationEvent]:
    return db.query(models.LocationEvent).filter(
        models.LocationEvent.senior_id == senior_id
    ).order_by(desc(models.LocationEvent.created_at)).first()


# ==========================================
# AUDIT LOG & OTHER HELPERS
# ==========================================

def create_audit_log(
    db: Session,
    action: str,
    entity_type: str,
    user_id: Optional[int] = None,
    entity_id: Optional[str] = None,
    details: Optional[str] = None
) -> models.AuditLog:
    log = models.AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
