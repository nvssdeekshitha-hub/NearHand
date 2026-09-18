from sqlalchemy.orm import relationship
from app.models import (
    User,
    Senior,
    Caretaker,
    CaretakerSenior,
    Volunteer,
    FamilyMember,
    MedicalRecord,
    Medication,
    Request,
    Assignment,
    Notification,
    LocationEvent,
    CompanionshipRequest,
    AuditLog
)

# User Relationships
User.senior = relationship("Senior", back_populates="user", uselist=False, cascade="all, delete-orphan")
User.caretaker = relationship("Caretaker", back_populates="user", uselist=False, cascade="all, delete-orphan")
User.volunteer = relationship("Volunteer", back_populates="user", uselist=False, cascade="all, delete-orphan")
User.family_memberships = relationship("FamilyMember", back_populates="user", cascade="all, delete-orphan")
User.assignments = relationship("Assignment", back_populates="responder", cascade="all, delete-orphan")
User.notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
User.audit_logs = relationship("AuditLog", back_populates="user")

# Senior Relationships
Senior.user = relationship("User", back_populates="senior")
Senior.caretaker_links = relationship("CaretakerSenior", back_populates="senior", cascade="all, delete-orphan")
Senior.family_members = relationship("FamilyMember", back_populates="senior", cascade="all, delete-orphan")
Senior.medical_records = relationship("MedicalRecord", back_populates="senior", cascade="all, delete-orphan")
Senior.medications = relationship("Medication", back_populates="senior", cascade="all, delete-orphan")
Senior.requests = relationship("Request", back_populates="senior", cascade="all, delete-orphan")
Senior.location_events = relationship("LocationEvent", back_populates="senior", cascade="all, delete-orphan")
Senior.companionship_requests = relationship("CompanionshipRequest", back_populates="senior", cascade="all, delete-orphan")

# Caretaker Relationships
Caretaker.user = relationship("User", back_populates="caretaker")
Caretaker.senior_links = relationship("CaretakerSenior", back_populates="caretaker", cascade="all, delete-orphan")

# CaretakerSenior Join Table Relationships
CaretakerSenior.caretaker = relationship("Caretaker", back_populates="senior_links")
CaretakerSenior.senior = relationship("Senior", back_populates="caretaker_links")

# Volunteer Relationships
Volunteer.user = relationship("User", back_populates="volunteer")

# FamilyMember Relationships
FamilyMember.user = relationship("User", back_populates="family_memberships")
FamilyMember.senior = relationship("Senior", back_populates="family_members")

# MedicalRecord Relationships
MedicalRecord.senior = relationship("Senior", back_populates="medical_records")

# Medication Relationships
Medication.senior = relationship("Senior", back_populates="medications")

# Request Relationships
Request.senior = relationship("Senior", back_populates="requests")
Request.assignments = relationship("Assignment", back_populates="request", cascade="all, delete-orphan")
Request.notifications = relationship("Notification", back_populates="request", cascade="all, delete-orphan")
Request.companionship_requests = relationship("CompanionshipRequest", back_populates="request", cascade="all, delete-orphan")

# Assignment Relationships
Assignment.request = relationship("Request", back_populates="assignments")
Assignment.responder = relationship("User", back_populates="assignments")

# Notification Relationships
Notification.user = relationship("User", back_populates="notifications")
Notification.request = relationship("Request", back_populates="notifications")

# LocationEvent Relationships
LocationEvent.senior = relationship("Senior", back_populates="location_events")

# CompanionshipRequest Relationships
CompanionshipRequest.senior = relationship("Senior", back_populates="companionship_requests")
CompanionshipRequest.request = relationship("Request", back_populates="companionship_requests")

# AuditLog Relationships
AuditLog.user = relationship("User", back_populates="audit_logs")
