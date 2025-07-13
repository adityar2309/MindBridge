"""
Quiz schemas for MindBridge application.

This module defines Pydantic schemas for quiz-related
validation, serialization, and request/response handling.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class QuestionTypeEnum(str, Enum):
    """Enumeration of supported question types."""
    
    MULTIPLE_CHOICE = "multiple_choice"
    SLIDER = "slider"
    OPEN_TEXT = "open_text"
    LIKERT_SCALE = "likert_scale"
    YES_NO = "yes_no"
    RATING = "rating"
    CHECKBOX = "checkbox"


class QuizTypeEnum(str, Enum):
    """Enumeration of supported quiz types."""
    
    MORNING_MOOD = "morning_mood"
    EVENING_REFLECTION = "evening_reflection"
    STRESS_ASSESSMENT = "stress_assessment"
    ANXIETY_CHECK = "anxiety_check"
    DEPRESSION_SCREENING = "depression_screening"
    WELLBEING_SURVEY = "wellbeing_survey"
    DAILY_HABITS = "daily_habits"
    SLEEP_QUALITY = "sleep_quality"
    SOCIAL_CONNECTION = "social_connection"
    WORK_LIFE_BALANCE = "work_life_balance"


class QuizQuestionCreate(BaseModel):
    """Schema for creating a quiz question."""
    
    question_text: str = Field(..., min_length=10, max_length=500)
    question_type: QuestionTypeEnum
    options: Optional[List[str]] = Field(None, max_items=10)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    category: str = Field(..., max_length=50)
    tags: Optional[List[str]] = Field(default_factory=list, max_items=20)
    difficulty_level: Optional[int] = Field(default=1, ge=1, le=5)
    expected_response_time: Optional[int] = Field(default=30, ge=5, le=300)
    
    @validator('options')
    def validate_options(cls, v, values):
        """Validate options based on question type."""
        if 'question_type' not in values:
            return v
        
        question_type = values['question_type']
        
        if question_type == QuestionTypeEnum.MULTIPLE_CHOICE:
            if not v or len(v) < 2:
                raise ValueError("Multiple choice questions must have at least 2 options")
        elif question_type == QuestionTypeEnum.YES_NO:
            if v and len(v) != 2:
                raise ValueError("Yes/No questions must have exactly 2 options")
        elif question_type in [QuestionTypeEnum.SLIDER, QuestionTypeEnum.RATING]:
            if v:
                raise ValueError("Slider and rating questions should not have options")
        
        return v
    
    @validator('min_value')
    def validate_min_value(cls, v, values):
        """Validate min_value based on question type."""
        if 'question_type' not in values:
            return v
        
        question_type = values['question_type']
        
        if question_type in [QuestionTypeEnum.SLIDER, QuestionTypeEnum.RATING]:
            if v is None:
                raise ValueError("Slider and rating questions must have min_value")
        
        return v
    
    @validator('max_value')
    def validate_max_value(cls, v, values):
        """Validate max_value based on question type."""
        if 'question_type' not in values or 'min_value' not in values:
            return v
        
        question_type = values['question_type']
        min_value = values['min_value']
        
        if question_type in [QuestionTypeEnum.SLIDER, QuestionTypeEnum.RATING]:
            if v is None:
                raise ValueError("Slider and rating questions must have max_value")
            if min_value is not None and v <= min_value:
                raise ValueError("max_value must be greater than min_value")
        
        return v


class QuizQuestionUpdate(BaseModel):
    """Schema for updating a quiz question."""
    
    question_text: Optional[str] = Field(None, min_length=10, max_length=500)
    options: Optional[List[str]] = Field(None, max_items=10)
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = Field(None, max_items=20)
    is_active: Optional[bool] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)


class QuizQuestionResponse(BaseModel):
    """Schema for quiz question response."""
    
    question_id: int
    question_text: str
    question_type: str
    options: Optional[List[str]]
    min_value: Optional[float]
    max_value: Optional[float]
    category: str
    tags: List[str]
    is_active: bool
    difficulty_level: int
    expected_response_time: int
    
    class Config:
        orm_mode = True


class QuizSessionCreate(BaseModel):
    """Schema for creating a quiz session."""
    
    quiz_type: QuizTypeEnum
    session_context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    adaptive_flow: Optional[bool] = Field(default=False)


class QuizResponseCreate(BaseModel):
    """Schema for creating a quiz response."""
    
    question_id: int
    user_answer: Union[str, int, float, List[str], Dict[str, Any]]
    response_time: Optional[float] = Field(None, ge=0)
    confidence_score: Optional[float] = Field(None, ge=1, le=10)
    
    @validator('user_answer')
    def validate_user_answer(cls, v):
        """Validate user answer format."""
        if v is None:
            raise ValueError("User answer cannot be None")
        return v


class QuizSessionUpdate(BaseModel):
    """Schema for updating a quiz session."""
    
    completion_rate: Optional[float] = Field(None, ge=0, le=100)
    final_mood_score: Optional[float] = Field(None, ge=1, le=10)
    session_context: Optional[Dict[str, Any]] = None


class QuizResponseResponse(BaseModel):
    """Schema for quiz response response."""
    
    response_id: int
    session_id: int
    question_id: int
    user_answer: Union[str, int, float, List[str], Dict[str, Any]]
    response_time: Optional[float]
    confidence_score: Optional[float]
    timestamp: datetime
    
    class Config:
        orm_mode = True


class QuizSessionResponse(BaseModel):
    """Schema for quiz session response."""
    
    session_id: int
    user_id: int
    quiz_type: str
    start_time: datetime
    end_time: Optional[datetime]
    completion_rate: float
    final_mood_score: Optional[float]
    session_context: Dict[str, Any]
    adaptive_flow: bool
    responses: Optional[List[QuizResponseResponse]] = None
    
    class Config:
        orm_mode = True


class QuizSessionSummary(BaseModel):
    """Schema for quiz session summary."""
    
    session_id: int
    quiz_type: str
    start_time: datetime
    completion_rate: float
    final_mood_score: Optional[float]
    
    class Config:
        orm_mode = True


class AdaptiveQuizFlow(BaseModel):
    """Schema for adaptive quiz flow configuration."""
    
    question_selection_strategy: str  # random, difficulty_based, context_based
    max_questions: int = Field(default=10, ge=1, le=50)
    completion_criteria: Dict[str, Any] = Field(default_factory=dict)
    branching_rules: Dict[str, Any] = Field(default_factory=dict)


class QuizRecommendation(BaseModel):
    """Schema for quiz recommendations."""
    
    quiz_type: str
    reason: str
    priority: str  # low, medium, high
    estimated_duration: int  # minutes
    benefits: List[str]


class QuizAnalytics(BaseModel):
    """Schema for quiz analytics."""
    
    total_sessions: int
    completion_rate: float
    average_session_duration: float
    most_popular_quiz_type: str
    mood_score_trend: List[Dict[str, Any]]
    response_patterns: Dict[str, Any]


class QuestionBankSummary(BaseModel):
    """Schema for question bank summary."""
    
    total_questions: int
    questions_by_category: Dict[str, int]
    questions_by_type: Dict[str, int]
    active_questions: int
    average_difficulty: float


class QuizInsight(BaseModel):
    """Schema for quiz-based insights."""
    
    session_id: int
    insight_type: str
    insight_text: str
    confidence_score: float
    recommendations: List[str]
    related_patterns: List[str] 