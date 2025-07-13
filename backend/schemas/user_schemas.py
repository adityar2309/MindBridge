"""
User schemas for MindBridge application.

This module defines Pydantic schemas for user-related API
validation, serialization, and request/response handling.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
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
    
    # Support both 'name' and 'first_name'/'last_name' patterns
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    timezone: Optional[str] = Field(default="UTC", max_length=50)
    language: Optional[str] = Field(default="en", max_length=10)
    settings: Optional[UserSettings] = None
    
    # Optional fields that might come from frontend
    date_of_birth: Optional[datetime] = None
    
    @model_validator(mode='before')
    @classmethod
    def validate_name_fields(cls, values):
        """Ensure either 'name' or both 'first_name' and 'last_name' are provided."""
        # Handle both dict and model instances
        if isinstance(values, dict):
            data = values
        else:
            data = values.__dict__ if hasattr(values, '__dict__') else values
            
        name = data.get('name')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        if not name and not (first_name and last_name):
            raise ValueError('Either "name" or both "first_name" and "last_name" must be provided')
        
        # If first_name and last_name provided but no name, combine them
        if not name and first_name and last_name:
            data['name'] = f"{first_name} {last_name}"
        
        # Ensure timezone is a string, not None
        if data.get('timezone') is None:
            data['timezone'] = "UTC"
            
        # Ensure language is a string, not None
        if data.get('language') is None:
            data['language'] = "en"
        
        return data
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Temporarily more lenient - can add stricter validation later
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
        from_attributes = True


class UserProfile(BaseModel):
    """Schema for user profile (public information)."""
    
    user_id: int
    name: str
    registration_date: datetime
    timezone: str
    language: str
    
    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for password change."""
    
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    
    @model_validator(mode='after')
    @classmethod
    def passwords_match(cls, values):
        """Validate that passwords match."""
        if hasattr(values, 'new_password') and hasattr(values, 'confirm_password'):
            if values.new_password != values.confirm_password:
                raise ValueError('Passwords do not match')
        return values
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Temporarily more lenient - can add stricter validation later
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
    
    @model_validator(mode='after')
    @classmethod
    def passwords_match(cls, values):
        """Validate that passwords match."""
        if hasattr(values, 'new_password') and hasattr(values, 'confirm_password'):
            if values.new_password != values.confirm_password:
                raise ValueError('Passwords do not match')
        return values


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    
    status: str
    timestamp: datetime
    version: str
    environment: str
    details: Optional[Dict[str, Any]] = None 
