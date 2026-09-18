import re
from typing import Tuple


def clean_input_text(text: str) -> str:
    """Removes extra whitespace and non-printable characters."""
    if not text:
        return ""
    # Replace multiple spaces/newlines with single space
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()


def detect_script_by_unicode(text: str) -> Tuple[str, str]:
    """
    Detects primary script from Unicode character ranges.
    Returns (language_code, language_name).
    """
    text = text.strip()
    if not text:
        return ("en", "English")

    counts = {
        "te": 0,  # Telugu: 0C00-0C7F
        "hi": 0,  # Devanagari (Hindi): 0900-097F
        "ta": 0,  # Tamil: 0B80-0BFF
        "kn": 0,  # Kannada: 0C80-0CFF
        "ml": 0,  # Malayalam: 0D00-0D7F
        "en": 0,  # Basic Latin: 0000-007F
    }

    for char in text:
        cp = ord(char)
        if 0x0C00 <= cp <= 0x0C7F:
            counts["te"] += 1
        elif 0x0900 <= cp <= 0x097F:
            counts["hi"] += 1
        elif 0x0B80 <= cp <= 0x0BFF:
            counts["ta"] += 1
        elif 0x0C80 <= cp <= 0x0CFF:
            counts["kn"] += 1
        elif 0x0D00 <= cp <= 0x0D7F:
            counts["ml"] += 1
        elif (0x0041 <= cp <= 0x005A) or (0x0061 <= cp <= 0x007A):
            counts["en"] += 1

    # Find dominant script among non-English Indian languages first
    indian_lang_counts = {k: v for k, v in counts.items() if k != "en"}
    max_indian_lang = max(indian_lang_counts, key=indian_lang_counts.get)

    if indian_lang_counts[max_indian_lang] > 0:
        code_to_name = {
            "te": "Telugu",
            "hi": "Hindi",
            "ta": "Tamil",
            "kn": "Kannada",
            "ml": "Malayalam",
        }
        return (max_indian_lang, code_to_name[max_indian_lang])

    return ("en", "English")


# Common transliterated (Romanized) phrase mappings for fallback text normalization
ROMANIZED_PHRASE_TRANSLATIONS = {
    "nenu bathroom lo padipoyanu": "I fell in the bathroom",
    "levalekapothunnanu": "and cannot stand up",
    "padipoyanu": "fell down",
    "mujeh madad chahiye": "I need help",
    "mai gir gaya": "I fell down",
    "chhatia me dard": "chest pain",
    "saas lene me taklif": "difficulty breathing",
    "naan keezhe vizhundhutten": "I fell down",
    "elundhirukka mudiyavillai": "cannot get up",
    "naan thaniyaaga irukiren": "I feel lonely",
}


def normalize_to_english_summary(text: str, language_code: str) -> str:
    """
    Generates a clean English normalized text summary of the senior's input.
    """
    cleaned = clean_input_text(text)
    if not cleaned:
        return ""

    if language_code == "en":
        return cleaned

    # Check known transliterated phrases for demo reliability
    lowered = cleaned.lower()
    matches = []
    for pattern, target in ROMANIZED_PHRASE_TRANSLATIONS.items():
        if pattern in lowered:
            matches.append(target)

    if matches:
        return " ".join(matches) + "."

    # Default fallback: return clean text with language tag note if untranslated
    return f"{cleaned} (Original: {language_code})"
