"""
Passive data schemas for MindBridge application.

This module defines Pydantic schemas for passive data point
validation, serialization, and request/response handling.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class DataTypeEnum(str, Enum):
    """Enumeration of supported passive data types."""
    
    # Sleep data
    SLEEP_DURATION = "sleep_duration"
    SLEEP_QUALITY = "sleep_quality"
    SLEEP_EFFICIENCY = "sleep_efficiency"
    
    # Activity data
    STEP_COUNT = "step_count"
    EXERCISE_DURATION = "exercise_duration"
    ACTIVE_MINUTES = "active_minutes"
    CALORIES_BURNED = "calories_burned"
    
    # Health metrics
    HEART_RATE = "heart_rate"
    HEART_RATE_VARIABILITY = "heart_rate_variability"
    BLOOD_PRESSURE = "blood_pressure"
    WEIGHT = "weight"
    
    # Screen time and usage
    SCREEN_TIME = "screen_time"
    APP_USAGE = "app_usage"
    NOTIFICATION_COUNT = "notification_count"
    
    # Environmental
    LOCATION_SUMMARY = "location_summary"
    WEATHER_EXPOSURE = "weather_exposure"
    AMBIENT_LIGHT = "ambient_light"
    NOISE_LEVEL = "noise_level"
    
    # Social and communication
    SOCIAL_INTERACTION = "social_interaction"
    CALL_DURATION = "call_duration"
    MESSAGE_COUNT = "message_count"


class DataSourceEnum(str, Enum):
    """Enumeration of supported data sources."""
    
    # Health platforms
    HEALTH_KIT = "HealthKit"
    GOOGLE_FIT = "GoogleFit"
    FITBIT = "Fitbit"
    SAMSUNG_HEALTH = "Samsung Health"
    
    # Device sensors
    DEVICE_SENSORS = "device_sensors"
    SMARTPHONE = "smartphone"
    WEARABLE = "wearable"
    
    # Apps and services
    SCREEN_TIME_API = "screen_time_api"
    LOCATION_SERVICES = "location_services"
    WEATHER_API = "weather_api"
    CALENDAR = "calendar"
    
    # Internal app tracking
    INTERNAL_TRACKING = "internal_tracking"
    USER_BEHAVIOR = "user_behavior"


class PassiveDataCreate(BaseModel):
    """Schema for creating a passive data point."""
    
    data_type: DataTypeEnum
    value: Union[int, float, str, Dict[str, Any]]
    source: DataSourceEnum
    timestamp: Optional[datetime] = None
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    quality_score: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    
    @validator('value')
    def validate_value_by_type(cls, v, values):
        """Validate value based on data type."""
        if 'data_type' not in values:
            return v
        
        data_type = values['data_type']
        
        # Sleep data validation
        if data_type == DataTypeEnum.SLEEP_DURATION:
            if not isinstance(v, (int, float)) or v < 0 or v > 24:
                raise ValueError("Sleep duration must be between 0 and 24 hours")
        
        elif data_type == DataTypeEnum.SLEEP_QUALITY:
            if not isinstance(v, (int, float)) or v < 1 or v > 10:
                raise ValueError("Sleep quality must be between 1 and 10")
        
        # Activity data validation
        elif data_type == DataTypeEnum.STEP_COUNT:
            if not isinstance(v, int) or v < 0:
                raise ValueError("Step count must be a non-negative integer")
        
        elif data_type == DataTypeEnum.EXERCISE_DURATION:
            if not isinstance(v, (int, float)) or v < 0:
                raise ValueError("Exercise duration must be non-negative")
        
        # Health metrics validation
        elif data_type == DataTypeEnum.HEART_RATE:
            if not isinstance(v, (int, float)) or v < 30 or v > 250:
                raise ValueError("Heart rate must be between 30 and 250 bpm")
        
        elif data_type == DataTypeEnum.BLOOD_PRESSURE:
            if not isinstance(v, dict) or 'systolic' not in v or 'diastolic' not in v:
                raise ValueError("Blood pressure must include systolic and diastolic values")
        
        # Screen time validation
        elif data_type == DataTypeEnum.SCREEN_TIME:
            if not isinstance(v, (int, float)) or v < 0 or v > 24:
                raise ValueError("Screen time must be between 0 and 24 hours")
        
        return v


class PassiveDataUpdate(BaseModel):
    """Schema for updating a passive data point."""
    
    value: Optional[Union[int, float, str, Dict[str, Any]]] = None
    meta_data: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    processed: Optional[bool] = None


class PassiveDataResponse(BaseModel):
    """Schema for passive data point response."""
    
    data_point_id: int
    user_id: int
    timestamp: datetime
    data_type: str
    value: Union[int, float, str, Dict[str, Any]]
    source: str
    meta_data: Dict[str, Any]
    quality_score: float
    processed: bool
    
    class Config:
        orm_mode = True


class PassiveDataSummary(BaseModel):
    """Schema for passive data summary."""
    
    data_point_id: int
    timestamp: datetime
    data_type: str
    value: Union[int, float, str, Dict[str, Any]]
    source: str
    
    class Config:
        orm_mode = True


class PassiveDataBulkCreate(BaseModel):
    """Schema for bulk creating passive data points."""
    
    data_points: List[PassiveDataCreate] = Field(..., max_items=1000)
    process_async: bool = Field(default=False, description="Whether to process data asynchronously")
    
    @validator('data_points')
    def validate_data_points(cls, v):
        """Validate data points list."""
        if len(v) == 0:
            raise ValueError("At least one data point is required")
        return v


class DataAggregation(BaseModel):
    """Schema for data aggregation results."""
    
    data_type: str
    period: str  # hourly, daily, weekly, monthly
    start_date: datetime
    end_date: datetime
    aggregated_value: Union[int, float, Dict[str, Any]]
    count: int
    source_breakdown: Dict[str, int]


class HealthMetrics(BaseModel):
    """Schema for health metrics summary."""
    
    date: str
    sleep_duration: Optional[float] = None
    sleep_quality: Optional[float] = None
    step_count: Optional[int] = None
    exercise_duration: Optional[float] = None
    heart_rate_avg: Optional[float] = None
    screen_time: Optional[float] = None


class ActivitySummary(BaseModel):
    """Schema for activity summary."""
    
    date: str
    total_steps: int
    active_minutes: int
    calories_burned: int
    exercise_sessions: int
    most_active_hour: Optional[str] = None


class SleepAnalysis(BaseModel):
    """Schema for sleep analysis."""
    
    date: str
    duration: float
    quality: float
    efficiency: float
    bedtime: Optional[str] = None
    wake_time: Optional[str] = None
    sleep_stages: Optional[Dict[str, float]] = None


class DataSourceStatus(BaseModel):
    """Schema for data source status."""
    
    source: str
    last_sync: Optional[datetime] = None
    status: str  # active, inactive, error
    error_message: Optional[str] = None
    data_types: List[str]
    total_points: int


class DataProcessingStatus(BaseModel):
    """Schema for data processing status."""
    
    total_points: int
    processed_points: int
    processing_rate: float
    last_processed: Optional[datetime] = None
    errors: List[str]


class DataQualityMetrics(BaseModel):
    """Schema for data quality metrics."""
    
    data_type: str
    average_quality: float
    quality_distribution: Dict[str, int]  # quality ranges
    outlier_count: int
    missing_data_periods: List[Dict[str, datetime]]


class BulkIngestResponse(BaseModel):
    """Schema for bulk ingest response."""
    
    success_count: int
    error_count: int
    total_count: int
    created_ids: List[int]
    processing_async: bool 