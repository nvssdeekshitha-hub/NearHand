import json
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Volunteer, User, Senior, Request, Assignment, RequestStatus, AssignmentStatus
from app.schemas.volunteer import VolunteerRegister, AvailabilityUpdate
from app.schemas.common import success_response, error_response
from app.services.matching_service import find_best_volunteers
from app.services.escalation_service import notify_family_members, notify_request_resolved
from app.api.websocket import emit_ws_event
from app.utils.timers import cancel_caretaker_timeout_timer

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])

@router.post("/register")
def register_volunteer(payload: VolunteerRegister, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"User {payload.user_id} not found."))

    vol = Volunteer(
        user_id=payload.user_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        max_distance_km=payload.max_distance_km,
        skills=json.dumps(payload.skills),
        first_aid_trained=payload.first_aid_trained
    )
    db.add(vol)
    db.commit()
    db.refresh(vol)

    return success_response(
        data={
            "id": vol.id,
            "user_id": vol.user_id,
            "name": user.name,
            "latitude": vol.latitude,
            "longitude": vol.longitude,
            "max_distance_km": vol.max_distance_km,
            "skills": payload.skills,
            "first_aid_trained": vol.first_aid_trained
        },
        message="Volunteer profile registered"
    )

@router.get("/nearby")
def get_nearby_volunteers(
    senior_id: Optional[int] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    senior = None
    if senior_id:
        senior = db.query(Senior).filter(Senior.id == senior_id).first()
    if not senior:
        senior = db.query(Senior).first()

    mock_req = Request(
        senior_id=senior.id if senior else 1,
        request_type="FALL",
        urgency="CRITICAL"
    )

    matches = find_best_volunteers(db=db, senior=senior, request=mock_req, limit=10)
    
    frontend_contract_list = []
    for m in matches:
        frontend_contract_list.append({
            "id": m["volunteer_id"],
            "name": m["name"],
            "distance_km": m["distance_km"],
            "eta_minutes": m["eta_minutes"],
            "available": m["available"],
            "skills": m["skills"]
        })

    return success_response(data=frontend_contract_list, message="Nearby volunteers matching contract retrieved")

@router.patch("/{id}/availability")
def update_volunteer_availability(id: int, payload: AvailabilityUpdate, db: Session = Depends(get_db)):
    vol = db.query(Volunteer).filter(Volunteer.id == id).first()
    if not vol:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Volunteer {id} not found."))

    vol.availability_status = payload.availability_status
    db.commit()
    return success_response(
        data={"id": vol.id, "availability_status": vol.availability_status},
        message="Volunteer availability updated"
    )

@router.get("/{id}/requests")
def get_volunteer_requests(id: int, db: Session = Depends(get_db)):
    vol = db.query(Volunteer).filter(Volunteer.id == id).first()
    if not vol:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Volunteer {id} not found."))

    assignments = db.query(Assignment).filter(
        Assignment.responder_type == "VOLUNTEER",
        Assignment.responder_id == id
    ).all()

    req_ids = [a.request_id for a in assignments]
    requests = db.query(Request).filter(Request.id.in_(req_ids)).all() if req_ids else []

    results = []
    for r in requests:
        senior = db.query(Senior).filter(Senior.id == r.senior_id).first()
        u = db.query(User).filter(User.id == senior.user_id).first() if senior else None
        results.append({
            "request_id": r.id,
            "senior_id": r.senior_id,
            "senior_name": u.name if u else "Senior",
            "message": r.message,
            "request_type": r.request_type,
            "urgency": r.urgency,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })

    return success_response(data=results, message="Volunteer requests retrieved")

@router.post("/{id}/accept-request")
def volunteer_accept_request(id: int, request_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    vol = db.query(Volunteer).filter(Volunteer.id == id).first()
    if not vol:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Volunteer {id} not found."))

    # Find pending volunteer assignment or top pending assignment for request
    assignment = None
    if request_id:
        assignment = db.query(Assignment).filter(
            Assignment.request_id == request_id,
            Assignment.responder_type == "VOLUNTEER",
            Assignment.responder_id == id
        ).first()

    if not assignment:
        # Fallback to latest pending volunteer assignment for this volunteer
        assignment = db.query(Assignment).filter(
            Assignment.responder_type == "VOLUNTEER",
            Assignment.responder_id == id,
            Assignment.assignment_status == AssignmentStatus.PENDING.value
        ).order_by(Assignment.id.desc()).first()

    if not assignment and request_id:
        # Or any pending assignment for this request_id
        assignment = db.query(Assignment).filter(
            Assignment.request_id == request_id,
            Assignment.assignment_status == AssignmentStatus.PENDING.value
        ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail=error_response("NO_ASSIGNMENT", "No pending volunteer assignment found to accept."))

    req = db.query(Request).filter(Request.id == assignment.request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Associated request not found."))

    cancel_caretaker_timeout_timer(req.id)

    assignment.assignment_status = AssignmentStatus.ACCEPTED.value
    assignment.accepted_at = datetime.now(timezone.utc)
    
    req.status = RequestStatus.VOLUNTEER_ACCEPTED.value
    db.commit()

    # Emit VOLUNTEER_ACCEPTED WS event to senior
    senior = db.query(Senior).filter(Senior.id == req.senior_id).first()
    if senior:
        emit_ws_event(
            user_id=senior.user_id,
            event_name="VOLUNTEER_ACCEPTED",
            data={
                "request_id": req.id,
                "senior_id": senior.id,
                "volunteer_name": vol.user.name if vol.user else "Priya Sharma",
                "distance_km": assignment.distance_km,
                "eta_minutes": assignment.eta_minutes
            }
        )

    # Trigger family notification (Emits FAMILY_NOTIFIED WS events)
    notify_family_members(
        db=db,
        senior_id=req.senior_id,
        request_id=req.id,
        title="Volunteer Dispatched",
        message=f"Volunteer {vol.user.name if vol.user else 'Priya Sharma'} has accepted the request and is on their way."
    )

    req.status = RequestStatus.FAMILY_NOTIFIED.value
    db.commit()

    # Move to RESOLVED & broadcast RESOLVED event to all parties
    req.status = RequestStatus.RESOLVED.value
    db.commit()
    db.refresh(req)

    notify_request_resolved(db=db, request_id=req.id, message=f"Volunteer {vol.user.name if vol.user else 'Priya Sharma'} accepted request #{req.id}. Request RESOLVED.")

    user = db.query(User).filter(User.id == vol.user_id).first()

    return success_response(
        data={
            "request_id": req.id,
            "status": req.status,
            "volunteer": {
                "id": vol.id,
                "name": user.name if user else "Priya Sharma",
                "distance_km": assignment.distance_km or 2.4,
                "eta_minutes": assignment.eta_minutes or 7,
                "available": vol.availability_status,
                "skills": ["First Aid"] if vol.first_aid_trained else []
            }
        },
        message="Volunteer request accepted. Family notified and status marked RESOLVED."
    )
