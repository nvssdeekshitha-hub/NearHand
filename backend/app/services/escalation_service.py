from datetime import datetime, timezone
import logging
from sqlalchemy.orm import Session

from app.db.models import (
    Request, Assignment, Senior, Caretaker, CaretakerSenior, Volunteer, Family,
    RequestStatus, AssignmentStatus, ResponderType
)
from app.services.matching_service import find_best_volunteers
from app.services.notification_service import create_notification
from app.api.websocket import emit_ws_event

logger = logging.getLogger(__name__)

def handle_caretaker_timeout(db: Session, request_id: int) -> Request:
    """
    Executes caretaker timeout escalation:
    Status -> CARETAKER_TIMEOUT -> search volunteers -> status -> VOLUNTEER_NOTIFIED (or ESCALATED if none).
    Emits CARETAKER_TIMEOUT to senior, and VOLUNTEERS_NOTIFIED to candidate volunteer(s).
    """
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        logger.error(f"Request {request_id} not found for timeout handler.")
        return None

    # Check if request is still waiting for caretaker
    if req.status not in [RequestStatus.CARETAKER_NOTIFIED.value, RequestStatus.WAITING_FOR_ACKNOWLEDGEMENT.value, RequestStatus.PRIORITIZED.value]:
        logger.info(f"Request {request_id} is in status '{req.status}', timeout ignored.")
        return req

    senior = db.query(Senior).filter(Senior.id == req.senior_id).first()

    # Mark current pending caretaker assignment as TIMEOUT
    pending_assignment = db.query(Assignment).filter(
        Assignment.request_id == request_id,
        Assignment.assignment_status == AssignmentStatus.PENDING.value
    ).first()

    if pending_assignment:
        pending_assignment.assignment_status = AssignmentStatus.TIMEOUT.value

    req.status = RequestStatus.CARETAKER_TIMEOUT.value
    db.commit()

    # 5. Emit WS Event: CARETAKER_TIMEOUT (to senior)
    if senior:
        emit_ws_event(
            user_id=senior.user_id,
            event_name="CARETAKER_TIMEOUT",
            data={
                "request_id": req.id,
                "senior_id": senior.id,
                "status": req.status,
                "message": "Caretaker response window expired. Searching volunteer network..."
            }
        )

    # Query senior and find best volunteer match
    candidates = find_best_volunteers(db=db, senior=senior, request=req, limit=1)

    if candidates:
        top_volunteer = candidates[0]
        # Create assignment for volunteer
        assignment = Assignment(
            request_id=req.id,
            responder_type=ResponderType.VOLUNTEER.value,
            responder_id=top_volunteer["volunteer_id"],
            assignment_status=AssignmentStatus.PENDING.value,
            assigned_at=datetime.now(timezone.utc),
            distance_km=top_volunteer["distance_km"],
            eta_minutes=top_volunteer["eta_minutes"]
        )
        db.add(assignment)
        
        req.status = RequestStatus.VOLUNTEER_NOTIFIED.value
        db.commit()
        db.refresh(req)

        # 6. Emit WS Event: VOLUNTEERS_NOTIFIED (to volunteer user)
        emit_ws_event(
            user_id=top_volunteer["user_id"],
            event_name="VOLUNTEERS_NOTIFIED",
            data={
                "request_id": req.id,
                "volunteer_id": top_volunteer["volunteer_id"],
                "senior_id": senior.id if senior else None,
                "distance_km": top_volunteer["distance_km"],
                "eta_minutes": top_volunteer["eta_minutes"],
                "skills": top_volunteer["skills"]
            }
        )

        create_notification(
            db=db,
            user_id=top_volunteer["user_id"],
            notification_type="VOLUNTEER_NOTIFIED",
            title="Urgent Care Assistance Request",
            message=f"Urgent assistance needed for Senior ID {senior.id} (~{top_volunteer['distance_km']}km away, ETA {top_volunteer['eta_minutes']} min).",
            request_id=req.id
        )
        logger.info(f"Volunteer {top_volunteer['name']} notified for request {req.id}.")
    else:
        # Escalated to family/emergency if no volunteer available
        req.status = RequestStatus.ESCALATED.value
        db.commit()
        db.refresh(req)
        
        # Notify family members
        notify_family_members(db=db, senior_id=senior.id, request_id=req.id, title="CRITICAL ESCALATION", message="No primary caretaker or volunteer acknowledged request.")

    return req

def notify_family_members(db: Session, senior_id: int, request_id: int, title: str, message: str):
    """
    Sends emergency notifications to all family members registered for senior.
    Emits FAMILY_NOTIFIED WS event to each family member.
    """
    family_list = db.query(Family).filter(Family.senior_id == senior_id).all()
    for f in family_list:
        create_notification(
            db=db,
            user_id=f.user_id,
            notification_type="FAMILY_NOTIFIED",
            title=title,
            message=message,
            request_id=request_id,
            extra_data={"senior_id": senior_id}
        )

def notify_request_resolved(db: Session, request_id: int, message: str = "Request has been successfully resolved."):
    """
    Emits REQUEST_RESOLVED WS event to senior, caretaker, assigned volunteer, and family.
    """
    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        return

    senior = db.query(Senior).filter(Senior.id == req.senior_id).first()
    target_user_ids = set()

    if senior:
        target_user_ids.add(senior.user_id)

    # Caretaker
    assoc = db.query(CaretakerSenior).filter(CaretakerSenior.senior_id == req.senior_id, CaretakerSenior.is_primary == True).first()
    if assoc:
        c = db.query(Caretaker).filter(Caretaker.id == assoc.caretaker_id).first()
        if c:
            target_user_ids.add(c.user_id)

    # Assigned volunteers
    assignments = db.query(Assignment).filter(Assignment.request_id == req.id).all()
    for a in assignments:
        if a.responder_type == ResponderType.VOLUNTEER.value:
            vol = db.query(Volunteer).filter(Volunteer.id == a.responder_id).first()
            if vol:
                target_user_ids.add(vol.user_id)

    # Family members
    family_members = db.query(Family).filter(Family.senior_id == req.senior_id).all()
    for f in family_members:
        target_user_ids.add(f.user_id)

    data = {
        "request_id": req.id,
        "senior_id": req.senior_id,
        "status": RequestStatus.RESOLVED.value,
        "message": message
    }

    for user_id in target_user_ids:
        create_notification(
            db=db,
            user_id=user_id,
            notification_type="REQUEST_RESOLVED",
            title="Request Resolved",
            message=message,
            request_id=req.id,
            extra_data=data
        )
