import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from ai directory if present
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    # LLM Settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini").lower()
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-1.5-flash")
    AI_TIMEOUT_SECONDS: int = int(os.getenv("AI_TIMEOUT_SECONDS", "20"))
    ENABLE_AI_FALLBACK: bool = os.getenv("ENABLE_AI_FALLBACK", "true").lower() == "true"

    # Speech-to-Text Settings
    SPEECH_PROVIDER: str = os.getenv("SPEECH_PROVIDER", "mock").lower()
    SPEECH_API_KEY: str = os.getenv("SPEECH_API_KEY", "")

    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
