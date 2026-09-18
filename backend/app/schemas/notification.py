from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class NotificationRead(BaseModel):
    id: int
    user_id: int
    request_id: Optional[int] = None
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
