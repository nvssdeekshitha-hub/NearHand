from typing import Any, Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[dict] = None

def success_response(data: Any = None, message: str = "Success") -> dict:
    return {
        "success": True,
        "data": data,
        "message": message
    }

def error_response(code: str, message: str) -> dict:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
