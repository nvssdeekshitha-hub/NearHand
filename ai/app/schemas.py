from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RequestType(str, Enum):
    FALL = "FALL"
    MEDICAL_HELP = "MEDICAL_HELP"
    MEDICATION = "MEDICATION"
    COMPANIONSHIP = "COMPANIONSHIP"
    LOCATION_DEVIATION = "LOCATION_DEVIATION"
    GENERAL_HELP = "GENERAL_HELP"
    EMERGENCY = "EMERGENCY"
    OTHER = "OTHER"


class UrgencyLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Entities(BaseModel):
    symptoms: List[str] = Field(default_factory=list)
    medication: Optional[str] = None
    location: Optional[str] = None
    time_reference: Optional[str] = None
    body_area_if_explicit: Optional[str] = None


class AnalysisResultData(BaseModel):
    language: str = Field(description="Full name of detected language, e.g., Telugu, English")
    language_code: str = Field(description="2-letter ISO code, e.g., te, en, hi")
    transcript: Optional[str] = Field(default=None, description="Audio transcript if input was audio")
    normalized_text: str = Field(description="Standardized English representation of the request")
    request_type: RequestType = Field(description="Primary category of the request")
    urgency: UrgencyLevel = Field(description="Assessed urgency level for coordination")
    risk_score: int = Field(ge=0, le=100, description="Coordination priority risk score between 0 and 100")
    emergency: bool = Field(default=False, description="Flag indicating immediate critical emergency")
    potential_emergency: bool = Field(default=False, description="Flag indicating potential emergency condition")
    fall_detected: bool = Field(default=False, description="Flag indicating a senior fall event")
    mobility_issue: bool = Field(default=False, description="Flag indicating inability to move or stand")
    medical_attention_possible: bool = Field(default=False, description="Flag indicating medical care may be required")
    companionship: bool = Field(default=False, description="Flag indicating request for companionship/social connection")
    location_relevant: bool = Field(default=False, description="Flag indicating location context is specified in text")
    location_context: Optional[str] = Field(default=None, description="Extracted location details (e.g., bathroom, outside temple)")
    required_support: List[str] = Field(default_factory=list, description="Extracted required support actions")
    entities: Entities = Field(default_factory=Entities, description="Structured extracted entities")
    explanation: str = Field(description="Short factual, evidence-based AI summary for care coordination")
    confidence: float = Field(ge=0.0, le=1.0, description="AI confidence score in interpretation")


class AnalyzeTextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text message from senior citizen")


class ApiResponse(BaseModel):
    success: bool = True
    data: Optional[AnalysisResultData] = None
    error: Optional[str] = None


class HealthCheckResponse(BaseModel):
    status: str
    ai_provider: str
    fallback_available: bool


class SpeechTranscriptionResult(BaseModel):
    transcript: str
    language: str
    confidence: float = 0.95
