from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserRead

class FamilyRead(BaseModel):
    id: int
    user_id: int
    senior_id: int
    relationship: str
    can_receive_emergency_alerts: bool
    can_view_health: bool
    can_view_location: bool
    user: Optional[UserRead] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
