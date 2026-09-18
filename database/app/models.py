import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text,
    DateTime,
    Enum,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Index,
    func
)
from app.database import Base


# ==========================================
# ENUMS
# ==========================================

class UserRole(str, enum.Enum):
    SENIOR = "SENIOR"
    CARETAKER = "CARETAKER"
    VOLUNTEER = "VOLUNTEER"
    FAMILY = "FAMILY"
    ADMIN = "ADMIN"


class AvailabilityStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


class InputType(str, enum.Enum):
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    SOS = "SOS"


class RequestType(str, enum.Enum):
    FALL = "FALL"
    MEDICAL_HELP = "MEDICAL_HELP"
    MEDICATION = "MEDICATION"
    COMPANIONSHIP = "COMPANIONSHIP"
    LOCATION_DEVIATION = "LOCATION_DEVIATION"
    GENERAL_HELP = "GENERAL_HELP"
    EMERGENCY = "EMERGENCY"
    OTHER = "OTHER"


class UrgencyLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RequestStatus(str, enum.Enum):
    CREATED = "CREATED"
    ANALYZING = "ANALYZING"
    PRIORITIZED = "PRIORITIZED"
    CARETAKER_NOTIFIED = "CARETAKER_NOTIFIED"
    WAITING_FOR_ACKNOWLEDGEMENT = "WAITING_FOR_ACKNOWLEDGEMENT"
    CARETAKER_ACCEPTED = "CARETAKER_ACCEPTED"
    CARETAKER_REJECTED = "CARETAKER_REJECTED"
    CARETAKER_TIMEOUT = "CARETAKER_TIMEOUT"
    VOLUNTEER_NOTIFIED = "VOLUNTEER_NOTIFIED"
    VOLUNTEER_ACCEPTED = "VOLUNTEER_ACCEPTED"
    FAMILY_NOTIFIED = "FAMILY_NOTIFIED"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"


class ResponderType(str, enum.Enum):
    CARETAKER = "CARETAKER"
    VOLUNTEER = "VOLUNTEER"
    ADDITIONAL_CARETAKER = "ADDITIONAL_CARETAKER"


class AssignmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    TIMEOUT = "TIMEOUT"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class NotificationType(str, enum.Enum):
    EMERGENCY = "EMERGENCY"
    REQUEST = "REQUEST"
    ESCALATION = "ESCALATION"
    LOCATION = "LOCATION"
    MEDICATION = "MEDICATION"
    FAMILY = "FAMILY"
    SYSTEM = "SYSTEM"


class CompanionshipStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    NOTIFIED = "NOTIFIED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# ==========================================
# SQLALCHEMY ORM MODELS
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(30), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Senior(Base):
    __tablename__ = "seniors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=True)
    preferred_language = Column(String(50), default="English", nullable=False)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    home_latitude = Column(Float, nullable=True)
    home_longitude = Column(Float, nullable=True)
    location_deviation_threshold_km = Column(Float, default=0.5, nullable=False)
    emergency_contact = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("age > 0 AND age < 120", name="chk_senior_age"),
        CheckConstraint("latitude IS NULL OR (latitude BETWEEN -90 AND 90)", name="chk_senior_lat"),
        CheckConstraint("longitude IS NULL OR (longitude BETWEEN -180 AND 180)", name="chk_senior_lng"),
        CheckConstraint("home_latitude IS NULL OR (home_latitude BETWEEN -90 AND 90)", name="chk_senior_home_lat"),
        CheckConstraint("home_longitude IS NULL OR (home_longitude BETWEEN -180 AND 180)", name="chk_senior_home_lng"),
    )


class Caretaker(Base):
    __tablename__ = "caretakers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    availability_status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    max_seniors = Column(Integer, default=5, nullable=False)
    current_load = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class CaretakerSenior(Base):
    __tablename__ = "caretaker_seniors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    caretaker_id = Column(Integer, ForeignKey("caretakers.id", ondelete="CASCADE"), nullable=False, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False, index=True)
    is_primary = Column(Boolean, default=True, nullable=False)
    assigned_at = Column(DateTime, default=func.now(), nullable=False)
    ended_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_caretaker_senior_ids", "caretaker_id", "senior_id"),
    )


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    availability_status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE, nullable=False)
    max_distance_km = Column(Float, default=10.0, nullable=False)
    skills = Column(Text, nullable=True)
    first_aid_trained = Column(Boolean, default=False, nullable=False)
    current_active_requests = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False)
    relationship = Column(String(50), nullable=False)
    can_receive_emergency_alerts = Column(Boolean, default=True, nullable=False)
    can_view_health = Column(Boolean, default=True, nullable=False)
    can_view_location = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False)
    conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    blood_group = Column(String(10), nullable=True)
    important_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False)
    medicine_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    schedule = Column(String(100), nullable=False)
    taken_today = Column(Boolean, default=False, nullable=False)
    last_taken_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    input_type = Column(Enum(InputType), default=InputType.TEXT, nullable=False)
    language = Column(String(50), nullable=True)
    request_type = Column(Enum(RequestType), default=RequestType.GENERAL_HELP, nullable=False)
    urgency = Column(Enum(UrgencyLevel), default=UrgencyLevel.LOW, nullable=False, index=True)
    risk_score = Column(Integer, default=0, nullable=False)
    emergency = Column(Boolean, default=False, nullable=False)
    potential_emergency = Column(Boolean, default=False, nullable=False)
    fall_detected = Column(Boolean, default=False, nullable=False)
    mobility_issue = Column(Boolean, default=False, nullable=False)
    medical_attention_possible = Column(Boolean, default=False, nullable=False)
    required_support = Column(Text, nullable=True)
    location_relevant = Column(Boolean, default=False, nullable=False)
    location_context = Column(Text, nullable=True)
    companionship = Column(Boolean, default=False, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.CREATED, nullable=False, index=True)
    target_response_minutes = Column(Integer, default=10, nullable=False)
    ai_analysis_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("risk_score BETWEEN 0 AND 100", name="chk_request_risk_score"),
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False, index=True)
    responder_type = Column(Enum(ResponderType), nullable=False)
    responder_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assignment_status = Column(Enum(AssignmentStatus), default=AssignmentStatus.PENDING, nullable=False)
    assigned_at = Column(DateTime, default=func.now(), nullable=False)
    accepted_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    response_deadline = Column(DateTime, nullable=True)
    distance_km = Column(Float, nullable=True)
    eta_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="SET NULL"), nullable=True)
    type = Column(Enum(NotificationType), default=NotificationType.SYSTEM, nullable=False)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    read_at = Column(DateTime, nullable=True)


class LocationEvent(Base):
    __tablename__ = "location_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    distance_from_home_km = Column(Float, default=0.0, nullable=False)
    deviation_detected = Column(Boolean, default=False, nullable=False)
    expected_trip = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("latitude BETWEEN -90 AND 90", name="chk_loc_lat"),
        CheckConstraint("longitude BETWEEN -180 AND 180", name="chk_loc_lng"),
    )


class CompanionshipRequest(Base):
    __tablename__ = "companionship_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    senior_id = Column(Integer, ForeignKey("seniors.id", ondelete="CASCADE"), nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(CompanionshipStatus), default=CompanionshipStatus.REQUESTED, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    accepted_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
