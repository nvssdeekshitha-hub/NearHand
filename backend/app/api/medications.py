from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Medication, Senior
from app.schemas.medication import MedicationCreate
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/medications", tags=["Medications"])

@router.post("")
def add_medication(payload: MedicationCreate, db: Session = Depends(get_db)):
    senior = db.query(Senior).filter(Senior.id == payload.senior_id).first()
    if not senior:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Senior {payload.senior_id} not found."))

    med = Medication(
        senior_id=payload.senior_id,
        medicine_name=payload.medicine_name,
        dosage=payload.dosage,
        schedule=payload.schedule
    )
    db.add(med)
    db.commit()
    db.refresh(med)

    return success_response(
        data={
            "id": med.id,
            "senior_id": med.senior_id,
            "medicine_name": med.medicine_name,
            "dosage": med.dosage,
            "schedule": med.schedule,
            "taken_today": med.taken_today
        },
        message="Medication added"
    )

@router.get("/{senior_id}")
def get_senior_medications(senior_id: int, db: Session = Depends(get_db)):
    meds = db.query(Medication).filter(Medication.senior_id == senior_id).all()
    results = []
    for m in meds:
        results.append({
            "id": m.id,
            "senior_id": m.senior_id,
            "medicine_name": m.medicine_name,
            "dosage": m.dosage,
            "schedule": m.schedule,
            "taken_today": m.taken_today,
            "last_taken_at": m.last_taken_at.isoformat() if m.last_taken_at else None
        })

    return success_response(data=results, message="Medications retrieved")

@router.patch("/{id}/mark-taken")
def mark_medication_taken(id: int, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == id).first()
    if not med:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Medication {id} not found."))

    med.taken_today = True
    med.last_taken_at = datetime.now(timezone.utc)
    db.commit()

    return success_response(
        data={
            "id": med.id,
            "medicine_name": med.medicine_name,
            "taken_today": True,
            "last_taken_at": med.last_taken_at.isoformat()
        },
        message="Medication marked as taken"
    )
