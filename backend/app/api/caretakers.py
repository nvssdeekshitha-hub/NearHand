from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Caretaker, CaretakerSenior, Senior, User, Request, Assignment
from app.schemas.caretaker import AvailabilityUpdate
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/caretakers", tags=["Caretakers"])

@router.get("/{id}/seniors")
def get_caretaker_seniors(id: int, db: Session = Depends(get_db)):
    caretaker = db.query(Caretaker).filter(Caretaker.id == id).first()
    if not caretaker:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Caretaker {id} not found."))

    associations = db.query(CaretakerSenior).filter(CaretakerSenior.caretaker_id == id).all()
    results = []
    for assoc in associations:
        senior = db.query(Senior).filter(Senior.id == assoc.senior_id).first()
        if senior:
            u = db.query(User).filter(User.id == senior.user_id).first()
            results.append({
                "senior_id": senior.id,
                "name": u.name if u else "Senior",
                "age": senior.age,
                "gender": senior.gender,
                "preferred_language": senior.preferred_language,
                "address": senior.address,
                "is_primary": assoc.is_primary,
                "assigned_at": assoc.assigned_at.isoformat() if assoc.assigned_at else None
            })
    return success_response(data=results, message=f"Retrieved {len(results)} assigned seniors for caretaker {id}")

@router.get("/{id}/requests")
def get_caretaker_requests(id: int, db: Session = Depends(get_db)):
    caretaker = db.query(Caretaker).filter(Caretaker.id == id).first()
    if not caretaker:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Caretaker {id} not found."))

    # Query assignments for caretaker
    assignments = db.query(Assignment).filter(
        Assignment.responder_type == "CARETAKER",
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
            "risk_score": r.risk_score,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })

    return success_response(data=results, message="Retrieved caretaker requests")

@router.patch("/{id}/availability")
def update_caretaker_availability(id: int, payload: AvailabilityUpdate, db: Session = Depends(get_db)):
    caretaker = db.query(Caretaker).filter(Caretaker.id == id).first()
    if not caretaker:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Caretaker {id} not found."))

    caretaker.availability_status = payload.availability_status
    db.commit()
    return success_response(
        data={"id": caretaker.id, "availability_status": caretaker.availability_status},
        message="Caretaker availability updated"
    )

@router.post("/{id}/request-support")
def request_additional_support(id: int, request_id: int, db: Session = Depends(get_db)):
    """
    Tier 3: Creates an assignment with responder_type=ADDITIONAL_CARETAKER
    without replacing the primary caretaker.
    """
    caretaker = db.query(Caretaker).filter(Caretaker.id == id).first()
    if not caretaker:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Caretaker {id} not found."))

    req = db.query(Request).filter(Request.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Request {request_id} not found."))

    # Find another caretaker
    sec_caretaker = db.query(Caretaker).filter(Caretaker.id != id, Caretaker.availability_status == True).first()
    if not sec_caretaker:
        raise HTTPException(status_code=400, detail=error_response("NO_CARETAKER", "No secondary caretaker available."))

    assignment = Assignment(
        request_id=req.id,
        responder_type="ADDITIONAL_CARETAKER",
        responder_id=sec_caretaker.id,
        assignment_status="PENDING",
        distance_km=2.0,
        eta_minutes=10
    )
    db.add(assignment)
    db.commit()

    return success_response(
        data={
            "request_id": req.id,
            "additional_caretaker_id": sec_caretaker.id,
            "status": "ADDITIONAL_CARETAKER_ASSIGNED"
        },
        message="Additional caretaker support requested"
    )
