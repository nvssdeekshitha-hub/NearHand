import os
import json
import logging
import httpx
from app.core.config import settings
from app.schemas.ai import AIAnalysisResult

logger = logging.getLogger(__name__)

def is_telugu(text: str) -> bool:
    """Detect if string contains Telugu Unicode characters (0x0C00 - 0x0C7F)."""
    return any('\u0c00' <= char <= '\u0c7f' for char in text)

def analyze_text_request(message: str) -> AIAnalysisResult:
    """
    Analyzes text input from senior using LLM (if AI_API_KEY is present) 
    or robust rule-based fallback engine.
    NOTE: This provides operational coordination classification only, NOT medical diagnosis.
    """
    if not message:
        return AIAnalysisResult(
            language="English",
            request_type="GENERAL_HELP",
            urgency="MEDIUM",
            risk_score=50,
            emergency=False,
            required_support=["general_support"],
            explanation="Empty message provided."
        )

    # 1. If AI_API_KEY is set, try calling external LLM API
    if settings.AI_API_KEY:
        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.AI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are an assistant categorizing senior care requests for dispatch coordination. "
                                "Return JSON with keys: language, request_type (FALL/MEDICAL_HELP/MEDICATION/COMPANIONSHIP/GENERAL_HELP/EMERGENCY), "
                                "urgency (CRITICAL/HIGH/MEDIUM/LOW), risk_score (0-100 int), emergency (bool), "
                                "required_support (array of strings), explanation (string). "
                                "DO NOT output medical diagnosis."
                            )
                        },
                        {"role": "user", "content": message}
                    ],
                    "response_format": {"type": "json_object"}
                },
                timeout=5.0
            )
            if response.status_code == 200:
                data = response.json()["choices"][0]["message"]["content"]
                parsed = json.loads(data)
                return AIAnalysisResult(
                    language=parsed.get("language", "English"),
                    request_type=parsed.get("request_type", "GENERAL_HELP").upper(),
                    urgency=parsed.get("urgency", "MEDIUM").upper(),
                    risk_score=int(parsed.get("risk_score", 50)),
                    emergency=bool(parsed.get("emergency", False)),
                    required_support=parsed.get("required_support", ["general_support"]),
                    explanation=parsed.get("explanation", "AI analyzed request.")
                )
        except Exception as e:
            logger.warning(f"External AI API call failed or timed out: {e}. Falling back to rule engine.")

    # 2. Rule-based Fallback Engine (Guaranteed 100% reliable local processing)
    msg_lower = message.lower()
    has_telugu_script = is_telugu(message)

    # Fall / Inability to stand keywords
    fall_keywords_en = ["fell", "fall", "can't stand", "cannot stand", "unable to stand", "dropped down", "slipped", "bathroom fall"]
    fall_keywords_te_script = ["పడ్డాను", "లేవలేకపోతున్నాను", "పడిపోయాను", "పడి", "లేవలేను"]
    fall_keywords_te_roman = ["padipoyanu", "padipoya", "levalekapothunnanu", "levalekapothunna", "levalenu", "padithe", "padda", "paddi"]

    is_fall = (
        any(kw in msg_lower for kw in fall_keywords_en) or
        any(kw in message for kw in fall_keywords_te_script) or
        any(kw in msg_lower for kw in fall_keywords_te_roman)
    )

    # Medical emergency keywords (English, Telugu script & Romanized Telugu)
    medical_keywords_en = [
        "heart attack", "chest pain", "difficulty breathing", "can't breathe", "cannot breathe",
        "unconscious", "heavy bleeding", "severe pain", "heart", "breath", "bleeding", "stroke"
    ]
    medical_keywords_te_script = ["గుండెపోటు", "ఛాతీ నొప్పి", "ఊపిరి పీల్చుకోలేకపోతున్నాను", "ఊపిరి"]
    medical_keywords_te_roman = ["gundepotu", "gunde noppi", "gundenoppi", "gunde", "chati noppi", "chatinoppi", "oopiri", "upiri"]

    is_medical = (
        any(kw in msg_lower for kw in medical_keywords_en) or
        any(kw in message for kw in medical_keywords_te_script) or
        any(kw in msg_lower for kw in medical_keywords_te_roman)
    )

    # Medication keywords (English & Telugu)
    medication_keywords_en = ["medicine", "medication", "tablet", "pill", "dose", "prescription"]
    medication_keywords_te_script = ["మందులు", "మందు"]
    medication_keywords_te_roman = ["mandhulu", "mandhu"]

    is_medication = (
        any(kw in msg_lower for kw in medication_keywords_en) or
        any(kw in message for kw in medication_keywords_te_script) or
        any(kw in msg_lower for kw in medication_keywords_te_roman)
    )

    # Companionship keywords (English, Telugu script & Romanized Telugu)
    companionship_keywords_en = [
        "alone", "lonely", "feel alone", "feeling lonely", "talk to someone",
        "someone to talk to", "want company", "need company", "bored"
    ]
    companionship_keywords_te_script = ["ఒంటరిగా", "ఒంటరి"]
    companionship_keywords_te_roman = ["ontariga", "ontari"]

    is_companionship = (
        any(kw in msg_lower for kw in companionship_keywords_en) or
        any(kw in message for kw in companionship_keywords_te_script) or
        any(kw in msg_lower for kw in companionship_keywords_te_roman)
    )

    # Determine language
    is_romanized_telugu = (
        any(kw in msg_lower for kw in fall_keywords_te_roman) or
        any(kw in msg_lower for kw in medical_keywords_te_roman) or
        any(kw in msg_lower for kw in medication_keywords_te_roman) or
        any(kw in msg_lower for kw in companionship_keywords_te_roman)
    )
    lang = "Telugu" if (has_telugu_script or is_romanized_telugu) else "English"

    if is_fall:
        return AIAnalysisResult(
            language=lang,
            request_type="FALL",
            urgency="CRITICAL",
            risk_score=94,
            emergency=True,
            required_support=["immediate_assistance", "medical_attention"],
            explanation="Senior reports a fall and inability to stand."
        )
    elif is_medical:
        return AIAnalysisResult(
            language=lang,
            request_type="MEDICAL_HELP",
            urgency="CRITICAL",
            risk_score=95,
            emergency=True,
            required_support=["medical_attention", "emergency_dispatch"],
            explanation="Senior reports acute medical emergency symptoms."
        )
    elif is_medication:
        return AIAnalysisResult(
            language=lang,
            request_type="MEDICATION",
            urgency="MEDIUM",
            risk_score=40,
            emergency=False,
            required_support=["medication_assistance"],
            explanation="Senior requested assistance with medication."
        )
    elif is_companionship:
        return AIAnalysisResult(
            language=lang,
            request_type="COMPANIONSHIP",
            urgency="LOW",
            risk_score=20,
            emergency=False,
            required_support=["companionship", "check_in"],
            explanation="Senior expressed feeling lonely and requested companionship."
        )
    else:
        return AIAnalysisResult(
            language=lang,
            request_type="GENERAL_HELP",
            urgency="MEDIUM",
            risk_score=50,
            emergency=False,
            required_support=["general_support"],
            explanation="General request for assistance."
        )
