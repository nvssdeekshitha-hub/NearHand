import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.database import engine, Base, SessionLocal
from app.db.seed import seed_data
from app.schemas.common import error_response

# Routers
from app.api.auth import router as auth_router
from app.api.seniors import router as seniors_router
from app.api.requests import router as requests_router
from app.api.caretakers import router as caretakers_router
from app.api.volunteers import router as volunteers_router
from app.api.family import router as family_router
from app.api.emergency import router as emergency_router
from app.api.location import router as location_router
from app.api.companionship import router as companionship_router
from app.api.notifications import router as notifications_router
from app.api.medications import router as medications_router
from app.api.websocket import router as websocket_router
from app.api.demo import router as demo_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    from app.api.websocket import set_main_loop
    set_main_loop(asyncio.get_running_loop())

    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Auto-seed if database is empty
    db = SessionLocal()
    try:
        from app.db.models import User
        if db.query(User).count() == 0:
            logger.info("Database is empty. Running initial seed...")
            seed_data(db)
    except Exception as e:
        logger.error(f"Auto-seed check error: {e}")
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend REST API & WebSockets for NearHand Senior Coordination & Emergency Escalation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open CORS for hackathon dev & frontend integration
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler to format errors uniformly
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response("SERVER_ERROR", str(exc))
    )

# Register API Routers
app.include_router(auth_router)
app.include_router(seniors_router)
app.include_router(requests_router)
app.include_router(caretakers_router)
app.include_router(volunteers_router)
app.include_router(family_router)
app.include_router(emergency_router)
app.include_router(location_router)
app.include_router(companionship_router)
app.include_router(notifications_router)
app.include_router(medications_router)
app.include_router(websocket_router)
app.include_router(demo_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "success": True,
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
