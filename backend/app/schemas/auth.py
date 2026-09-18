from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    role: str = "SENIOR"
    
    # Senior specific fields if role == SENIOR
    age: Optional[int] = 72
    gender: Optional[str] = "Female"
    preferred_language: Optional[str] = "Telugu"
    address: Optional[str] = "Hyderabad, India"
    latitude: Optional[float] = 17.385044
    longitude: Optional[float] = 78.486671
    emergency_contact: Optional[str] = "Anjali"

class TokenData(BaseModel):
    user_id: int
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
