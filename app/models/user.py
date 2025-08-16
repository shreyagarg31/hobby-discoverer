from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class SocialPref(str, Enum):
    SOLO = "solo"
    GROUP = "group"
    EITHER = "either"

class UserProfile(BaseModel):
    time_available: int  = Field(..., description="Hours per week available for hobbies")
    prefers_indoor: bool = Field(..., description="Indoor vs outdoor preference")
    social_preference: SocialPref
    interests: List[str]
    location: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    profile: UserProfile

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserBase(BaseModel):
    email: EmailStr
    name: str
    profile: UserProfile
    created_at: datetime = Field(default_factory=datetime.utcnow)
class User(BaseModel):
    id: str
    class Config:
        orm_mode = True
class DBUser(UserBase):
    hashed_password: str
    id: Optional[str] = None