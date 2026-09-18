from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class LocationUpdate(BaseModel):
    senior_id: Optional[int] = None
    latitude: float
    longitude: float
    expected_trip: bool = False

class LocationCheck(BaseModel):
    senior_id: int
    current_latitude: float
    current_longitude: float
    expected_trip: bool = False

class LocationEventRead(BaseModel):
    id: int
    senior_id: int
    latitude: float
    longitude: float
    timestamp: datetime
    is_deviation: bool
    expected_trip: bool

    model_config = ConfigDict(from_attributes=True)
