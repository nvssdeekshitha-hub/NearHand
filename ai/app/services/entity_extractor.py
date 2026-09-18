import re
from typing import Dict, Any, List, Optional
from app.schemas import Entities, RequestType


# Key phrase patterns for pattern matching extraction
FALL_PATTERNS = [
    r"\bfell\b", r"\bfallen\b", r"\bfall\b", r"\bpadipoyanu\b", r"\bpadipoya\b",
    r"\bpaddanu\b", r"\bgir gaya\b", r"\bgir gayi\b", r"\bvizhundhutten\b",
    r"\bbiddidene\b", r"\bveenu\b"
]

MOBILITY_PATTERNS = [
    r"cannot stand", r"can't stand", r"unable to stand", r"cannot get up",
    r"can't get up", r"levalekapothunnanu", r"levaleka", r"levaledu",
    r"utha nahi ja raha", r"uth nahi sakta", r"elundhirukka mudiyavillai",
    r"ezhunnelkan pattunnilla"
]

COMPANIONSHIP_PATTERNS = [
    r"\blonely\b", r"\balone\b", r"feel alone", r"someone to talk",
    r"need company", r"\bontari\b", r"\bontariga\b", r"\bakela\b", r"\bakele\b",
    r"\bthaniyaaga\b", r"\bekangi\b", r"\botthaykkanu\b"
]

MEDICATION_PATTERNS = [
    r"\bmedicine\b", r"\bmedication\b", r"\btablet\b", r"\bpill\b",
    r"\bmandulu\b", r"\bdawai\b", r"\bdava\b", r"\bmarundhu\b", r"\boushadha\b"
]

EMERGENCY_SYMPTOM_PATTERNS = {
    "chest pain": [r"chest pain", r"chhati me dard", r"nenju vali"],
    "difficulty breathing": [r"difficulty breathing", r"shortness of breath", r"saas lene me taklif"],
    "unconsciousness": [r"unconscious", r"passed out", r"fainted", r"spruha ledu"],
    "heavy bleeding": [r"heavy bleeding", r"bleeding profusely", r"raktham"],
    "severe dizziness": [r"severe dizziness", r"dizzy and weak", r"thalathippu"]
}

LOCATION_KEYWORDS = [
    "bathroom", "bedroom", "kitchen", "living room", "stairs", "temple",
    "outside", "garden", "street", "park", "balcony", "floor", "snanala gadi"
]


def extract_entities_and_flags(text: str, normalized_text: str = "") -> Dict[str, Any]:
    """
    Extracts structured entities, emergency indicators, and safety flags from text.
    Never invents facts not present in text.
    """
    combined = f"{text} {normalized_text}".lower()

    # 1. Fall detection
    fall_detected = any(re.search(pat, combined) for pat in FALL_PATTERNS)

    # 2. Mobility issue
    mobility_issue = any(re.search(pat, combined) for pat in MOBILITY_PATTERNS)

    # 3. Companionship
    companionship = any(re.search(pat, combined) for pat in COMPANIONSHIP_PATTERNS)

    # 4. Emergency symptoms
    detected_symptoms: List[str] = []
    for symptom_name, patterns in EMERGENCY_SYMPTOM_PATTERNS.items():
        if any(re.search(pat, combined) for pat in patterns):
            detected_symptoms.append(symptom_name)

    emergency = len(detected_symptoms) > 0 or (fall_detected and mobility_issue)
    potential_emergency = emergency or "dizzy" in combined or "pain" in combined

    # 5. Location extraction
    extracted_location: Optional[str] = None
    for loc in LOCATION_KEYWORDS:
        if loc in combined:
            extracted_location = loc
            break

    location_relevant = extracted_location is not None
    location_context = extracted_location

    # 6. Medication extraction
    medication_found = any(re.search(pat, combined) for pat in MEDICATION_PATTERNS)
    medication_val: Optional[str] = "medication mentioned" if medication_found else None

    # 7. Required support list
    required_support: List[str] = []
    if fall_detected or mobility_issue or emergency:
        required_support.append("immediate_assistance")
    if emergency or detected_symptoms or "doctor" in combined or "hospital" in combined:
        required_support.append("medical_attention")
    if medication_found:
        required_support.append("medication_assistance")
    if companionship:
        required_support.append("companionship_visit")
    if "groceries" in combined or "grocery" in combined or "food" in combined or "water" in combined:
        required_support.append("daily_living_assistance")
    if not required_support:
        required_support.append("general_assistance")

    medical_attention_possible = "medical_attention" in required_support or emergency or len(detected_symptoms) > 0

    entities = Entities(
        symptoms=detected_symptoms,
        medication=medication_val,
        location=extracted_location,
        time_reference="evening" if "evening" in combined else None,
        body_area_if_explicit="chest" if "chest" in combined else None,
    )

    return {
        "fall_detected": fall_detected,
        "mobility_issue": mobility_issue,
        "companionship": companionship,
        "emergency": emergency,
        "potential_emergency": potential_emergency,
        "medical_attention_possible": medical_attention_possible,
        "location_relevant": location_relevant,
        "location_context": location_context,
        "required_support": required_support,
        "entities": entities,
        "detected_symptoms": detected_symptoms
    }
