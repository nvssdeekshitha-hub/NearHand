import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Request, Senior, Assignment, User, RequestStatus, AssignmentStatus, ResponderType
from app.core.security import get_current_user_optional
from app.schemas.request import RequestCreate, RequestAcceptReject
from app.schemas.common import success_response, error_response
from app.services.request_service import create_and_process_request
from app.services.escalation_service import handle_caretaker_timeout, notify_family_members, notify_request_resolved
from app.services.notification_service import create_notification
from app.api.websocket import emit_ws_event
from app.utils.timers import cancel_caretaker_timeout_timer, schedule_caretaker_timeout_timer

router = APIRouter(prefix="/requests", tags=["Requests"])

def format_request_dto(req: Request, db: Session) -> dict:
    try:
        support_list = json.loads(req.required_support) if req.required_support else []
    except Exception:
        support_list = [req.required_support] if req.required_support else []

    assignments_data = []
    for a in req.assignments:
        assignments_data.append({
            "id": a.id,
            "request_id": a.request_id,
            "responder_type": a.responder_type,
            "responder_id": a.responder_id,
            "assignment_status": a.assignment_status,
            "assigned_at": a.assigned_at.isoformat() if a.assigned_at else None,
            "accepted_at": a.accepted_at.isoformat() if a.accepted_at else None,
            "rejected_at": a.rejected_at.isoformat() if a.rejected_at else None,
            "response_deadline": a.response_deadline.isoformat() if a.response_deadline else None,
            "distance_km": a.distance_km,
            "eta_minutes": a.eta_minutes
        })

    return {
        "id": req.id,
        "senior_id": req.senior_id,
        "request_type": req.request_type,
        "message": req.message,
        "input_type": req.input_type,
        "language": req.language,
        "urgency": req.urgency,
        "risk_score": req.risk_score,
        "emergency": req.emergency,
        "mobility_issue": req.mobility_issue,
        "medical_attention_possible": req.medical_attention_possible,
        "required_support": support_list,
        "companionship": req.companionship,
        "status": req.status,
        "target_response_minutes": req.target_response_minutes,
        "created_at": req.created_at.isoformat() if req.created_at else None,
        "updated_at": req.updated_at.isoformat() if req.updated_at else None,
        "assignments": assignments_data
    }

@router.post("")
async def create_request(
    request_in: RequestCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # Determine target senior
    senior = None
    if request_in.senior_id:
        senior = db.query(Senior).filter(Senior.id == request_in.senior_id).first()
    elif current_user and current_user.senior_profile:
        senior = current_user.senior_profile
    else:
        # Default fallback to first senior (Lakshmi) for demo ease if unauthenticated
        senior = db.query(Senior).first()

    if not senior:
        raise HTTPException(status_code=400, detail=error_response("SENIOR_NOT_FOUND", "No valid senior profile found for request creation."))

    # Sync service: creates request, runs AI analysis, assigns caretaker
    req = create_and_process_request(db=db, request_in=request_in, senior=senior)

    # Schedule caretaker timeout timer HERE — from async context where event loop is running.
    # Only needed for non-emergency requests that are now waiting for caretaker acknowledgement.
    if (
        req.status == RequestStatus.WAITING_FOR_ACKNOWLEDGEMENT.value
        and not req.emergency
    ):
        delay_sec = float(req.target_response_minutes * 60)
        schedule_caretaker_timeout_timer(request_id=req.id, delay_seconds=delay_sec)

    return success_response(
        data=format_request_dto(req, db),
        message="Request submitted and analyzed successfully"
    )

@router.get("/{id}")
def get_request_by_id(id: int, db: Session = Depends(get_db)):
    req = db.query(Request).filter(Request.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Request with id {id} not found."))
    return success_response(data=format_request_dto(req, db), message="Request retrieved")

@router.get("/senior/{senior_id}")
def get_requests_for_senior(senior_id: int, db: Session = Depends(get_db)):
    requests = db.query(Request).filter(Request.senior_id == senior_id).order_by(Request.id.desc()).all()
    dtos = [format_request_dto(r, db) for r in requests]
    return success_response(data=dtos, message=f"Retrieved {len(dtos)} requests for senior {senior_id}")

@router.post("/{id}/accept")
def accept_request(id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user_optional)):
    req = db.query(Request).filter(Request.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Request with id {id} not found."))

    # Cancel background timeout timer
    cancel_caretaker_timeout_timer(req.id)

    # Find pending assignment
    pending_assignment = db.query(Assignment).filter(
        Assignment.request_id == id,
        Assignment.assignment_status == AssignmentStatus.PENDING.value
    ).first()

    if pending_assignment:
        pending_assignment.assignment_status = AssignmentStatus.ACCEPTED.value
        pending_assignment.accepted_at = datetime.now(timezone.utc)
        if pending_assignment.responder_type == ResponderType.CARETAKER.value:
            req.status = RequestStatus.CARETAKER_ACCEPTED.value
        else:
            req.status = RequestStatus.VOLUNTEER_ACCEPTED.value
    else:
        req.status = RequestStatus.CARETAKER_ACCEPTED.value

    db.commit()

    # Emit CARETAKER_ACCEPTED WS event to senior and family
    senior = db.query(Senior).filter(Senior.id == req.senior_id).first()
    if senior:
        emit_ws_event(
            user_id=senior.user_id,
            event_name="CARETAKER_ACCEPTED",
            data={"request_id": req.id, "senior_id": senior.id, "status": req.status}
        )

    # Notify family members (Emits FAMILY_NOTIFIED WS events)
    notify_family_members(
        db=db,
        senior_id=req.senior_id,
        request_id=req.id,
        title="Request Accepted",
        message=f"Caretaker has accepted request #{req.id} for senior."
    )
    req.status = RequestStatus.FAMILY_NOTIFIED.value
    db.commit()

    # Mark RESOLVED and broadcast REQUEST_RESOLVED
    req.status = RequestStatus.RESOLVED.value
    db.commit()

    notify_request_resolved(db=db, request_id=req.id, message=f"Request #{req.id} accepted and resolved.")

    return success_response(data=format_request_dto(req, db), message="Request accepted successfully")

@router.post("/{id}/reject")
def reject_request(id: int, payload: Optional[RequestAcceptReject] = None, db: Session = Depends(get_db)):
    req = db.query(Request).filter(Request.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Request with id {id} not found."))

    # Cancel background timer
    cancel_caretaker_timeout_timer(req.id)

    # Mark current assignment rejected
    pending_assignment = db.query(Assignment).filter(
        Assignment.request_id == id,
        Assignment.assignment_status == AssignmentStatus.PENDING.value
    ).first()

    if pending_assignment:
        pending_assignment.assignment_status = AssignmentStatus.REJECTED.value
        pending_assignment.rejected_at = datetime.now(timezone.utc)
        db.commit()

    req.status = RequestStatus.CARETAKER_REJECTED.value
    db.commit()

    # Immediately escalate to volunteer matching
    updated_req = handle_caretaker_timeout(db=db, request_id=id)
    return success_response(data=format_request_dto(updated_req or req, db), message="Request rejected and escalated to volunteer network")

@router.post("/{id}/escalate")
def escalate_request(id: int, db: Session = Depends(get_db)):
    req = db.query(Request).filter(Request.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Request with id {id} not found."))

    cancel_caretaker_timeout_timer(req.id)
    req.status = RequestStatus.ESCALATED.value
    db.commit()

    notify_family_members(
        db=db,
        senior_id=req.senior_id,
        request_id=req.id,
        title="EMERGENCY ESCALATION",
        message=f"Request #{req.id} was manually escalated to family & emergency contacts."
    )
    return success_response(data=format_request_dto(req, db), message="Request escalated to emergency status")

@router.post("/audio")
async def create_audio_request(
    file: UploadFile = File(...),
    senior_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Tier 3 Audio Endpoint: Transcribes incoming audio file (mock/demo speech-to-text pipeline)
    and passes to request processing pipeline.
    """
    senior = None
    if senior_id:
        senior = db.query(Senior).filter(Senior.id == senior_id).first()
    if not senior:
        senior = db.query(Senior).first()

    # Mock audio transcription for demo mode
    transcribed_text = "నాకు బాత్రూమ్‌లో కాలు జారి పడిపోయాను, లేవలేకపోతున్నాను" # Fall in Telugu demo mock
    
    request_in = RequestCreate(
        senior_id=senior.id,
        message=transcribed_text,
        input_type="AUDIO"
    )
    req = create_and_process_request(db=db, request_in=request_in, senior=senior)
    return success_response(
        data={
            "transcription": transcribed_text,
            "request": format_request_dto(req, db)
        },
        message="Audio request transcribed and processed successfully"
    )
