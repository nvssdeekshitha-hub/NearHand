from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Senior, Request, Caretaker, Volunteer, Assignment, RequestStatus, AssignmentStatus
from app.schemas.common import success_response, error_response
from app.schemas.request import RequestCreate
from app.services.request_service import create_and_process_request
from app.services.escalation_service import handle_caretaker_timeout
from app.services.escalation_service import notify_family_members
from app.utils.timers import cancel_caretaker_timeout_timer

router = APIRouter(prefix="/demo", tags=["Demo Simulation"])

@router.post("/simulate-critical-request")
def simulate_critical_request(db: Session = Depends(get_db)):
    """
    Creates Lakshmi's critical Telugu fall request for live hackathon demonstration.
    """
    # Find Lakshmi
    senior = db.query(Senior).first()
    if not senior:
        raise HTTPException(status_code=400, detail=error_response("SEED_REQUIRED", "Please run seed script first."))

    message_text = "నాకు బాత్రూమ్‌లో కాలు జారి పడిపోయాను, లేవలేకపోతున్నాను"
    req_in = RequestCreate(
        senior_id=senior.id,
        message=message_text,
        input_type="TEXT"
    )

    req = create_and_process_request(db=db, request_in=req_in, senior=senior)
    return success_response(
        data={
            "id": req.id,
            "senior_id": req.senior_id,
            "request_type": req.request_type,
            "message": req.message,
            "language": req.language,
            "urgency": req.urgency,
            "risk_score": req.risk_score,
            "emergency": req.emergency,
            "status": req.status,
            "target_response_minutes": req.target_response_minutes
        },
        message="Demo critical fall request simulated successfully"
    )

@router.post("/simulate-caretaker-timeout")
def simulate_caretaker_timeout(request_id: int = None, db: Session = Depends(get_db)):
    """
    Bypasses background timers to immediately force Caretaker Timeout and trigger Volunteer Matching.
    """
    req = None
    if request_id:
        req = db.query(Request).filter(Request.id == request_id).first()
    else:
        req = db.query(Request).order_by(Request.id.desc()).first()

    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "No request found to simulate timeout for."))

    cancel_caretaker_timeout_timer(req.id)
    updated_req = handle_caretaker_timeout(db=db, request_id=req.id)
    
    volunteer_assignment = db.query(Assignment).filter(
        Assignment.request_id == req.id,
        Assignment.responder_type == "VOLUNTEER"
    ).first()

    volunteer_data = None
    if volunteer_assignment:
        vol = db.query(Volunteer).filter(Volunteer.id == volunteer_assignment.responder_id).first()
        if vol:
            volunteer_data = {
                "id": vol.id,
                "name": vol.user.name if vol.user else "Priya Sharma",
                "distance_km": volunteer_assignment.distance_km,
                "eta_minutes": volunteer_assignment.eta_minutes,
                "available": vol.availability_status,
                "skills": ["First Aid"] if vol.first_aid_trained else []
            }

    return success_response(
        data={
            "request_id": req.id,
            "status": updated_req.status if updated_req else req.status,
            "matched_volunteer": volunteer_data
        },
        message="Caretaker timeout simulated. Volunteer notified."
    )

@router.post("/simulate-volunteer-acceptance")
def simulate_volunteer_acceptance(request_id: int = None, db: Session = Depends(get_db)):
    """
    Simulates Priya Sharma accepting the escalated volunteer request.
    """
    req = None
    if request_id:
        req = db.query(Request).filter(Request.id == request_id).first()
    else:
        req = db.query(Request).order_by(Request.id.desc()).first()

    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "No request found to accept."))

    cancel_caretaker_timeout_timer(req.id)

    # Find pending volunteer assignment
    assignment = db.query(Assignment).filter(
        Assignment.request_id == req.id,
        Assignment.responder_type == "VOLUNTEER"
    ).first()

    if assignment:
        assignment.assignment_status = AssignmentStatus.ACCEPTED.value

    req.status = RequestStatus.VOLUNTEER_ACCEPTED.value
    db.commit()

    from app.api.websocket import emit_ws_event
    senior = db.query(Senior).filter(Senior.id == req.senior_id).first()
    if senior:
        emit_ws_event(
            user_id=senior.user_id,
            event_name="VOLUNTEER_ACCEPTED",
            data={"request_id": req.id, "senior_id": senior.id, "volunteer_name": "Priya Sharma"}
        )

    notify_family_members(
        db=db,
        senior_id=req.senior_id,
        request_id=req.id,
        title="Volunteer Dispatched (Demo)",
        message="Volunteer Priya Sharma has accepted the request and is en route."
    )

    req.status = RequestStatus.FAMILY_NOTIFIED.value
    db.commit()

    req.status = RequestStatus.RESOLVED.value
    db.commit()

    from app.services.escalation_service import notify_request_resolved
    notify_request_resolved(db=db, request_id=req.id, message="Priya Sharma accepted request. Request RESOLVED.")

    return success_response(
        data={
            "request_id": req.id,
            "status": req.status,
            "resolution_summary": "Priya Sharma accepted request -> Family Notified -> Request RESOLVED."
        },
        message="Volunteer acceptance simulated successfully"
    )

@router.post("/reset-db")
def reset_database_seed(db: Session = Depends(get_db)):
    """
    Resets and re-seeds database during live demo presentation.
    """
    from app.db.seed import seed_data
    seed_data(db)
    return success_response(message="Database re-seeded successfully!")
