"""
User Pydantic schemas
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str
    preferences: Optional[Dict[str, Any]] = {}


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates"""
    name: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class UserInDBBase(UserBase):
    """Base schema for user in database"""
    id: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """User schema for responses"""
    pass


class UserInDB(UserInDBBase):
    """User schema for database operations"""
    hashed_password: str


class Token(BaseModel):
    """JWT token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT token data"""
    sub: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class RegisterRequest(UserCreate):
    """Registration request schema"""
    pass
