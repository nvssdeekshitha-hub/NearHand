# NEARHAND AI Integration Layer

> **Tagline:** “The right help. At the right time. For every senior.”

The **NEARHAND AI Integration Layer** is an AI-assisted care coordination analyzer for senior citizens. It processes natural language text or voice inputs in Indian languages and English, extracts structured care indicators, assigns transparent priority risk scores, and outputs a standardized JSON payload for care coordination.

> [!IMPORTANT]
> **Safety Disclaimer:** NEARHAND AI is an **AI-assisted care coordination system, NOT a medical diagnosis system**. The AI must understand and prioritize requests for care coordination purposes. It does NOT claim to diagnose diseases, guarantee medical outcomes, or determine that a person is medically safe for any particular period.

---

## 1. AI Architecture & Core Pipeline

```
Senior Text / Voice
       │
       ▼
┌──────────────────────────────┐
│ Speech-to-Text (if audio)    │ (speech_service.py)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Language Detection           │ (language_service.py)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Text Normalization           │ (normalization.py)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Request Understanding & LLM  │ (request_analyzer.py / fallback_analyzer.py)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Deterministic Risk Scoring   │ (urgency_classifier.py: 0–100 Bounded Score)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Structured JSON Output       │ (schemas.py)
└──────────────┬───────────────┘
               │
               ▼
FastAPI Backend Coordination (Member 2)
```

---

## 2. Supported Inputs & Languages

### Input Modes
- **TEXT**: Raw strings sent by senior citizens or front-end voice wrappers.
- **AUDIO**: Audio file uploads (`multipart/form-data`) supporting speech-to-text.

### Supported Languages
- **English** (`en`)
- **Telugu** (`te`) — Native script and Romanized transliteration (e.g., *"Nenu bathroom lo padipoyanu, levalekapothunnanu."*)
- **Hindi** (`hi`) — Native script and Romanized transliteration
- **Tamil** (`ta`)
- **Kannada** (`kn`)
- **Malayalam** (`ml`)
- *Extensible design for additional Indian regional languages.*

---

## 3. Request Categories & Urgency Levels

### Request Types (`request_type`)
- `FALL`: Senior has fallen or is unable to stand up after a drop.
- `MEDICAL_HELP`: Acute physical distress or medical support request.
- `MEDICATION`: Reminders or requests for medicine/tablets.
- `COMPANIONSHIP`: Loneliness, isolation, or request for someone to talk to.
- `LOCATION_DEVIATION`: Specified movement or location context outside home/routine.
- `GENERAL_HELP`: Assistance with daily activities (groceries, walking support, etc.).
- `EMERGENCY`: Explicit critical indicators (chest pain, breathing difficulty, unconsciousness).
- `OTHER`: Unspecified general check-ins.

### Urgency Levels (`urgency`)
- `CRITICAL`: Immediate response required (e.g., fall + unable to stand, severe chest pain).
- `HIGH`: Priority response required (e.g., dizzy, weak, unhandled minor fall).
- `MEDIUM`: Moderate priority (e.g., grocery help, routine check-in).
- `LOW`: Low priority (e.g., companionship, loneliness).

---

## 4. Bounded Risk Scoring Engine

The AI calculates a transparent **coordination priority risk score (0–100)**:
- **Fall + unable to stand**: ~94
- **Severe symptoms (chest pain / difficulty breathing)**: 95+
- **Medication reminder**: ~25
- **Companionship**: ~10–15

*Note: Target response windows (e.g., CRITICAL → 2 mins, HIGH → 5 mins) are owned by the Backend, NOT stated as guarantees by the AI.*

---

## 5. JSON Output Schema

Every analysis returns the following structured schema:

```json
{
  "language": "Telugu",
  "language_code": "te",
  "transcript": "Nenu bathroom lo padipoyanu, levalekapothunnanu.",
  "normalized_text": "I fell in the bathroom and cannot stand up.",
  "request_type": "FALL",
  "urgency": "CRITICAL",
  "risk_score": 94,
  "emergency": true,
  "potential_emergency": true,
  "fall_detected": true,
  "mobility_issue": true,
  "medical_attention_possible": true,
  "companionship": false,
  "location_relevant": true,
  "location_context": "bathroom",
  "required_support": [
    "immediate_assistance",
    "medical_attention"
  ],
  "entities": {
    "symptoms": [],
    "medication": null,
    "location": "bathroom",
    "time_reference": null,
    "body_area_if_explicit": null
  },
  "explanation": "The senior reports a fall in the bathroom and inability to stand, indicating a high-priority care coordination request.",
  "confidence": 0.94
}
```

---

## 6. API Endpoints

### 1. `POST /ai/analyze-text`
**Request Body:**
```json
{
  "text": "Nenu bathroom lo padipoyanu, levalekapothunnanu."
}
```
**Response:**
```json
{
  "success": true,
  "data": { ... }
}
```

### 2. `POST /ai/analyze-audio`
**Request Format:** `multipart/form-data` with `file` upload.

### 3. `GET /ai/health`
**Response:**
```json
{
  "status": "healthy",
  "ai_provider": "configured",
  "fallback_available": true
}
```

---

## 7. Environment Variables (`.env`)

```env
AI_PROVIDER=gemini       # gemini | openai | mock
AI_API_KEY=your_key_here
AI_MODEL=gemini-1.5-flash
AI_TIMEOUT_SECONDS=20
ENABLE_AI_FALLBACK=true

SPEECH_PROVIDER=mock     # mock | whisper_api | openai
SPEECH_API_KEY=
```

---

## 8. Deterministic Rule-Based Fallback System (`fallback_analyzer.py`)

For hackathon reliability, if:
- `AI_API_KEY` is missing
- Network connection fails
- LLM API times out or returns malformed JSON

The service automatically executes `fallback_analyzer.py`. It uses pattern matching across English, Telugu, Hindi, Tamil, Kannada, and Malayalam to generate **100% compliant JSON responses** with identical fields.

---

## 9. Integration Instructions for Member 2 (FastAPI Backend)

Member 2 can integrate with the AI layer in **two ways**:

### Option A: Direct Python Functions (Single FastAPI Process)
Import functions directly from `app.main`:

```python
from app.main import analyze_text_request, analyze_audio_request

# Text analysis
analysis = await analyze_text_request("Nenu bathroom lo padipoyanu...")
print(analysis.request_type)  # FALL
print(analysis.urgency)       # CRITICAL
print(analysis.risk_score)     # 94

# Audio analysis
analysis_audio = await analyze_audio_request(audio_bytes, filename="voice.wav")
```

### Option B: HTTP REST Service (Decoupled Microservice)
Call the running AI REST service:

```python
import httpx

async with httpx.AsyncClient() as client:
    res = await client.post("http://localhost:8000/ai/analyze-text", json={
        "text": "Nenu bathroom lo padipoyanu, levalekapothunnanu."
    })
    data = res.json()["data"]
    urgency = data["urgency"]  # "CRITICAL"
```

---

## 10. Installation & Run Commands

### Installation Command
```bash
pip install -r requirements.txt
```

### Run Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Test Command
```bash
pytest tests/
```
