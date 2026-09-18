from typing import Dict, Any
from app.utils.normalization import clean_input_text, detect_script_by_unicode

# Romanized keyword indicators for Indian languages
ROMANIZED_KEYWORDS = {
    "te": {
        "name": "Telugu",
        "keywords": [
            "nenu", "padipoyanu", "levalekapothunnanu", "padipoya", "levaleka",
            "sahayam", "ontari", "ontariga", "mandulu", "snanala", "bathroom lo",
            "kavali", "levaledu", "padda", "paddanu", "doctoru", "vali"
        ]
    },
    "hi": {
        "name": "Hindi",
        "keywords": [
            "mujhe", "madad", "chahiye", "gir", "gaya", "gayi", "takleef",
            "dard", "akele", "akela", "dawai", "dava", "chhati", "saas",
            "khana", "sahayata", "hospitall", "bhookh"
        ]
    },
    "ta": {
        "name": "Tamil",
        "keywords": [
            "naan", "vizhundhutten", "mudiyavillai", "udhavai", "thaniyaaga",
            "irukiren", "marundhu", "vali", "nenju", "keezhe", "elundhirukka"
        ]
    },
    "kn": {
        "name": "Kannada",
        "keywords": [
            "nanu", "biddidene", "sahaya", "beku", "ekangi", "nanna",
            "oushadha", "yelalu", "yellidane", "tumbane"
        ]
    },
    "ml": {
        "name": "Malayalam",
        "keywords": [
            "njan", "veenu", "sahayam", "venam", "otthaykkanu", "marrunnu",
            "neer", "vedhana", "ezhunnelkan"
        ]
    }
}


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detects language of input text (supports native script & transliterated romanized text).
    Returns dict: {"language_code": "te", "language_name": "Telugu", "confidence": 0.98}
    """
    cleaned = clean_input_text(text)
    if not cleaned:
        return {
            "language_code": "en",
            "language_name": "English",
            "confidence": 1.0
        }

    # First check unicode script detection (for native scripts like Telugu/Devanagari/Tamil)
    lang_code, lang_name = detect_script_by_unicode(cleaned)
    if lang_code != "en":
        return {
            "language_code": lang_code,
            "language_name": lang_name,
            "confidence": 0.98
        }

    # If text is written in Latin alphabet, check for Romanized Indian language keywords
    lowered = cleaned.lower()
    scores = {}

    for code, info in ROMANIZED_KEYWORDS.items():
        match_count = 0
        for kw in info["keywords"]:
            if kw in lowered:
                match_count += 1
        if match_count > 0:
            scores[code] = (match_count, info["name"])

    if scores:
        best_code = max(scores, key=lambda k: scores[k][0])
        best_count, best_name = scores[best_code]
        confidence = min(0.70 + (best_count * 0.10), 0.98)
        return {
            "language_code": best_code,
            "language_name": best_name,
            "confidence": round(confidence, 2)
        }

    # Default to English if no Indian language keywords matched
    return {
        "language_code": "en",
        "language_name": "English",
        "confidence": 0.90
    }
