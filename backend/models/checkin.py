"""
Daily check-in model for MindBridge application.

This module defines the DailyCheckin model for storing user's
daily mood check-ins, including ratings, tags, and notes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class DailyCheckin(Base):
    """
    Daily check-in model for storing user's daily mood data.
    
    Attributes:
        checkin_id: Primary key identifier
        user_id: Foreign key to User model
        timestamp: When the check-in was recorded
        mood_rating: Numerical mood rating (1-10 scale)
        mood_category: Categorical mood description
        keywords: List of user-selected mood keywords/tags
        notes: Free-text notes from the user
        location: Optional location context
        weather: Optional weather context
        energy_level: Energy level rating (1-10)
        stress_level: Stress level rating (1-10)
        sleep_quality: Sleep quality rating (1-10)
        social_interaction: Social interaction level (1-10)
    """
    
    __tablename__ = "daily_checkins"
    
    checkin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    mood_rating = Column(Float, nullable=False)  # 1-10 scale
    mood_category = Column(String(50), nullable=True)  # e.g., "happy", "anxious", "calm"
    keywords = Column(JSON, default=list)  # List of mood keywords/tags
    notes = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    weather = Column(String(50), nullable=True)
    energy_level = Column(Float, nullable=True)  # 1-10 scale
    stress_level = Column(Float, nullable=True)  # 1-10 scale
    sleep_quality = Column(Float, nullable=True)  # Previous night's sleep quality
    social_interaction = Column(Float, nullable=True)  # Social interaction level
    
    # Relationships
    user = relationship("User", back_populates="daily_checkins")
    
    def __repr__(self) -> str:
        return f"<DailyCheckin(checkin_id={self.checkin_id}, user_id={self.user_id}, mood_rating={self.mood_rating})>"
    
    def to_dict(self) -> dict:
        """Convert check-in instance to dictionary."""
        return {
            "checkin_id": self.checkin_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "mood_rating": self.mood_rating,
            "mood_category": self.mood_category,
            "keywords": self.keywords,
            "notes": self.notes,
            "location": self.location,
            "weather": self.weather,
            "energy_level": self.energy_level,
            "stress_level": self.stress_level,
            "sleep_quality": self.sleep_quality,
            "social_interaction": self.social_interaction
        }
    
    @classmethod
    def get_mood_categories(cls) -> list:
        """Get available mood categories."""
        return [
            "happy", "content", "calm", "excited", "optimistic",
            "sad", "anxious", "stressed", "angry", "frustrated",
            "tired", "energetic", "focused", "confused", "lonely",
            "grateful", "hopeful", "overwhelmed", "peaceful", "neutral"
        ]
    
    @classmethod
    def get_common_keywords(cls) -> list:
        """Get common mood keywords/tags."""
        return [
            "work", "family", "friends", "exercise", "sleep", "health",
            "weather", "social", "alone", "productive", "creative",
            "relaxed", "motivated", "challenged", "supported", "loved"
        ] 