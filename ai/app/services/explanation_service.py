from app.schemas import RequestType, UrgencyLevel


def generate_explanation(
    request_type: RequestType,
    urgency: UrgencyLevel,
    fall_detected: bool,
    mobility_issue: bool,
    location_context: str = None,
    symptoms: list = None,
    companionship: bool = False
) -> str:
    """
    Generates a concise, evidence-based human readable summary for care coordination.
    Does NOT diagnose or make medical safety guarantees.
    """
    evidence_parts = []

    if fall_detected:
        evidence_parts.append("a fall")
    if mobility_issue:
        evidence_parts.append("inability to stand")
    if location_context:
        evidence_parts.append(f"location in the {location_context}")
    if symptoms:
        evidence_parts.append(f"symptoms of {', '.join(symptoms)}")

    if request_type == RequestType.FALL and fall_detected and mobility_issue:
        loc_str = f" in the {location_context}" if location_context else ""
        return f"The senior reports a fall{loc_str} and inability to stand, indicating a high-priority care coordination request."

    if request_type == RequestType.COMPANIONSHIP or companionship:
        return "The senior expresses feeling lonely and requests companionship support."

    if request_type == RequestType.MEDICATION:
        return "The senior requests assistance regarding scheduled medication."

    if request_type == RequestType.EMERGENCY or urgency == UrgencyLevel.CRITICAL:
        if evidence_parts:
            return f"The senior reports {', '.join(evidence_parts)}, requiring immediate emergency care coordination."
        return "The senior expresses severe indicators requiring immediate critical care coordination."

    if request_type == RequestType.GENERAL_HELP:
        return "The senior requests general non-emergency assistance for daily living."

    if evidence_parts:
        return f"The senior indicates {', '.join(evidence_parts)}, assessed for {urgency.value.lower()} priority care coordination."

    return f"The senior submitted a {request_type.value.lower().replace('_', ' ')} request prioritized as {urgency.value} for care coordination."
