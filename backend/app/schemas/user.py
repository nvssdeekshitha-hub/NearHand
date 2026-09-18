from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    is_active: bool = True

class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
