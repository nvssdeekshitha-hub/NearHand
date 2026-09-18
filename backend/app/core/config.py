import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NearHand Backend API"
    API_V1_STR: str = ""
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nearhand.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_nearhand_hackathon_key_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Response windows (in minutes)
    TARGET_RESPONSE_CRITICAL: int = int(os.getenv("TARGET_RESPONSE_CRITICAL", "2"))
    TARGET_RESPONSE_HIGH: int = int(os.getenv("TARGET_RESPONSE_HIGH", "5"))
    TARGET_RESPONSE_MEDIUM: int = int(os.getenv("TARGET_RESPONSE_MEDIUM", "10"))
    TARGET_RESPONSE_LOW: int = int(os.getenv("TARGET_RESPONSE_LOW", "20"))
    
    # Volunteer matching constants
    VOLUNTEER_SEARCH_RADIUS_KM: float = float(os.getenv("VOLUNTEER_SEARCH_RADIUS_KM", "5.0"))
    WEIGHT_URGENCY: float = 0.40
    WEIGHT_ETA: float = 0.25
    WEIGHT_DISTANCE: float = 0.15
    WEIGHT_AVAILABILITY: float = 0.10
    WEIGHT_SKILL: float = 0.10

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
