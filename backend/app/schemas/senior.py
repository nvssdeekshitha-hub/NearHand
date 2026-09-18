from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserRead

class MedicalRecordRead(BaseModel):
    id: int
    senior_id: int
    conditions: Optional[str] = None
    allergies: Optional[str] = None
    blood_group: Optional[str] = None
    important_notes: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SeniorRead(BaseModel):
    id: int
    user_id: int
    age: Optional[int] = None
    gender: Optional[str] = None
    preferred_language: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    home_latitude: Optional[float] = None
    home_longitude: Optional[float] = None
    location_deviation_threshold_km: float = 1.0
    emergency_contact: Optional[str] = None
    user: Optional[UserRead] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
