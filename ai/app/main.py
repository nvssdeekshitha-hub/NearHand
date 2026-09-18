import asyncio
from typing import Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import (
    AnalyzeTextRequest,
    ApiResponse,
    HealthCheckResponse,
    AnalysisResultData
)
from app.services.request_analyzer import analyze_request
from app.services.speech_service import transcribe_audio

app = FastAPI(
    title="NEARHAND AI Integration Service",
    description="AI analysis layer for senior assistance & care coordination",
    version="1.0.0"
)

# CORS middleware for local frontend / backend cross-origin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- PYTHON INTEGRATION INTERFACE FOR BACKEND MEMBER 2 ---
async def analyze_text_request(text: str) -> AnalysisResultData:
    """
    Direct Python async function for backend integration.
    Usage: result = await analyze_text_request("Nenu bathroom lo padipoyanu...")
    """
    return await analyze_request(text)


async def analyze_audio_request(audio_bytes: bytes, filename: str = "audio.wav") -> AnalysisResultData:
    """
    Direct Python async function for audio processing backend integration.
    Usage: result = await analyze_audio_request(audio_bytes, filename)
    """
    speech_res = await transcribe_audio(audio_bytes, filename)
    transcript = speech_res["transcript"]
    return await analyze_request(transcript, transcript=transcript)


# Synchronous wrapper functions for synchronous backend calls
def analyze_text_request_sync(text: str) -> AnalysisResultData:
    """Synchronous wrapper for backend integration if needed."""
    return asyncio.run(analyze_text_request(text))


def analyze_audio_request_sync(audio_bytes: bytes, filename: str = "audio.wav") -> AnalysisResultData:
    """Synchronous wrapper for audio backend integration if needed."""
    return asyncio.run(analyze_audio_request(audio_bytes, filename))


# --- FASTAPI REST API ENDPOINTS ---

@app.get("/ai/health", response_model=HealthCheckResponse)
async def health_check():
    """
    AI Health check endpoint. Does not expose secrets or API keys.
    """
    ai_status = "configured" if settings.AI_API_KEY else "fallback_only"
    return HealthCheckResponse(
        status="healthy",
        ai_provider=ai_status,
        fallback_available=settings.ENABLE_AI_FALLBACK
    )


@app.post("/ai/analyze-text", response_model=ApiResponse)
async def analyze_text_endpoint(payload: AnalyzeTextRequest):
    """
    Analyze text input from a senior citizen.
    """
    try:
        result = await analyze_text_request(payload.text)
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing request: {str(e)}"
        )


@app.post("/ai/analyze-audio", response_model=ApiResponse)
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    """
    Analyze audio input (multipart form-data) from a senior citizen.
    Pipeline: Audio -> Speech-to-text -> Language -> Analysis -> Structured JSON
    """
    try:
        contents = await file.read()
        result = await analyze_audio_request(contents, filename=file.filename or "audio.wav")
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing audio request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
