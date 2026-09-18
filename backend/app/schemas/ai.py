from typing import List, Optional
from pydantic import BaseModel

class AIAnalysisResult(BaseModel):
    language: str
    request_type: str
    urgency: str
    risk_score: int
    emergency: bool
    required_support: List[str]
    explanation: Optional[str] = None
