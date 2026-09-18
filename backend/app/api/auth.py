from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User, Senior, Caretaker, Volunteer, Family, UserRole
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(request_in: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email exists
    existing = db.query(User).filter(User.email == request_in.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=error_response("USER_EXISTS", "User with this email already exists.")
        )

    # Create User
    hashed_pwd = get_password_hash(request_in.password)
    role_str = request_in.role.upper()
    user = User(
        name=request_in.name,
        email=request_in.email,
        phone=request_in.phone,
        password_hash=hashed_pwd,
        role=role_str
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create role specific profile
    if role_str == UserRole.SENIOR.value:
        senior = Senior(
            user_id=user.id,
            age=request_in.age or 70,
            gender=request_in.gender or "Female",
            preferred_language=request_in.preferred_language or "English",
            address=request_in.address or "Hyderabad, India",
            latitude=request_in.latitude or 17.385044,
            longitude=request_in.longitude or 78.486671,
            home_latitude=request_in.latitude or 17.385044,
            home_longitude=request_in.longitude or 78.486671,
            emergency_contact=request_in.emergency_contact or "Family"
        )
        db.add(senior)
    elif role_str == UserRole.CARETAKER.value:
        caretaker = Caretaker(
            user_id=user.id,
            latitude=request_in.latitude or 17.385044,
            longitude=request_in.longitude or 78.486671
        )
        db.add(caretaker)
    elif role_str == UserRole.VOLUNTEER.value:
        volunteer = Volunteer(
            user_id=user.id,
            latitude=request_in.latitude or 17.385044,
            longitude=request_in.longitude or 78.486671,
            first_aid_trained=True,
            skills="[\"First Aid\"]"
        )
        db.add(volunteer)
    db.commit()

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return success_response(
        data={
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            },
            "access_token": token,
            "token_type": "bearer"
        },
        message="User registered successfully"
    )

@router.post("/login")
def login(request_in: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request_in.email).first()
    if not user or not verify_password(request_in.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail=error_response("INVALID_CREDENTIALS", "Invalid email or password.")
        )

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    
    profile_info = {}
    if user.role == UserRole.SENIOR.value and user.senior_profile:
        profile_info = {"senior_id": user.senior_profile.id}
    elif user.role == UserRole.CARETAKER.value and user.caretaker_profile:
        profile_info = {"caretaker_id": user.caretaker_profile.id}
    elif user.role == UserRole.VOLUNTEER.value and user.volunteer_profile:
        profile_info = {"volunteer_id": user.volunteer_profile.id}
    elif user.role == UserRole.FAMILY.value and user.family_profile:
        profile_info = {"family_id": user.family_profile.id, "senior_id": user.family_profile.senior_id}

    return success_response(
        data={
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                **profile_info
            },
            "access_token": token,
            "token_type": "bearer"
        },
        message="Login successful"
    )

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile_info = {}
    if current_user.role == UserRole.SENIOR.value and current_user.senior_profile:
        profile_info = {"senior_id": current_user.senior_profile.id}
    elif current_user.role == UserRole.CARETAKER.value and current_user.caretaker_profile:
        profile_info = {"caretaker_id": current_user.caretaker_profile.id}
    elif current_user.role == UserRole.VOLUNTEER.value and current_user.volunteer_profile:
        profile_info = {"volunteer_id": current_user.volunteer_profile.id}
    elif current_user.role == UserRole.FAMILY.value and current_user.family_profile:
        profile_info = {"family_id": current_user.family_profile.id, "senior_id": current_user.family_profile.senior_id}

    return success_response(
        data={
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "phone": current_user.phone,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            **profile_info
        },
        message="User profile fetched successfully"
    )
