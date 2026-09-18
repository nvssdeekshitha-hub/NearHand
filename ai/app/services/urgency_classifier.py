from typing import Dict, Any, Tuple
from app.schemas import UrgencyLevel, RequestType


def calculate_risk_score_and_urgency(
    request_type: RequestType,
    emergency: bool,
    potential_emergency: bool,
    fall_detected: bool,
    mobility_issue: bool,
    medical_attention_possible: bool,
    companionship: bool,
    has_severe_symptoms: bool = False
) -> Tuple[int, UrgencyLevel]:
    """
    Calculates a bounded priority risk score (0-100) and maps to UrgencyLevel.
    This is a care coordination priority score, NOT a medical probability score.
    """
    # Baseline score by request type
    base_scores = {
        RequestType.EMERGENCY: 85,
        RequestType.FALL: 75,
        RequestType.MEDICAL_HELP: 70,
        RequestType.MEDICATION: 25,
        RequestType.LOCATION_DEVIATION: 50,
        RequestType.GENERAL_HELP: 35,
        RequestType.COMPANIONSHIP: 10,
        RequestType.OTHER: 30,
    }

    score = base_scores.get(request_type, 30)

    # Signal modifiers
    if emergency:
        score += 15
    elif potential_emergency:
        score += 10

    if fall_detected:
        score += 10
        if mobility_issue:  # Fall + unable to stand/move
            score += 10

    if mobility_issue and not fall_detected:
        score += 15

    if has_severe_symptoms:
        score += 15

    if medical_attention_possible:
        score += 5

    if companionship and request_type == RequestType.COMPANIONSHIP:
        # Keep companionship low priority
        score = min(score, 20)

    # Clamp score to [0, 100]
    final_score = max(0, min(100, score))

    # Determine Urgency Level based on final score and critical flags
    if emergency or final_score >= 85 or (fall_detected and mobility_issue):
        urgency = UrgencyLevel.CRITICAL
    elif final_score >= 65:
        urgency = UrgencyLevel.HIGH
    elif final_score >= 35:
        urgency = UrgencyLevel.MEDIUM
    else:
        urgency = UrgencyLevel.LOW

    return final_score, urgency
