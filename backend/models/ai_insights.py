"""
AI Mood Insight models for MindBridge application.

This module defines the AIMoodInsight model for storing
AI-generated mood predictions, insights, and recommendations.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum


class InsightType(str, Enum):
    """Enumeration of insight types."""
    
    MOOD_PREDICTION = "mood_prediction"
    RISK_ASSESSMENT = "risk_assessment"
    PATTERN_ANALYSIS = "pattern_analysis"
    RECOMMENDATION = "recommendation"
    EARLY_WARNING = "early_warning"
    PROGRESS_TRACKING = "progress_tracking"
    INTERVENTION_SUGGESTION = "intervention_suggestion"


class RecommendationType(str, Enum):
    """Enumeration of recommendation types."""
    
    ACTIVITY = "activity"
    MINDFULNESS = "mindfulness"
    SOCIAL = "social"
    PROFESSIONAL_HELP = "professional_help"
    LIFESTYLE = "lifestyle"
    SLEEP = "sleep"
    EXERCISE = "exercise"
    NUTRITION = "nutrition"
    STRESS_MANAGEMENT = "stress_management"


class AIMoodInsight(Base):
    """
    AI mood insight model for storing ML-generated insights.
    
    Attributes:
        insight_id: Primary key identifier
        user_id: Foreign key to User model
        timestamp: When the insight was generated
        insight_type: Type of insight generated
        mood_score_prediction: Predicted mood score (1-10)
        confidence_score: Confidence in the prediction (0-1)
        contributing_factors: Factors that influenced the prediction
        recommendation: Suggested action or intervention
        recommendation_type: Type of recommendation
        priority_level: Priority level (low, medium, high, urgent)
        is_actionable: Whether the insight requires user action
        feedback_score: User feedback on the insight quality
        model_version: Version of the ML model used
        data_sources: Data sources used for the insight
    """
    
    __tablename__ = "ai_mood_insights"
    
    insight_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    insight_type = Column(String(50), nullable=False)
    mood_score_prediction = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=False)  # 0-1 scale
    contributing_factors = Column(JSON, default=list)
    recommendation = Column(Text, nullable=True)
    recommendation_type = Column(String(50), nullable=True)
    priority_level = Column(String(20), default="medium")  # low, medium, high, urgent
    is_actionable = Column(Boolean, default=True)
    feedback_score = Column(Float, nullable=True)  # User feedback 1-5
    model_version = Column(String(50), nullable=True)
    data_sources = Column(JSON, default=list)
    
    # Relationships
    user = relationship("User", back_populates="ai_insights")
    
    def __repr__(self) -> str:
        return f"<AIMoodInsight(insight_id={self.insight_id}, user_id={self.user_id}, insight_type='{self.insight_type}')>"
    
    def to_dict(self) -> dict:
        """Convert AI mood insight to dictionary."""
        return {
            "insight_id": self.insight_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "insight_type": self.insight_type,
            "mood_score_prediction": self.mood_score_prediction,
            "confidence_score": self.confidence_score,
            "contributing_factors": self.contributing_factors,
            "recommendation": self.recommendation,
            "recommendation_type": self.recommendation_type,
            "priority_level": self.priority_level,
            "is_actionable": self.is_actionable,
            "feedback_score": self.feedback_score,
            "model_version": self.model_version,
            "data_sources": self.data_sources
        }
    
    @classmethod
    def get_priority_levels(cls) -> list:
        """Get available priority levels."""
        return ["low", "medium", "high", "urgent"]
    
    @classmethod
    def get_common_factors(cls) -> list:
        """Get common contributing factors."""
        return [
            "sleep_pattern", "exercise_frequency", "social_activity",
            "work_stress", "weather_conditions", "screen_time",
            "mood_history", "seasonal_patterns", "weekly_patterns",
            "health_metrics", "medication_adherence", "social_support"
        ]
    
    @classmethod
    def get_recommendation_templates(cls) -> dict:
        """Get recommendation templates by type."""
        return {
            "mindfulness": [
                "Consider practicing 10 minutes of mindfulness meditation",
                "Try the 4-7-8 breathing technique for stress relief",
                "Take a mindful walk in nature for 15 minutes"
            ],
            "social": [
                "Reach out to a friend or family member today",
                "Consider joining a social activity or group",
                "Schedule a coffee date with someone you trust"
            ],
            "activity": [
                "Engage in a favorite hobby for 30 minutes",
                "Try a new creative activity to boost mood",
                "Take a break and do something you enjoy"
            ],
            "exercise": [
                "Consider a 20-minute walk or light exercise",
                "Try some gentle stretching or yoga",
                "Engage in your favorite physical activity"
            ],
            "professional_help": [
                "Consider speaking with a mental health professional",
                "It might be helpful to consult with a therapist",
                "Professional support could be beneficial right now"
            ]
        }


class ConversationLog(Base):
    """
    Conversation log model for storing AI assistant interactions.
    
    Attributes:
        log_id: Primary key identifier
        user_id: Foreign key to User model
        session_id: Conversation session identifier
        timestamp: When the interaction occurred
        user_message: User's message/query
        ai_response: AI assistant's response
        context_data: Contextual information used for response
        response_quality: Quality rating of the response
        user_feedback: User feedback on the response
        model_version: Version of the conversation model used
    """
    
    __tablename__ = "conversation_logs"
    
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    session_id = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    context_data = Column(JSON, default=dict)
    response_quality = Column(Float, nullable=True)  # 1-5 scale
    user_feedback = Column(String(20), nullable=True)  # positive, negative, neutral
    model_version = Column(String(50), nullable=True)
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<ConversationLog(log_id={self.log_id}, user_id={self.user_id}, session_id='{self.session_id}')>"
    
    def to_dict(self) -> dict:
        """Convert conversation log to dictionary."""
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "user_message": self.user_message,
            "ai_response": self.ai_response,
            "context_data": self.context_data,
            "response_quality": self.response_quality,
            "user_feedback": self.user_feedback,
            "model_version": self.model_version
        } 
