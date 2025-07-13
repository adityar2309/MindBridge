"""
Schemas package for MindBridge application.

This module exports all Pydantic schemas for easy importing
throughout the application.
"""

# User schemas
from .user_schemas import (
    UserCreate, UserLogin, UserUpdate, UserResponse, UserProfile,
    PasswordChange, TokenResponse, RefreshTokenRequest,
    ForgotPasswordRequest, ResetPasswordRequest, UserSettings
)

# Check-in schemas
from .checkin_schemas import (
    DailyCheckinCreate, DailyCheckinUpdate, DailyCheckinResponse,
    DailyCheckinSummary, MoodTrend, MoodAnalytics, CheckinStreak,
    QuickMoodEntry, MoodCategories, CheckinReminder
)

# Passive data schemas
from .passive_data_schemas import (
    PassiveDataCreate, PassiveDataUpdate, PassiveDataResponse,
    PassiveDataSummary, PassiveDataBulkCreate, DataAggregation,
    HealthMetrics, ActivitySummary, SleepAnalysis, DataSourceStatus,
    DataProcessingStatus, DataQualityMetrics, DataTypeEnum, DataSourceEnum
)

# Quiz schemas
from .quiz_schemas import (
    QuizQuestionCreate, QuizQuestionUpdate, QuizQuestionResponse,
    QuizSessionCreate, QuizSessionUpdate, QuizSessionResponse,
    QuizResponseCreate, QuizResponseResponse, QuizSessionSummary,
    AdaptiveQuizFlow, QuizRecommendation, QuizAnalytics,
    QuestionBankSummary, QuizInsight, QuestionTypeEnum, QuizTypeEnum
)

# AI schemas
from .ai_schemas import (
    AIMoodInsightCreate, AIMoodInsightUpdate, AIMoodInsightResponse,
    ConversationCreate, ConversationUpdate, ConversationResponse,
    ChatMessage, ChatResponse, MoodPredictionRequest, MoodPredictionResponse,
    PatternAnalysisRequest, PatternAnalysisResponse, RecommendationRequest,
    RecommendationResponse, ModelPerformanceMetrics, FeedbackSubmission,
    UserFeedbackAnalysis, AISystemStatus, InsightTypeEnum,
    RecommendationTypeEnum, PriorityLevel
)

# Export all schemas for easy importing
__all__ = [
    # User schemas
    "UserCreate", "UserLogin", "UserUpdate", "UserResponse", "UserProfile",
    "PasswordChange", "TokenResponse", "RefreshTokenRequest",
    "ForgotPasswordRequest", "ResetPasswordRequest", "UserSettings",
    
    # Check-in schemas
    "DailyCheckinCreate", "DailyCheckinUpdate", "DailyCheckinResponse",
    "DailyCheckinSummary", "MoodTrend", "MoodAnalytics", "CheckinStreak",
    "QuickMoodEntry", "MoodCategories", "CheckinReminder",
    
    # Passive data schemas
    "PassiveDataCreate", "PassiveDataUpdate", "PassiveDataResponse",
    "PassiveDataSummary", "PassiveDataBulkCreate", "DataAggregation",
    "HealthMetrics", "ActivitySummary", "SleepAnalysis", "DataSourceStatus",
    "DataProcessingStatus", "DataQualityMetrics", "DataTypeEnum", "DataSourceEnum",
    
    # Quiz schemas
    "QuizQuestionCreate", "QuizQuestionUpdate", "QuizQuestionResponse",
    "QuizSessionCreate", "QuizSessionUpdate", "QuizSessionResponse",
    "QuizResponseCreate", "QuizResponseResponse", "QuizSessionSummary",
    "AdaptiveQuizFlow", "QuizRecommendation", "QuizAnalytics",
    "QuestionBankSummary", "QuizInsight", "QuestionTypeEnum", "QuizTypeEnum",
    
    # AI schemas
    "AIMoodInsightCreate", "AIMoodInsightUpdate", "AIMoodInsightResponse",
    "ConversationCreate", "ConversationUpdate", "ConversationResponse",
    "ChatMessage", "ChatResponse", "MoodPredictionRequest", "MoodPredictionResponse",
    "PatternAnalysisRequest", "PatternAnalysisResponse", "RecommendationRequest",
    "RecommendationResponse", "ModelPerformanceMetrics", "FeedbackSubmission",
    "UserFeedbackAnalysis", "AISystemStatus", "InsightTypeEnum",
    "RecommendationTypeEnum", "PriorityLevel",
] 