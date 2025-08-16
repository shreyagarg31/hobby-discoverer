from fastapi import APIRouter, HTTPException, status, Request
from app.models.user import UserCreate, UserLogin, User, UserProfile
from app.services.user_service import (
    create_user_in_db,
    get_user_by_email,
    verify_user_credentials,
    get_user_by_id,
    update_user_profile_in_db,
)
from datetime import datetime

router = APIRouter(prefix="/api/v1")

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Idempotency: Check if user already exists
    print("Received user signup request for :", user.name)
    existing = await get_user_by_email(user.email)
    if existing:
        print("User already exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    created_user = await create_user_in_db(user)
    return created_user

@router.post("/users/login")
async def login(user: UserLogin):
    print("Received user login request for:", user.email)
    db_user = await verify_user_credentials(user.email, user.password)
    if not db_user:
        print("Login failed.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {
        "message": "Login successful",
        "user_id": str(db_user.id),
        "email": db_user.email,
        "name": db_user.name
    }

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    db_user = await get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Convert DBUser to User for response
    return User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        profile=db_user.profile,
        created_at=db_user.created_at
    )

@router.post("/users/{user_id}/profile", response_model=UserProfile)
async def create_user_profile(user_id: str, profile: UserProfile):
    updated_profile = await update_user_profile_in_db(user_id, profile)
    if not updated_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_profile