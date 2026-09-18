from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Senior, MedicalRecord, CaretakerSenior, Caretaker, Family, User
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/seniors", tags=["Seniors"])

@router.get("/{id}")
def get_senior_profile(id: int, db: Session = Depends(get_db)):
    senior = db.query(Senior).filter(Senior.id == id).first()
    if not senior:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Senior with id {id} not found."))
    
    user = db.query(User).filter(User.id == senior.user_id).first()
    return success_response(
        data={
            "id": senior.id,
            "user_id": senior.user_id,
            "name": user.name if user else "Senior",
            "email": user.email if user else "",
            "phone": user.phone if user else "",
            "age": senior.age,
            "gender": senior.gender,
            "preferred_language": senior.preferred_language,
            "address": senior.address,
            "latitude": senior.latitude,
            "longitude": senior.longitude,
            "home_latitude": senior.home_latitude,
            "home_longitude": senior.home_longitude,
            "location_deviation_threshold_km": senior.location_deviation_threshold_km,
            "emergency_contact": senior.emergency_contact
        },
        message="Senior profile retrieved successfully"
    )

@router.get("/{id}/health")
def get_senior_health(id: int, db: Session = Depends(get_db)):
    senior = db.query(Senior).filter(Senior.id == id).first()
    if not senior:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Senior with id {id} not found."))

    record = db.query(MedicalRecord).filter(MedicalRecord.senior_id == id).first()
    if not record:
        return success_response(
            data={
                "senior_id": id,
                "conditions": "None reported",
                "allergies": "None",
                "blood_group": "Unknown",
                "important_notes": "No special medical records on file."
            },
            message="Health summary retrieved"
        )
    return success_response(
        data={
            "id": record.id,
            "senior_id": record.senior_id,
            "conditions": record.conditions,
            "allergies": record.allergies,
            "blood_group": record.blood_group,
            "important_notes": record.important_notes,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        },
        message="Health records retrieved successfully"
    )

@router.get("/{id}/caretaker")
def get_senior_caretaker(id: int, db: Session = Depends(get_db)):
    assoc = db.query(CaretakerSenior).filter(
        CaretakerSenior.senior_id == id,
        CaretakerSenior.is_primary == True
    ).first()
    
    if not assoc:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "No primary caretaker assigned."))

    caretaker = db.query(Caretaker).filter(Caretaker.id == assoc.caretaker_id).first()
    if not caretaker:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", "Caretaker details not found."))

    user = db.query(User).filter(User.id == caretaker.user_id).first()
    return success_response(
        data={
            "caretaker_id": caretaker.id,
            "user_id": user.id if user else None,
            "name": user.name if user else "Primary Caretaker",
            "phone": user.phone if user else "",
            "availability_status": caretaker.availability_status,
            "assigned_at": assoc.assigned_at.isoformat() if assoc.assigned_at else None
        },
        message="Caretaker details retrieved"
    )

@router.get("/{id}/family")
def get_senior_family(id: int, db: Session = Depends(get_db)):
    family_members = db.query(Family).filter(Family.senior_id == id).all()
    results = []
    for fam in family_members:
        user = db.query(User).filter(User.id == fam.user_id).first()
        results.append({
            "family_id": fam.id,
            "user_id": fam.user_id,
            "name": user.name if user else "Family Member",
            "phone": user.phone if user else "",
            "relationship": fam.relationship,
            "can_receive_emergency_alerts": fam.can_receive_emergency_alerts,
            "can_view_health": fam.can_view_health,
            "can_view_location": fam.can_view_location
        })
    return success_response(data=results, message="Family members retrieved successfully")
