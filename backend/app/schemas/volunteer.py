from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserRead

class VolunteerRegister(BaseModel):
    user_id: int
    latitude: float
    longitude: float
    max_distance_km: float = 5.0
    skills: List[str] = ["First Aid"]
    first_aid_trained: bool = True

class VolunteerRead(BaseModel):
    id: int
    user_id: int
    latitude: float
    longitude: float
    availability_status: bool
    max_distance_km: float
    skills: List[str] = []
    first_aid_trained: bool
    current_active_requests: int
    user: Optional[UserRead] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AvailabilityUpdate(BaseModel):
    availability_status: bool

class VolunteerFrontendContract(BaseModel):
    id: int
    name: str
    distance_km: float
    eta_minutes: int
    available: bool
    skills: List[str]
