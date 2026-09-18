from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Family, Senior, User, MedicalRecord
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/family", tags=["Family"])

@router.get("/{id}/senior")
def get_family_senior_details(id: int, db: Session = Depends(get_db)):
    family = db.query(Family).filter(Family.id == id).first()
    if not family:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Family record {id} not found."))

    senior = db.query(Senior).filter(Senior.id == family.senior_id).first()
    if not senior:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Associated senior profile not found."))

    user = db.query(User).filter(User.id == senior.user_id).first()
    return success_response(
        data={
            "senior_id": senior.id,
            "name": user.name if user else "Senior",
            "age": senior.age,
            "gender": senior.gender,
            "preferred_language": senior.preferred_language,
            "address": senior.address,
            "latitude": senior.latitude if family.can_view_location else None,
            "longitude": senior.longitude if family.can_view_location else None,
            "relationship": family.relationship,
            "can_receive_emergency_alerts": family.can_receive_emergency_alerts
        },
        message="Senior details retrieved for family member"
    )

@router.get("/{id}/health-summary")
def get_family_senior_health(id: int, db: Session = Depends(get_db)):
    family = db.query(Family).filter(Family.id == id).first()
    if not family:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Family record {id} not found."))

    if not family.can_view_health:
        raise HTTPException(status_code=403, detail=error_response("FORBIDDEN", "Family member is not authorized to view health records."))

    record = db.query(MedicalRecord).filter(MedicalRecord.senior_id == family.senior_id).first()
    return success_response(
        data={
            "senior_id": family.senior_id,
            "conditions": record.conditions if record else "None reported",
            "allergies": record.allergies if record else "None",
            "blood_group": record.blood_group if record else "Unknown",
            "important_notes": record.important_notes if record else "No special medical records."
        },
        message="Senior health summary retrieved for family"
    )
