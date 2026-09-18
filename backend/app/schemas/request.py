from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict

class RequestCreate(BaseModel):
    senior_id: Optional[int] = None  # If not provided, derived from logged-in senior
    message: str
    input_type: Optional[str] = "TEXT"
    language: Optional[str] = None

class AssignmentRead(BaseModel):
    id: int
    request_id: int
    responder_type: str
    responder_id: int
    assignment_status: str
    assigned_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    distance_km: Optional[float] = None
    eta_minutes: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class RequestRead(BaseModel):
    id: int
    senior_id: int
    message: str
    input_type: str
    language: str
    request_type: str
    urgency: str
    risk_score: int
    emergency: bool
    mobility_issue: bool
    medical_attention_possible: bool
    required_support: List[str] = []
    companionship: bool
    status: str
    target_response_minutes: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    assignments: List[AssignmentRead] = []

    model_config = ConfigDict(from_attributes=True)

class RequestAcceptReject(BaseModel):
    reason: Optional[str] = None
