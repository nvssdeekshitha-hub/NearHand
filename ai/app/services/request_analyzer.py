import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

import httpx
from app.config import settings
from app.schemas import AnalysisResultData
from app.services.fallback_analyzer import analyze_request_fallback
from app.services.urgency_classifier import calculate_risk_score_and_urgency

logger = logging.getLogger("nearhand.ai.analyzer")

# Load system prompt
PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "request_analysis_prompt.txt"
try:
    SYSTEM_PROMPT = PROMPT_FILE.read_text(encoding="utf-8")
except Exception:
    SYSTEM_PROMPT = "You are an AI care coordination analyzer. Return structured JSON only."


async def call_gemini_api(text: str) -> Optional[Dict[str, Any]]:
    """Calls Google Gemini REST API using httpx."""
    if not settings.AI_API_KEY:
        return None

    model = settings.AI_MODEL or "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={settings.AI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": f"User Request: {text}"}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }

    try:
        async with httpx.AsyncClient(timeout=float(settings.AI_TIMEOUT_SECONDS)) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(content)
    except Exception as e:
        logger.warning(f"Gemini API call failed: {e}")
    return None


async def call_openai_api(text: str) -> Optional[Dict[str, Any]]:
    """Calls OpenAI API using httpx."""
    if not settings.AI_API_KEY:
        return None

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {settings.AI_API_KEY}"}
    payload = {
        "model": settings.AI_MODEL or "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }

    try:
        async with httpx.AsyncClient(timeout=float(settings.AI_TIMEOUT_SECONDS)) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
    except Exception as e:
        logger.warning(f"OpenAI API call failed: {e}")
    return None


async def analyze_request(
    text: str,
    transcript: Optional[str] = None
) -> AnalysisResultData:
    """
    Main entrypoint for AI request understanding.
    Tries external LLM provider if configured. Fallback to deterministic analyzer if
    API key is missing, network fails, or response is invalid.
    """
    llm_output: Optional[Dict[str, Any]] = None

    if settings.AI_API_KEY and settings.ENABLE_AI_FALLBACK:
        provider = settings.AI_PROVIDER.lower()
        if provider == "gemini":
            llm_output = await call_gemini_api(text)
        elif provider == "openai":
            llm_output = await call_openai_api(text)

    # If LLM response succeeded, validate and enforce deterministic scoring
    if llm_output:
        try:
            # Overwrite/refine risk score with transparent deterministic scoring layer
            fall_detected = llm_output.get("fall_detected", False)
            mobility_issue = llm_output.get("mobility_issue", False)
            emergency = llm_output.get("emergency", False)
            potential_emergency = llm_output.get("potential_emergency", False)
            medical_attention_possible = llm_output.get("medical_attention_possible", False)
            companionship = llm_output.get("companionship", False)
            req_type_str = llm_output.get("request_type", "GENERAL_HELP")

            risk_score, urgency = calculate_risk_score_and_urgency(
                request_type=req_type_str,
                emergency=emergency,
                potential_emergency=potential_emergency,
                fall_detected=fall_detected,
                mobility_issue=mobility_issue,
                medical_attention_possible=medical_attention_possible,
                companionship=companionship
            )

            llm_output["risk_score"] = risk_score
            llm_output["urgency"] = urgency.value
            if transcript and not llm_output.get("transcript"):
                llm_output["transcript"] = transcript

            return AnalysisResultData(**llm_output)
        except Exception as err:
            logger.warning(f"Error parsing LLM response into schema: {err}. Using fallback.")

    # Graceful fallback analyzer execution
    return analyze_request_fallback(text, transcript=transcript)
