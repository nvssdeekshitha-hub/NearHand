from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Senior, Request, RequestStatus
from app.schemas.common import success_response, error_response
from app.schemas.request import RequestCreate
from app.services.request_service import create_and_process_request

router = APIRouter(tags=["Emergency SOS"])

@router.post("/emergency")
def trigger_global_emergency_sos(senior_id: int = 1, db: Session = Depends(get_db)):
    """
    Big SOS Button trigger endpoint. Bypasses standard delay logic, 
    notifies caretaker + family immediately and logs mock healthcare service dispatch.
    """
    senior = db.query(Senior).filter(Senior.id == senior_id).first()
    if not senior:
        senior = db.query(Senior).first()

    req_in = RequestCreate(
        senior_id=senior.id if senior else 1,
        message="EMERGENCY SOS BUTTON ACTIVATED! Immediate help required!",
        input_type="SOS"
    )
    req = create_and_process_request(db=db, request_in=req_in, senior=senior)

    return success_response(
        data={
            "request_id": req.id,
            "status": req.status,
            "urgency": req.urgency,
            "simulated_healthcare_dispatch": "Dispatch notification sent to local emergency response service (Simulated for Demo)."
        },
        message="Emergency SOS alert triggered immediately!"
    )

@router.post("/requests/{id}/emergency")
def mark_request_as_emergency(id: int, db: Session = Depends(get_db)):
    req = db.query(Request).filter(Request.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Request {id} not found."))

    req.emergency = True
    req.urgency = "CRITICAL"
    req.target_response_minutes = 2
    req.status = RequestStatus.CARETAKER_NOTIFIED.value
    db.commit()

    from app.services.escalation_service import notify_family_members
    notify_family_members(
        db=db,
        senior_id=req.senior_id,
        request_id=req.id,
        title="CRITICAL EMERGENCY CONVERSION",
        message=f"Request #{req.id} was upgraded to Emergency status."
    )

    return success_response(
        data={
            "request_id": req.id,
            "status": req.status,
            "emergency": True,
            "simulated_healthcare_dispatch": "Dispatch notification logged."
        },
        message="Request converted to Emergency SOS"
    )
