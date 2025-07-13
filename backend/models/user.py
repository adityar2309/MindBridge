"""
User model for MindBridge application.

This module defines the User model with profile information,
authentication details, and user preferences.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """
    User model for storing user profile and authentication data.
    
    Attributes:
        user_id: Primary key identifier
        name: User's full name
        email: User's email address (unique)
        password_hash: Hashed password for authentication
        registration_date: Timestamp of user registration
        is_active: Whether the user account is active
        settings: JSON field for user preferences and settings
        last_login: Timestamp of last login
        timezone: User's timezone preference
        language: User's language preference
    """
    
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    registration_date = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    settings = Column(JSON, default=lambda: {
        "notifications": {
            "daily_reminder": True,
            "weekly_summary": True,
            "mood_alerts": True,
            "reminder_time": "09:00"
        },
        "privacy": {
            "data_sharing": False,
            "anonymous_analytics": True
        },
        "ui": {
            "theme": "auto",
            "font_size": "medium",
            "animations": True
        }
    })
    last_login = Column(DateTime, nullable=True)
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    
    # Relationships
    daily_checkins = relationship("DailyCheckin", back_populates="user")
    passive_data = relationship("PassiveDataPoint", back_populates="user")
    quiz_sessions = relationship("QuizSession", back_populates="user")
    ai_insights = relationship("AIMoodInsight", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, email='{self.email}')>"
    
    def to_dict(self) -> dict:
        """Convert user instance to dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "registration_date": self.registration_date.isoformat(),
            "is_active": self.is_active,
            "settings": self.settings,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "timezone": self.timezone,
            "language": self.language
        } 
