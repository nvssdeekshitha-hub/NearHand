from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserRead

class CaretakerRead(BaseModel):
    id: int
    user_id: int
    availability_status: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_seniors: int
    current_load: int
    user: Optional[UserRead] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AvailabilityUpdate(BaseModel):
    availability_status: bool
