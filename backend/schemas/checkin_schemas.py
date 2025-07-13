"""
Check-in schemas for MindBridge application.

This module defines Pydantic schemas for daily check-in
validation, serialization, and request/response handling.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class DailyCheckinCreate(BaseModel):
    """Schema for creating a daily check-in."""
    
    mood_rating: float = Field(..., ge=1.0, le=10.0, description="Mood rating from 1-10")
    mood_category: Optional[str] = Field(None, max_length=50)
    keywords: Optional[List[str]] = Field(default_factory=list, max_items=20)
    notes: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=100)
    weather: Optional[str] = Field(None, max_length=50)
    energy_level: Optional[float] = Field(None, ge=1.0, le=10.0)
    stress_level: Optional[float] = Field(None, ge=1.0, le=10.0)
    sleep_quality: Optional[float] = Field(None, ge=1.0, le=10.0)
    social_interaction: Optional[float] = Field(None, ge=1.0, le=10.0)
    
    @validator('mood_category')
    def validate_mood_category(cls, v):
        """Validate mood category."""
        if v is None:
            return v
        
        valid_categories = [
            "happy", "content", "calm", "excited", "optimistic",
            "sad", "anxious", "stressed", "angry", "frustrated",
            "tired", "energetic", "focused", "confused", "lonely",
            "grateful", "hopeful", "overwhelmed", "peaceful", "neutral"
        ]
        
        if v not in valid_categories:
            raise ValueError(f"Invalid mood category. Must be one of: {valid_categories}")
        return v
    
    @validator('keywords')
    def validate_keywords(cls, v):
        """Validate keywords list."""
        if v is None:
            return []
        
        # Remove duplicates and empty strings
        cleaned = list(set(k.strip() for k in v if k.strip()))
        
        # Validate each keyword
        for keyword in cleaned:
            if len(keyword) > 50:
                raise ValueError("Keywords must be 50 characters or less")
        
        return cleaned[:20]  # Limit to 20 keywords


class DailyCheckinUpdate(BaseModel):
    """Schema for updating a daily check-in."""
    
    mood_rating: Optional[float] = Field(None, ge=1.0, le=10.0)
    mood_category: Optional[str] = Field(None, max_length=50)
    keywords: Optional[List[str]] = Field(None, max_items=20)
    notes: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=100)
    weather: Optional[str] = Field(None, max_length=50)
    energy_level: Optional[float] = Field(None, ge=1.0, le=10.0)
    stress_level: Optional[float] = Field(None, ge=1.0, le=10.0)
    sleep_quality: Optional[float] = Field(None, ge=1.0, le=10.0)
    social_interaction: Optional[float] = Field(None, ge=1.0, le=10.0)
    
    @validator('mood_category')
    def validate_mood_category(cls, v):
        """Validate mood category."""
        if v is None:
            return v
        
        valid_categories = [
            "happy", "content", "calm", "excited", "optimistic",
            "sad", "anxious", "stressed", "angry", "frustrated",
            "tired", "energetic", "focused", "confused", "lonely",
            "grateful", "hopeful", "overwhelmed", "peaceful", "neutral"
        ]
        
        if v not in valid_categories:
            raise ValueError(f"Invalid mood category. Must be one of: {valid_categories}")
        return v


class DailyCheckinResponse(BaseModel):
    """Schema for daily check-in response."""
    
    checkin_id: int
    user_id: int
    timestamp: datetime
    mood_rating: float
    mood_category: Optional[str]
    keywords: List[str]
    notes: Optional[str]
    location: Optional[str]
    weather: Optional[str]
    energy_level: Optional[float]
    stress_level: Optional[float]
    sleep_quality: Optional[float]
    social_interaction: Optional[float]
    
    class Config:
        orm_mode = True


class DailyCheckinSummary(BaseModel):
    """Schema for daily check-in summary."""
    
    checkin_id: int
    timestamp: datetime
    mood_rating: float
    mood_category: Optional[str]
    keywords: List[str]
    
    class Config:
        orm_mode = True


class MoodTrend(BaseModel):
    """Schema for mood trend analysis."""
    
    date: str
    mood_rating: float
    energy_level: Optional[float]
    stress_level: Optional[float]
    sleep_quality: Optional[float]


class MoodAnalytics(BaseModel):
    """Schema for mood analytics."""
    
    period: str  # daily, weekly, monthly
    average_mood: float
    mood_range: Dict[str, float]  # min, max
    most_common_category: Optional[str]
    trend_direction: str  # improving, declining, stable
    trend_data: List[MoodTrend]
    keyword_frequency: Dict[str, int]
    correlation_insights: Dict[str, Any]


class CheckinStreak(BaseModel):
    """Schema for check-in streak information."""
    
    current_streak: int
    longest_streak: int
    total_checkins: int
    streak_start_date: Optional[datetime]
    days_since_last_checkin: int


class QuickMoodEntry(BaseModel):
    """Schema for quick mood entry (simplified check-in)."""
    
    mood_rating: float = Field(..., ge=1.0, le=10.0)
    mood_category: Optional[str] = None
    keywords: Optional[List[str]] = Field(default_factory=list, max_items=5)
    
    @validator('mood_category')
    def validate_mood_category(cls, v):
        """Validate mood category."""
        if v is None:
            return v
        
        valid_categories = [
            "happy", "content", "calm", "excited", "optimistic",
            "sad", "anxious", "stressed", "angry", "frustrated",
            "tired", "energetic", "focused", "confused", "lonely",
            "grateful", "hopeful", "overwhelmed", "peaceful", "neutral"
        ]
        
        if v not in valid_categories:
            raise ValueError(f"Invalid mood category. Must be one of: {valid_categories}")
        return v


class MoodCategories(BaseModel):
    """Schema for available mood categories."""
    
    categories: List[str]
    keywords: List[str]


class CheckinReminder(BaseModel):
    """Schema for check-in reminder settings."""
    
    enabled: bool
    time: str  # HH:MM format
    days_of_week: List[int]  # 0-6 (Monday-Sunday)
    message: Optional[str] = None 