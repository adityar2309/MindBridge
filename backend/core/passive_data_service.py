"""
Passive data service for MindBridge application.

This module provides core business logic for handling passive data
ingestion, validation, de-duplication, and aggregation.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import hashlib
import json

from ..models import PassiveDataPoint, User, DataType, DataSource
from ..schemas import (
    PassiveDataCreate, PassiveDataUpdate, PassiveDataResponse,
    PassiveDataBulkCreate, DataAggregation, HealthMetrics
)


class PassiveDataService:
    """
    Service class for handling passive data operations.
    
    This class provides methods for ingesting, validating, and processing
    passive data points from various sources.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the passive data service.
        
        Args:
            db: Database session instance.
        """
        self.db = db
    
    def ingest_data_point(self, user_id: int, 
                         data_point: PassiveDataCreate) -> PassiveDataPoint:
        """
        Ingest a single passive data point.
        
        Args:
            user_id: User ID.
            data_point: Passive data point to ingest.
            
        Returns:
            Created PassiveDataPoint instance.
            
        Raises:
            ValueError: If validation fails or duplicate detected.
        """
        # Validate data point
        validation_errors = self.validate_data_point(data_point)
        if validation_errors:
            raise ValueError(f"Validation failed: {', '.join(validation_errors)}")
        
        # Check for duplicates
        if self._is_duplicate(user_id, data_point):
            raise ValueError("Duplicate data point detected")
        
        # Create data point
        db_data_point = PassiveDataPoint(
            user_id=user_id,
            data_type=data_point.data_type.value,
            value=data_point.value,
            source=data_point.source.value,
            timestamp=data_point.timestamp or datetime.now(),
            metadata=data_point.metadata or {},
            quality_score=data_point.quality_score or 1.0
        )
        
        self.db.add(db_data_point)
        self.db.commit()
        self.db.refresh(db_data_point)
        
        return db_data_point
    
    def bulk_ingest(self, user_id: int, 
                   bulk_data: PassiveDataBulkCreate) -> List[PassiveDataPoint]:
        """
        Bulk ingest multiple passive data points.
        
        Args:
            user_id: User ID.
            bulk_data: Bulk data containing multiple data points.
            
        Returns:
            List of created PassiveDataPoint instances.
        """
        created_points = []
        errors = []
        
        for i, data_point in enumerate(bulk_data.data_points):
            try:
                # Validate data point
                validation_errors = self.validate_data_point(data_point)
                if validation_errors:
                    errors.append(f"Item {i}: {', '.join(validation_errors)}")
                    continue
                
                # Check for duplicates
                if self._is_duplicate(user_id, data_point):
                    errors.append(f"Item {i}: Duplicate data point")
                    continue
                
                # Create data point
                db_data_point = PassiveDataPoint(
                    user_id=user_id,
                    data_type=data_point.data_type.value,
                    value=data_point.value,
                    source=data_point.source.value,
                    timestamp=data_point.timestamp or datetime.now(),
                    metadata=data_point.metadata or {},
                    quality_score=data_point.quality_score or 1.0
                )
                
                created_points.append(db_data_point)
                
            except Exception as e:
                errors.append(f"Item {i}: {str(e)}")
        
        # Batch insert successful data points
        if created_points:
            self.db.add_all(created_points)
            self.db.commit()
            
            # Refresh all instances
            for point in created_points:
                self.db.refresh(point)
        
        # Log errors if any
        if errors:
            print(f"Bulk ingest errors: {errors}")
        
        return created_points
    
    def update_data_point(self, data_point_id: int, user_id: int, 
                         update_data: PassiveDataUpdate) -> Optional[PassiveDataPoint]:
        """
        Update an existing passive data point.
        
        Args:
            data_point_id: Data point ID.
            user_id: User ID.
            update_data: Update data.
            
        Returns:
            Updated PassiveDataPoint instance or None if not found.
        """
        data_point = self.db.query(PassiveDataPoint).filter(
            and_(
                PassiveDataPoint.data_point_id == data_point_id,
                PassiveDataPoint.user_id == user_id
            )
        ).first()
        
        if not data_point:
            return None
        
        # Update fields if provided
        update_fields = update_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(data_point, field, value)
        
        self.db.commit()
        self.db.refresh(data_point)
        
        return data_point
    
    def get_data_points(self, user_id: int, data_type: Optional[str] = None,
                       source: Optional[str] = None, start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None, limit: int = 100,
                       offset: int = 0) -> List[PassiveDataPoint]:
        """
        Get passive data points with filters.
        
        Args:
            user_id: User ID.
            data_type: Optional data type filter.
            source: Optional source filter.
            start_date: Optional start date filter.
            end_date: Optional end date filter.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            List of PassiveDataPoint instances.
        """
        query = self.db.query(PassiveDataPoint).filter(
            PassiveDataPoint.user_id == user_id
        )
        
        if data_type:
            query = query.filter(PassiveDataPoint.data_type == data_type)
        
        if source:
            query = query.filter(PassiveDataPoint.source == source)
        
        if start_date:
            query = query.filter(PassiveDataPoint.timestamp >= start_date)
        
        if end_date:
            query = query.filter(PassiveDataPoint.timestamp <= end_date)
        
        return query.order_by(PassiveDataPoint.timestamp.desc()).limit(limit).offset(offset).all()
    
    def aggregate_data(self, user_id: int, data_type: str, 
                      period: str = "daily", start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> List[DataAggregation]:
        """
        Aggregate passive data points by time period.
        
        Args:
            user_id: User ID.
            data_type: Data type to aggregate.
            period: Aggregation period (hourly, daily, weekly, monthly).
            start_date: Start date for aggregation.
            end_date: End date for aggregation.
            
        Returns:
            List of DataAggregation instances.
        """
        # Default date range if not provided
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            if period == "hourly":
                start_date = end_date - timedelta(days=1)
            elif period == "daily":
                start_date = end_date - timedelta(days=30)
            elif period == "weekly":
                start_date = end_date - timedelta(days=90)
            else:  # monthly
                start_date = end_date - timedelta(days=365)
        
        # Get data points
        data_points = self.get_data_points(
            user_id=user_id,
            data_type=data_type,
            start_date=start_date,
            end_date=end_date,
            limit=10000  # Large limit for aggregation
        )
        
        # Group by time period
        aggregations = {}
        
        for point in data_points:
            # Determine grouping key based on period
            if period == "hourly":
                key = point.timestamp.strftime("%Y-%m-%d %H:00:00")
            elif period == "daily":
                key = point.timestamp.strftime("%Y-%m-%d")
            elif period == "weekly":
                # Week starting Monday
                week_start = point.timestamp - timedelta(days=point.timestamp.weekday())
                key = week_start.strftime("%Y-%m-%d")
            else:  # monthly
                key = point.timestamp.strftime("%Y-%m")
            
            if key not in aggregations:
                aggregations[key] = {
                    "values": [],
                    "sources": {},
                    "quality_scores": []
                }
            
            # Add value for aggregation
            numeric_value = point.get_numeric_value()
            aggregations[key]["values"].append(numeric_value)
            
            # Track sources
            source = point.source
            aggregations[key]["sources"][source] = aggregations[key]["sources"].get(source, 0) + 1
            
            # Track quality scores
            aggregations[key]["quality_scores"].append(point.quality_score)
        
        # Calculate aggregated values
        result = []
        for key, data in aggregations.items():
            if period == "hourly":
                period_start = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
                period_end = period_start + timedelta(hours=1)
            elif period == "daily":
                period_start = datetime.strptime(key, "%Y-%m-%d")
                period_end = period_start + timedelta(days=1)
            elif period == "weekly":
                period_start = datetime.strptime(key, "%Y-%m-%d")
                period_end = period_start + timedelta(weeks=1)
            else:  # monthly
                period_start = datetime.strptime(key + "-01", "%Y-%m-%d")
                if period_start.month == 12:
                    period_end = period_start.replace(year=period_start.year + 1, month=1)
                else:
                    period_end = period_start.replace(month=period_start.month + 1)
            
            # Calculate aggregated value based on data type
            if data_type in ["step_count", "notification_count", "message_count"]:
                # Sum for counting data types
                aggregated_value = sum(data["values"])
            else:
                # Average for other data types
                aggregated_value = sum(data["values"]) / len(data["values"])
            
            result.append(DataAggregation(
                data_type=data_type,
                period=period,
                start_date=period_start,
                end_date=period_end,
                aggregated_value=aggregated_value,
                count=len(data["values"]),
                source_breakdown=data["sources"]
            ))
        
        return sorted(result, key=lambda x: x.start_date)
    
    def get_health_metrics(self, user_id: int, 
                          date: Optional[datetime] = None) -> HealthMetrics:
        """
        Get health metrics for a specific date.
        
        Args:
            user_id: User ID.
            date: Date to get metrics for (defaults to today).
            
        Returns:
            HealthMetrics instance.
        """
        if not date:
            date = datetime.now()
        
        # Get data points for the day
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        data_points = self.get_data_points(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )
        
        # Extract metrics
        metrics = {
            "sleep_duration": None,
            "sleep_quality": None,
            "step_count": None,
            "exercise_duration": None,
            "heart_rate_avg": None,
            "screen_time": None
        }
        
        # Process data points
        heart_rates = []
        
        for point in data_points:
            if point.data_type == "sleep_duration":
                metrics["sleep_duration"] = point.get_numeric_value()
            elif point.data_type == "sleep_quality":
                metrics["sleep_quality"] = point.get_numeric_value()
            elif point.data_type == "step_count":
                metrics["step_count"] = int(point.get_numeric_value())
            elif point.data_type == "exercise_duration":
                metrics["exercise_duration"] = point.get_numeric_value()
            elif point.data_type == "heart_rate":
                heart_rates.append(point.get_numeric_value())
            elif point.data_type == "screen_time":
                metrics["screen_time"] = point.get_numeric_value()
        
        # Calculate average heart rate
        if heart_rates:
            metrics["heart_rate_avg"] = sum(heart_rates) / len(heart_rates)
        
        return HealthMetrics(
            date=date.date().isoformat(),
            **metrics
        )
    
    def validate_data_point(self, data_point: PassiveDataCreate) -> List[str]:
        """
        Validate a passive data point.
        
        Args:
            data_point: Data point to validate.
            
        Returns:
            List of validation error messages.
        """
        errors = []
        
        # Validate data type
        if data_point.data_type not in DataType:
            errors.append(f"Invalid data type: {data_point.data_type}")
        
        # Validate source
        if data_point.source not in DataSource:
            errors.append(f"Invalid source: {data_point.source}")
        
        # Validate quality score
        if data_point.quality_score is not None:
            if not (0.0 <= data_point.quality_score <= 1.0):
                errors.append("Quality score must be between 0.0 and 1.0")
        
        # Validate timestamp
        if data_point.timestamp:
            if data_point.timestamp > datetime.now():
                errors.append("Timestamp cannot be in the future")
            if data_point.timestamp < datetime.now() - timedelta(days=365):
                errors.append("Timestamp cannot be more than 1 year in the past")
        
        return errors
    
    def _is_duplicate(self, user_id: int, data_point: PassiveDataCreate) -> bool:
        """
        Check if a data point is a duplicate.
        
        Args:
            user_id: User ID.
            data_point: Data point to check.
            
        Returns:
            True if duplicate, False otherwise.
        """
        # Create a hash of the data point for duplicate detection
        data_hash = self._create_data_hash(data_point)
        
        # Check for existing data point with same hash within a small time window
        timestamp = data_point.timestamp or datetime.now()
        window_start = timestamp - timedelta(minutes=5)
        window_end = timestamp + timedelta(minutes=5)
        
        existing = self.db.query(PassiveDataPoint).filter(
            and_(
                PassiveDataPoint.user_id == user_id,
                PassiveDataPoint.data_type == data_point.data_type.value,
                PassiveDataPoint.source == data_point.source.value,
                PassiveDataPoint.timestamp >= window_start,
                PassiveDataPoint.timestamp <= window_end
            )
        ).first()
        
        if existing:
            # Check if values are similar (for duplicate detection)
            existing_hash = self._create_data_hash_from_db(existing)
            return data_hash == existing_hash
        
        return False
    
    def _create_data_hash(self, data_point: PassiveDataCreate) -> str:
        """
        Create a hash for duplicate detection.
        
        Args:
            data_point: Data point to hash.
            
        Returns:
            Hash string.
        """
        hash_data = {
            "data_type": data_point.data_type.value,
            "value": data_point.value,
            "source": data_point.source.value
        }
        
        hash_string = json.dumps(hash_data, sort_keys=True)
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def _create_data_hash_from_db(self, data_point: PassiveDataPoint) -> str:
        """
        Create a hash from a database data point.
        
        Args:
            data_point: Database data point.
            
        Returns:
            Hash string.
        """
        hash_data = {
            "data_type": data_point.data_type,
            "value": data_point.value,
            "source": data_point.source
        }
        
        hash_string = json.dumps(hash_data, sort_keys=True)
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def mark_processed(self, data_point_ids: List[int]) -> int:
        """
        Mark data points as processed.
        
        Args:
            data_point_ids: List of data point IDs to mark as processed.
            
        Returns:
            Number of data points marked as processed.
        """
        updated_count = self.db.query(PassiveDataPoint).filter(
            PassiveDataPoint.data_point_id.in_(data_point_ids)
        ).update({PassiveDataPoint.processed: True}, synchronize_session=False)
        
        self.db.commit()
        return updated_count
    
    def get_unprocessed_data(self, limit: int = 1000) -> List[PassiveDataPoint]:
        """
        Get unprocessed data points for ML processing.
        
        Args:
            limit: Maximum number of data points to return.
            
        Returns:
            List of unprocessed PassiveDataPoint instances.
        """
        return self.db.query(PassiveDataPoint).filter(
            PassiveDataPoint.processed == False
        ).order_by(PassiveDataPoint.timestamp.asc()).limit(limit).all() 