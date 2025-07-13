"""
Quiz models for MindBridge application.

This module defines the QuizQuestion and QuizSession models for
storing quiz questions and user responses, including adaptive
quiz flows and mood assessment quizzes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum


class QuestionType(str, Enum):
    """Enumeration of supported question types."""
    
    MULTIPLE_CHOICE = "multiple_choice"
    SLIDER = "slider"
    OPEN_TEXT = "open_text"
    LIKERT_SCALE = "likert_scale"
    YES_NO = "yes_no"
    RATING = "rating"
    CHECKBOX = "checkbox"


class QuizType(str, Enum):
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


class QuizQuestion(Base):
    """
    Quiz question model for storing question templates.
    
    Attributes:
        question_id: Primary key identifier
        question_text: The actual question text
        question_type: Type of question (multiple choice, slider, etc.)
        options: Available options for multiple choice questions
        min_value: Minimum value for slider/rating questions
        max_value: Maximum value for slider/rating questions
        category: Question category (mood, stress, sleep, etc.)
        tags: Keywords associated with the question
        is_active: Whether the question is active in the pool
        difficulty_level: Difficulty/complexity level (1-5)
        expected_response_time: Expected time to answer in seconds
    """
    
    __tablename__ = "quiz_questions"
    
    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)
    options = Column(JSON, nullable=True)  # For multiple choice questions
    min_value = Column(Float, nullable=True)  # For slider/rating questions
    max_value = Column(Float, nullable=True)  # For slider/rating questions
    category = Column(String(50), nullable=False)
    tags = Column(JSON, default=list)  # Keywords/tags
    is_active = Column(Boolean, default=True)
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    expected_response_time = Column(Integer, default=30)  # Seconds
    
    # Relationships
    quiz_responses = relationship("QuizResponse", back_populates="question")
    
    def __repr__(self) -> str:
        return f"<QuizQuestion(question_id={self.question_id}, category='{self.category}')>"
    
    def to_dict(self) -> dict:
        """Convert quiz question to dictionary."""
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "options": self.options,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "category": self.category,
            "tags": self.tags,
            "is_active": self.is_active,
            "difficulty_level": self.difficulty_level,
            "expected_response_time": self.expected_response_time
        }


class QuizSession(Base):
    """
    Quiz session model for storing user quiz sessions.
    
    Attributes:
        session_id: Primary key identifier
        user_id: Foreign key to User model
        quiz_type: Type of quiz being taken
        start_time: When the quiz session started
        end_time: When the quiz session ended
        completion_rate: Percentage of questions completed
        final_mood_score: Derived mood score from responses
        session_context: Additional context about the session
        adaptive_flow: Whether adaptive questioning was used
    """
    
    __tablename__ = "quiz_sessions"
    
    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    quiz_type = Column(String(50), nullable=False)
    start_time = Column(DateTime, default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)
    completion_rate = Column(Float, default=0.0)  # 0-100%
    final_mood_score = Column(Float, nullable=True)
    session_context = Column(JSON, default=dict)  # Additional context
    adaptive_flow = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="quiz_sessions")
    responses = relationship("QuizResponse", back_populates="session")
    
    def __repr__(self) -> str:
        return f"<QuizSession(session_id={self.session_id}, user_id={self.user_id}, quiz_type='{self.quiz_type}')>"
    
    def to_dict(self) -> dict:
        """Convert quiz session to dictionary."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "quiz_type": self.quiz_type,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "completion_rate": self.completion_rate,
            "final_mood_score": self.final_mood_score,
            "session_context": self.session_context,
            "adaptive_flow": self.adaptive_flow
        }


class QuizResponse(Base):
    """
    Quiz response model for storing individual question responses.
    
    Attributes:
        response_id: Primary key identifier
        session_id: Foreign key to QuizSession
        question_id: Foreign key to QuizQuestion
        user_answer: The user's answer to the question
        response_time: Time taken to answer in seconds
        confidence_score: User's confidence in their answer (1-10)
        timestamp: When the response was recorded
    """
    
    __tablename__ = "quiz_responses"
    
    response_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.session_id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.question_id"), nullable=False)
    user_answer = Column(JSON, nullable=False)  # Can be various types
    response_time = Column(Float, nullable=True)  # Seconds
    confidence_score = Column(Float, nullable=True)  # 1-10 scale
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    session = relationship("QuizSession", back_populates="responses")
    question = relationship("QuizQuestion", back_populates="quiz_responses")
    
    def __repr__(self) -> str:
        return f"<QuizResponse(response_id={self.response_id}, session_id={self.session_id}, question_id={self.question_id})>"
    
    def to_dict(self) -> dict:
        """Convert quiz response to dictionary."""
        return {
            "response_id": self.response_id,
            "session_id": self.session_id,
            "question_id": self.question_id,
            "user_answer": self.user_answer,
            "response_time": self.response_time,
            "confidence_score": self.confidence_score,
            "timestamp": self.timestamp.isoformat()
        } 
