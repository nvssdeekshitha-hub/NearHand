from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models import (
    UserRole,
    AvailabilityStatus,
    InputType,
    RequestType,
    UrgencyLevel,
    RequestStatus,
    ResponderType,
    AssignmentStatus,
    NotificationType,
    CompanionshipStatus
)


# Base Pydantic Model Config
class OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# USER SCHEMAS
# ==========================================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserOut(UserBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# SENIOR SCHEMAS
# ==========================================

class SeniorBase(BaseModel):
    user_id: int
    age: int = Field(..., gt=0, lt=120)
    gender: Optional[str] = None
    preferred_language: str = "English"
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    home_latitude: Optional[float] = Field(None, ge=-90, le=90)
    home_longitude: Optional[float] = Field(None, ge=-180, le=180)
    location_deviation_threshold_km: float = 0.5
    emergency_contact: Optional[str] = None


class SeniorCreate(SeniorBase):
    pass


class SeniorOut(SeniorBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# CARETAKER SCHEMAS
# ==========================================

class CaretakerBase(BaseModel):
    user_id: int
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_seniors: int = 5
    current_load: int = 0


class CaretakerCreate(CaretakerBase):
    pass


class CaretakerOut(CaretakerBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# VOLUNTEER SCHEMAS
# ==========================================

class VolunteerBase(BaseModel):
    user_id: int
    availability_status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_distance_km: float = 10.0
    skills: Optional[str] = None
    first_aid_trained: bool = False
    current_active_requests: int = 0


class VolunteerCreate(VolunteerBase):
    pass


class VolunteerOut(VolunteerBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# FAMILY MEMBER SCHEMAS
# ==========================================

class FamilyMemberBase(BaseModel):
    user_id: int
    senior_id: int
    relationship: str
    can_receive_emergency_alerts: bool = True
    can_view_health: bool = True
    can_view_location: bool = True


class FamilyMemberCreate(FamilyMemberBase):
    pass


class FamilyMemberOut(FamilyMemberBase, OrmBase):
    id: int
    created_at: datetime


# ==========================================
# MEDICAL RECORD SCHEMAS
# ==========================================

class MedicalRecordBase(BaseModel):
    senior_id: int
    conditions: Optional[str] = None
    allergies: Optional[str] = None
    blood_group: Optional[str] = None
    important_notes: Optional[str] = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordOut(MedicalRecordBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# MEDICATION SCHEMAS
# ==========================================

class MedicationBase(BaseModel):
    senior_id: int
    medicine_name: str
    dosage: str
    schedule: str
    taken_today: bool = False
    last_taken_at: Optional[datetime] = None
    active: bool = True


class MedicationCreate(MedicationBase):
    pass


class MedicationOut(MedicationBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime


# ==========================================
# REQUEST SCHEMAS
# ==========================================

class RequestBase(BaseModel):
    senior_id: int
    message: str
    input_type: InputType = InputType.TEXT
    language: Optional[str] = "English"
    request_type: RequestType = RequestType.GENERAL_HELP
    urgency: UrgencyLevel = UrgencyLevel.LOW
    risk_score: int = Field(0, ge=0, le=100)
    emergency: bool = False
    potential_emergency: bool = False
    fall_detected: bool = False
    mobility_issue: bool = False
    medical_attention_possible: bool = False
    required_support: Optional[str] = None
    location_relevant: bool = False
    location_context: Optional[str] = None
    companionship: bool = False
    status: RequestStatus = RequestStatus.CREATED
    target_response_minutes: int = 10
    ai_analysis_json: Optional[str] = None


class RequestCreate(RequestBase):
    pass


class RequestUpdateStatus(BaseModel):
    status: RequestStatus
    resolved_at: Optional[datetime] = None


class RequestOut(RequestBase, OrmBase):
    id: int
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None


# ==========================================
# ASSIGNMENT SCHEMAS
# ==========================================

class AssignmentBase(BaseModel):
    request_id: int
    responder_type: ResponderType
    responder_id: int
    assignment_status: AssignmentStatus = AssignmentStatus.PENDING
    assigned_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    response_deadline: Optional[datetime] = None
    distance_km: Optional[float] = None
    eta_minutes: Optional[int] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentOut(AssignmentBase, OrmBase):
    id: int
    created_at: datetime


# ==========================================
# NOTIFICATION SCHEMAS
# ==========================================

class NotificationBase(BaseModel):
    user_id: int
    request_id: Optional[int] = None
    type: NotificationType = NotificationType.SYSTEM
    title: str
    message: str
    is_read: bool = False


class NotificationCreate(NotificationBase):
    pass


class NotificationOut(NotificationBase, OrmBase):
    id: int
    created_at: datetime
    read_at: Optional[datetime] = None


# ==========================================
# LOCATION EVENT SCHEMAS
# ==========================================

class LocationEventBase(BaseModel):
    senior_id: int
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    distance_from_home_km: float = 0.0
    deviation_detected: bool = False
    expected_trip: bool = False


class LocationEventCreate(LocationEventBase):
    pass


class LocationEventOut(LocationEventBase, OrmBase):
    id: int
    created_at: datetime


# ==========================================
# AUDIT LOG SCHEMAS
# ==========================================

class AuditLogCreate(BaseModel):
    user_id: Optional[int] = None
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    details: Optional[str] = None


class AuditLogOut(AuditLogCreate, OrmBase):
    id: int
    created_at: datetime
