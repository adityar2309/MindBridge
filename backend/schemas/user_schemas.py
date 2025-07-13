"""
User schemas for MindBridge application.

This module defines Pydantic schemas for user-related API
validation, serialization, and request/response handling.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class UserSettings(BaseModel):
    """Schema for user settings."""
    
    notifications: Dict[str, Any] = Field(default={
        "daily_reminder": True,
        "weekly_summary": True,
        "mood_alerts": True,
        "reminder_time": "09:00"
    })
    privacy: Dict[str, Any] = Field(default={
        "data_sharing": False,
        "anonymous_analytics": True
    })
    ui: Dict[str, Any] = Field(default={
        "theme": "auto",
        "font_size": "medium",
        "animations": True
    })


class UserCreate(BaseModel):
    """Schema for user creation."""
    
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    timezone: str = Field(default="UTC", max_length=50)
    language: str = Field(default="en", max_length=10)
    settings: Optional[UserSettings] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    timezone: Optional[str] = Field(None, max_length=50)
    language: Optional[str] = Field(None, max_length=10)
    settings: Optional[UserSettings] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    
    user_id: int
    name: str
    email: str
    registration_date: datetime
    is_active: bool
    settings: Dict[str, Any]
    last_login: Optional[datetime]
    timezone: str
    language: str
    
    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    """Schema for user profile (public information)."""
    
    user_id: int
    name: str
    registration_date: datetime
    timezone: str
    language: str
    
    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    """Schema for password change."""
    
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request."""
    
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for reset password request."""
    
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    
    status: str
    timestamp: datetime
    version: str
    environment: str
    details: Optional[Dict[str, Any]] = None 