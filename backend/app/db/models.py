from datetime import datetime, timezone
import enum
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship as db_relationship

from app.db.database import Base

class UserRole(str, enum.Enum):
    SENIOR = "SENIOR"
    CARETAKER = "CARETAKER"
    VOLUNTEER = "VOLUNTEER"
    FAMILY = "FAMILY"
    ADMIN = "ADMIN"

class RequestType(str, enum.Enum):
    FALL = "FALL"
    MEDICAL_HELP = "MEDICAL_HELP"
    MEDICATION = "MEDICATION"
    COMPANIONSHIP = "COMPANIONSHIP"
    LOCATION_DEVIATION = "LOCATION_DEVIATION"
    GENERAL_HELP = "GENERAL_HELP"
    EMERGENCY = "EMERGENCY"
    OTHER = "OTHER"

class RequestUrgency(str, enum.Enum):
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.SENIOR.value)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    senior_profile = db_relationship("Senior", back_populates="user", uselist=False)
    caretaker_profile = db_relationship("Caretaker", back_populates="user", uselist=False)
    volunteer_profile = db_relationship("Volunteer", back_populates="user", uselist=False)
    family_profile = db_relationship("Family", back_populates="user", uselist=False)

class Senior(Base):
    __tablename__ = "seniors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    preferred_language = Column(String(30), default="English")
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    home_latitude = Column(Float, nullable=True)
    home_longitude = Column(Float, nullable=True)
    location_deviation_threshold_km = Column(Float, default=1.0)
    emergency_contact = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = db_relationship("User", back_populates="senior_profile")
    requests = db_relationship("Request", back_populates="senior")
    caretaker_associations = db_relationship("CaretakerSenior", back_populates="senior")
    family_members = db_relationship("Family", back_populates="senior")
    medical_records = db_relationship("MedicalRecord", back_populates="senior", uselist=False)
    location_events = db_relationship("LocationEvent", back_populates="senior")
    medications = db_relationship("Medication", back_populates="senior")

class Caretaker(Base):
    __tablename__ = "caretakers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    availability_status = Column(Boolean, default=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    max_seniors = Column(Integer, default=10)
    current_load = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = db_relationship("User", back_populates="caretaker_profile")
    senior_associations = db_relationship("CaretakerSenior", back_populates="caretaker")

class CaretakerSenior(Base):
    __tablename__ = "caretaker_seniors"

    id = Column(Integer, primary_key=True, index=True)
    caretaker_id = Column(Integer, ForeignKey("caretakers.id"), nullable=False)
    senior_id = Column(Integer, ForeignKey("seniors.id"), nullable=False)
    is_primary = Column(Boolean, default=True)
    assigned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    caretaker = db_relationship("Caretaker", back_populates="senior_associations")
    senior = db_relationship("Senior", back_populates="caretaker_associations")

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    availability_status = Column(Boolean, default=True)
    max_distance_km = Column(Float, default=5.0)
    skills = Column(Text, default="[]")  # JSON string of skills
    first_aid_trained = Column(Boolean, default=False)
    current_active_requests = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = db_relationship("User", back_populates="volunteer_profile")

class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    senior_id = Column(Integer, ForeignKey("seniors.id"), nullable=False)
    relationship = Column(String(50), nullable=False)
    can_receive_emergency_alerts = Column(Boolean, default=True)
    can_view_health = Column(Boolean, default=True)
    can_view_location = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = db_relationship("User", back_populates="family_profile")
    senior = db_relationship("Senior", back_populates="family_members")

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"), nullable=False, unique=True)
    conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    blood_group = Column(String(10), nullable=True)
    important_notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    senior = db_relationship("Senior", back_populates="medical_records")

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"), nullable=False)
    message = Column(Text, nullable=False)
    input_type = Column(String(20), default="TEXT")
    language = Column(String(30), default="English")
    request_type = Column(String(30), default=RequestType.GENERAL_HELP.value)
    urgency = Column(String(20), default=RequestUrgency.MEDIUM.value)
    risk_score = Column(Integer, default=50)
    emergency = Column(Boolean, default=False)
    mobility_issue = Column(Boolean, default=False)
    medical_attention_possible = Column(Boolean, default=False)
    required_support = Column(Text, default="[]")  # JSON string array
    companionship = Column(Boolean, default=False)
    status = Column(String(30), default=RequestStatus.CREATED.value)
    target_response_minutes = Column(Integer, default=10)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    senior = db_relationship("Senior", back_populates="requests")
    assignments = db_relationship("Assignment", back_populates="request")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    responder_type = Column(String(30), nullable=False)  # CARETAKER, VOLUNTEER, ADDITIONAL_CARETAKER
    responder_id = Column(Integer, nullable=False)       # Caretaker.id or Volunteer.id
    assignment_status = Column(String(30), default=AssignmentStatus.PENDING.value)
    assigned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    accepted_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    response_deadline = Column(DateTime, nullable=True)
    distance_km = Column(Float, nullable=True)
    eta_minutes = Column(Integer, nullable=True)

    request = db_relationship("Request", back_populates="assignments")

class LocationEvent(Base):
    __tablename__ = "location_events"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_deviation = Column(Boolean, default=False)
    expected_trip = Column(Boolean, default=False)

    senior = db_relationship("Senior", back_populates="location_events")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=True)
    type = Column(String(50), nullable=False)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"), nullable=False)
    medicine_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    schedule = Column(String(100), nullable=False)
    taken_today = Column(Boolean, default=False)
    last_taken_at = Column(DateTime, nullable=True)

    senior = db_relationship("Senior", back_populates="medications")
