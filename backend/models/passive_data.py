"""
Passive data model for MindBridge application.

This module defines the PassiveDataPoint model for storing
passively collected data from various sources like health apps,
device sensors, and usage patterns.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum


class DataType(str, Enum):
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


class DataSource(str, Enum):
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


class PassiveDataPoint(Base):
    """
    Passive data point model for storing automatically collected data.
    
    Attributes:
        data_point_id: Primary key identifier
        user_id: Foreign key to User model
        timestamp: When the data point was recorded
        data_type: Type of data being recorded
        value: The actual data value (can be numeric or JSON)
        source: Source of the data
        metadata: Additional context information
        quality_score: Data quality/reliability score (0-1)
        processed: Whether the data has been processed by ML models
    """
    
    __tablename__ = "passive_data_points"
    
    data_point_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    data_type = Column(String(50), nullable=False)
    value = Column(JSON, nullable=False)  # Can store numeric or complex data
    source = Column(String(50), nullable=False)
    metadata = Column(JSON, default=dict)  # Additional context
    quality_score = Column(Float, default=1.0)  # 0-1 reliability score
    processed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="passive_data")
    
    def __repr__(self) -> str:
        return f"<PassiveDataPoint(data_point_id={self.data_point_id}, data_type='{self.data_type}', value={self.value})>"
    
    def to_dict(self) -> dict:
        """Convert passive data point to dictionary."""
        return {
            "data_point_id": self.data_point_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "data_type": self.data_type,
            "value": self.value,
            "source": self.source,
            "metadata": self.metadata,
            "quality_score": self.quality_score,
            "processed": self.processed
        }
    
    @classmethod
    def get_supported_data_types(cls) -> list:
        """Get list of supported data types."""
        return [data_type.value for data_type in DataType]
    
    @classmethod
    def get_supported_sources(cls) -> list:
        """Get list of supported data sources."""
        return [source.value for source in DataSource]
    
    def get_numeric_value(self) -> float:
        """
        Extract numeric value from the data point.
        
        Returns:
            Numeric representation of the value.
        """
        if isinstance(self.value, (int, float)):
            return float(self.value)
        elif isinstance(self.value, dict) and "value" in self.value:
            return float(self.value["value"])
        else:
            return 0.0 