import re
from typing import Optional
from app.schemas import AnalysisResultData, RequestType, UrgencyLevel, Entities
from app.services.language_service import detect_language
from app.utils.normalization import normalize_to_english_summary, clean_input_text
from app.services.entity_extractor import extract_entities_and_flags
from app.services.urgency_classifier import calculate_risk_score_and_urgency
from app.services.explanation_service import generate_explanation


def analyze_request_fallback(
    text: str,
    transcript: Optional[str] = None
) -> AnalysisResultData:
    """
    Deterministic rule-based analyzer used when external LLM APIs are unreachable,
    unconfigured, or return invalid JSON. Generates identical schema.
    """
    cleaned = clean_input_text(text)
    
    # 1. Detect language
    lang_info = detect_language(cleaned)
    lang_name = lang_info["language_name"]
    lang_code = lang_info["language_code"]

    # 2. Normalize text to English representation
    normalized = normalize_to_english_summary(cleaned, lang_code)

    # 3. Extract entities and flags
    extractions = extract_entities_and_flags(cleaned, normalized)
    fall_detected = extractions["fall_detected"]
    mobility_issue = extractions["mobility_issue"]
    companionship = extractions["companionship"]
    emergency = extractions["emergency"]
    potential_emergency = extractions["potential_emergency"]
    medical_attention_possible = extractions["medical_attention_possible"]
    location_relevant = extractions["location_relevant"]
    location_context = extractions["location_context"]
    required_support = extractions["required_support"]
    entities = extractions["entities"]
    detected_symptoms = extractions["detected_symptoms"]

    # 4. Determine Request Type
    combined_lowered = f"{cleaned} {normalized}".lower()
    
    if fall_detected:
        request_type = RequestType.FALL
    elif emergency or len(detected_symptoms) > 0:
        if "chest pain" in combined_lowered or "breathing" in combined_lowered or "unconscious" in combined_lowered:
            request_type = RequestType.EMERGENCY
        else:
            request_type = RequestType.MEDICAL_HELP
    elif companionship:
        request_type = RequestType.COMPANIONSHIP
    elif entities.medication is not None:
        request_type = RequestType.MEDICATION
    elif "groceries" in combined_lowered or "grocery" in combined_lowered or "walk" in combined_lowered:
        request_type = RequestType.GENERAL_HELP
    elif cleaned == "I need help." or cleaned == "help":
        request_type = RequestType.GENERAL_HELP
    else:
        request_type = RequestType.GENERAL_HELP

    # 5. Calculate Risk Score and Urgency Level
    risk_score, urgency = calculate_risk_score_and_urgency(
        request_type=request_type,
        emergency=emergency,
        potential_emergency=potential_emergency,
        fall_detected=fall_detected,
        mobility_issue=mobility_issue,
        medical_attention_possible=medical_attention_possible,
        companionship=companionship,
        has_severe_symptoms=len(detected_symptoms) > 0
    )

    # 6. Generate human-readable factual explanation
    explanation = generate_explanation(
        request_type=request_type,
        urgency=urgency,
        fall_detected=fall_detected,
        mobility_issue=mobility_issue,
        location_context=location_context,
        symptoms=detected_symptoms,
        companionship=companionship
    )

    # Confidence calculation: lower confidence for vague input ("I need help")
    confidence = 0.94
    if cleaned.strip().lower() in ["i need help.", "i need help", "help"]:
        confidence = 0.60

    return AnalysisResultData(
        language=lang_name,
        language_code=lang_code,
        transcript=transcript,
        normalized_text=normalized,
        request_type=request_type,
        urgency=urgency,
        risk_score=risk_score,
        emergency=emergency,
        potential_emergency=potential_emergency,
        fall_detected=fall_detected,
        mobility_issue=mobility_issue,
        medical_attention_possible=medical_attention_possible,
        companionship=companionship,
        location_relevant=location_relevant,
        location_context=location_context,
        required_support=required_support,
        entities=entities,
        explanation=explanation,
        confidence=confidence
    )
