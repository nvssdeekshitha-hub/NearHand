import pytest
from fastapi.testclient import TestClient

from app.main import app, analyze_text_request, analyze_audio_request
from app.schemas import RequestType, UrgencyLevel
from app.services.fallback_analyzer import analyze_request_fallback

client = TestClient(app)


# --- TEST CASE 1: Telugu Fall ---
@pytest.mark.asyncio
async def test_telugu_fall():
    input_text = "Nenu bathroom lo padipoyanu, levalekapothunnanu."
    result = await analyze_text_request(input_text)

    assert result.language_code == "te"
    assert result.language == "Telugu"
    assert result.request_type == RequestType.FALL
    assert result.urgency == UrgencyLevel.CRITICAL
    assert result.fall_detected is True
    assert result.mobility_issue is True
    assert result.risk_score >= 85
    assert "immediate_assistance" in result.required_support
    assert "bathroom" in (result.location_context or "").lower()


# --- TEST CASE 2: English Companionship ---
@pytest.mark.asyncio
async def test_english_companionship():
    input_text = "I feel lonely and want someone to talk to."
    result = await analyze_text_request(input_text)

    assert result.request_type == RequestType.COMPANIONSHIP
    assert result.urgency == UrgencyLevel.LOW
    assert result.companionship is True
    assert result.risk_score <= 20
    assert "companionship_visit" in result.required_support


# --- TEST CASE 3: Medication ---
@pytest.mark.asyncio
async def test_medication():
    input_text = "I forgot to take my evening medicine."
    result = await analyze_text_request(input_text)

    assert result.request_type == RequestType.MEDICATION
    assert "medication_assistance" in result.required_support
    assert result.entities.medication is not None


# --- TEST CASE 4: General Help ---
@pytest.mark.asyncio
async def test_general_help():
    input_text = "Can someone help me get groceries?"
    result = await analyze_text_request(input_text)

    assert result.request_type == RequestType.GENERAL_HELP
    assert result.urgency in [UrgencyLevel.MEDIUM, UrgencyLevel.LOW]


# --- TEST CASE 5: Emergency Indicators ---
@pytest.mark.asyncio
async def test_emergency_indicators():
    input_text = "I have severe chest pain and difficulty breathing."
    result = await analyze_text_request(input_text)

    assert result.request_type in [RequestType.EMERGENCY, RequestType.MEDICAL_HELP]
    assert result.urgency in [UrgencyLevel.CRITICAL, UrgencyLevel.HIGH]
    assert (result.emergency or result.potential_emergency) is True
    assert result.medical_attention_possible is True
    assert "chest pain" in result.entities.symptoms or "difficulty breathing" in result.entities.symptoms


# --- TEST CASE 6: Unknown Request ---
@pytest.mark.asyncio
async def test_unknown_request():
    input_text = "I need help."
    result = await analyze_text_request(input_text)

    assert result.request_type == RequestType.GENERAL_HELP
    assert result.confidence <= 0.70


# --- TEST CASE 7: Deterministic Fallback Direct Test ---
def test_fallback_analyzer():
    input_text = "Nenu bathroom lo padipoyanu, levalekapothunnanu."
    result = analyze_request_fallback(input_text)

    assert result.language_code == "te"
    assert result.request_type == RequestType.FALL
    assert result.urgency == UrgencyLevel.CRITICAL
    assert result.risk_score >= 85
    assert result.fall_detected is True
    assert result.mobility_issue is True


# --- TEST CASE 8: FastAPI REST Endpoint /ai/analyze-text ---
def test_rest_analyze_text():
    response = client.post(
        "/ai/analyze-text",
        json={"text": "Nenu bathroom lo padipoyanu, levalekapothunnanu."}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]
    assert data["language_code"] == "te"
    assert data["request_type"] == "FALL"
    assert data["urgency"] == "CRITICAL"
    assert data["risk_score"] >= 85


# --- TEST CASE 9: FastAPI REST Endpoint /ai/analyze-audio ---
def test_rest_analyze_audio():
    # Mock audio file upload
    file_bytes = b"RIFF....WAVEfmt ....data...."
    response = client.post(
        "/ai/analyze-audio",
        files={"file": ("telugu_fall.wav", file_bytes, "audio/wav")}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]
    assert data["transcript"] is not None
    assert data["request_type"] == "FALL"


# --- TEST CASE 10: Health Check Endpoint ---
def test_health_check():
    response = client.get("/ai/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert json_data["fallback_available"] is True
