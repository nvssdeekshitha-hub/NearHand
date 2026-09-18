from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class MedicationCreate(BaseModel):
    senior_id: int
    medicine_name: str
    dosage: str
    schedule: str

class MedicationRead(BaseModel):
    id: int
    senior_id: int
    medicine_name: str
    dosage: str
    schedule: str
    taken_today: bool
    last_taken_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
