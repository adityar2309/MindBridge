"""
AI schemas for MindBridge application.

This module defines Pydantic schemas for AI insights,
conversational assistant, and ML-related API validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class InsightTypeEnum(str, Enum):
    """Enumeration of insight types."""
    
    MOOD_PREDICTION = "mood_prediction"
    RISK_ASSESSMENT = "risk_assessment"
    PATTERN_ANALYSIS = "pattern_analysis"
    RECOMMENDATION = "recommendation"
    EARLY_WARNING = "early_warning"
    PROGRESS_TRACKING = "progress_tracking"
    INTERVENTION_SUGGESTION = "intervention_suggestion"


class RecommendationTypeEnum(str, Enum):
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


class PriorityLevel(str, Enum):
    """Enumeration of priority levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class AIMoodInsightCreate(BaseModel):
    """Schema for creating an AI mood insight."""
    
    insight_type: InsightTypeEnum
    mood_score_prediction: Optional[float] = Field(None, ge=1.0, le=10.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    contributing_factors: List[str] = Field(default_factory=list)
    recommendation: Optional[str] = Field(None, max_length=1000)
    recommendation_type: Optional[RecommendationTypeEnum] = None
    priority_level: Optional[PriorityLevel] = Field(default=PriorityLevel.MEDIUM)
    is_actionable: Optional[bool] = Field(default=True)
    model_version: Optional[str] = Field(None, max_length=50)
    data_sources: Optional[List[str]] = Field(default_factory=list)
    
    @validator('contributing_factors')
    def validate_contributing_factors(cls, v):
        """Validate contributing factors list."""
        if len(v) > 10:
            raise ValueError("Maximum 10 contributing factors allowed")
        return v


class AIMoodInsightUpdate(BaseModel):
    """Schema for updating an AI mood insight."""
    
    recommendation: Optional[str] = Field(None, max_length=1000)
    priority_level: Optional[PriorityLevel] = None
    is_actionable: Optional[bool] = None
    feedback_score: Optional[float] = Field(None, ge=1.0, le=5.0)


class AIMoodInsightResponse(BaseModel):
    """Schema for AI mood insight response."""
    
    insight_id: int
    user_id: int
    timestamp: datetime
    insight_type: str
    mood_score_prediction: Optional[float]
    confidence_score: float
    contributing_factors: List[str]
    recommendation: Optional[str]
    recommendation_type: Optional[str]
    priority_level: str
    is_actionable: bool
    feedback_score: Optional[float]
    model_version: Optional[str]
    data_sources: List[str]
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    """Schema for creating a conversation log."""
    
    session_id: str = Field(..., max_length=255)
    user_message: str = Field(..., max_length=2000)
    ai_response: str = Field(..., max_length=5000)
    context_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    model_version: Optional[str] = Field(None, max_length=50)


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation log."""
    
    response_quality: Optional[float] = Field(None, ge=1.0, le=5.0)
    user_feedback: Optional[str] = Field(None, pattern="^(positive|negative|neutral)$")


class ConversationResponse(BaseModel):
    """Schema for conversation log response."""
    
    log_id: int
    user_id: int
    session_id: str
    timestamp: datetime
    user_message: str
    ai_response: str
    context_data: Dict[str, Any]
    response_quality: Optional[float]
    user_feedback: Optional[str]
    model_version: Optional[str]
    
    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    """Schema for chat message."""
    
    message: str = Field(..., max_length=2000)
    session_id: Optional[str] = Field(None, max_length=255)
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    response: str
    session_id: str
    confidence_score: Optional[float] = None
    suggestions: Optional[List[str]] = None
    mood_detected: Optional[str] = None
    escalation_needed: Optional[bool] = None


class MoodPredictionRequest(BaseModel):
    """Schema for mood prediction request."""
    
    checkin_data: Optional[Dict[str, Any]] = None
    passive_data: Optional[Dict[str, Any]] = None
    historical_data: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None


class MoodPredictionResponse(BaseModel):
    """Schema for mood prediction response."""
    
    predicted_mood: float = Field(..., ge=1.0, le=10.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    contributing_factors: List[str]
    recommendations: List[str]
    risk_level: str  # low, medium, high
    model_version: str


class PatternAnalysisRequest(BaseModel):
    """Schema for pattern analysis request."""
    
    analysis_type: str  # mood_trends, behavioral_patterns, correlation_analysis
    time_period: str  # daily, weekly, monthly, yearly
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    data_types: Optional[List[str]] = None


class PatternAnalysisResponse(BaseModel):
    """Schema for pattern analysis response."""
    
    analysis_type: str
    patterns_found: List[Dict[str, Any]]
    insights: List[str]
    confidence_scores: Dict[str, float]
    visualizations: Optional[Dict[str, Any]] = None
    recommendations: List[str]


class RecommendationRequest(BaseModel):
    """Schema for recommendation request."""
    
    current_mood: Optional[float] = Field(None, ge=1.0, le=10.0)
    context: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    recommendation_types: Optional[List[RecommendationTypeEnum]] = None


class RecommendationResponse(BaseModel):
    """Schema for recommendation response."""
    
    recommendations: List[Dict[str, Any]]
    priority_order: List[int]
    personalization_score: float
    reasoning: List[str]


class ModelPerformanceMetrics(BaseModel):
    """Schema for model performance metrics."""
    
    model_name: str
    version: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    last_updated: datetime
    training_data_size: int
    validation_metrics: Dict[str, float]


class FeedbackSubmission(BaseModel):
    """Schema for feedback submission."""
    
    feedback_type: str  # insight_feedback, recommendation_feedback, chat_feedback
    target_id: int  # ID of the insight, recommendation, or conversation
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=500)
    categories: Optional[List[str]] = None


class UserFeedbackAnalysis(BaseModel):
    """Schema for user feedback analysis."""
    
    feedback_type: str
    average_rating: float
    total_feedback: int
    rating_distribution: Dict[str, int]
    common_themes: List[str]
    improvement_areas: List[str]


class AISystemStatus(BaseModel):
    """Schema for AI system status."""
    
    models_active: Dict[str, bool]
    last_model_update: Dict[str, datetime]
    processing_queue_size: int
    average_response_time: float
    error_rate: float
    system_health: str  # healthy, degraded, error 
