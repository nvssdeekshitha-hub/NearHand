from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Senior, Request
from app.schemas.common import success_response, error_response
from app.schemas.request import RequestCreate
from app.services.request_service import create_and_process_request

router = APIRouter(prefix="/companionship", tags=["Companionship"])

@router.post("/request")
def request_companionship(senior_id: int = 1, message: str = "Feeling lonely today and would love to talk to someone.", db: Session = Depends(get_db)):
    senior = db.query(Senior).filter(Senior.id == senior_id).first()
    if not senior:
        senior = db.query(Senior).first()

    req_in = RequestCreate(
        senior_id=senior.id if senior else 1,
        message=message,
        input_type="TEXT"
    )
    req = create_and_process_request(db=db, request_in=req_in, senior=senior)

    return success_response(
        data={
            "request_id": req.id,
            "status": req.status,
            "urgency": req.urgency,
            "request_type": req.request_type
        },
        message="Companionship request submitted (Low urgency, no escalation priority)"
    )

@router.get("/{senior_id}")
def get_companionship_requests(senior_id: int, db: Session = Depends(get_db)):
    requests = db.query(Request).filter(
        Request.senior_id == senior_id,
        Request.request_type == "COMPANIONSHIP"
    ).order_by(Request.id.desc()).all()

    results = []
    for r in requests:
        results.append({
            "id": r.id,
            "message": r.message,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })

    return success_response(data=results, message="Companionship requests retrieved")
