"""
Check-in service for MindBridge application.

This module provides core business logic for handling daily check-ins,
including validation, processing, and analytics.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from models import DailyCheckin, User
from schemas import (
    DailyCheckinCreate, DailyCheckinUpdate, DailyCheckinResponse,
    MoodAnalytics, CheckinStreak, MoodTrend
)


class CheckinService:
    """
    Service class for handling daily check-in operations.
    
    This class provides methods for creating, updating, and analyzing
    daily check-ins, including mood trends and streak tracking.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the checkin service.
        
        Args:
            db: Database session instance.
        """
        self.db = db
    
    def create_checkin(self, user_id: int, checkin_data: DailyCheckinCreate) -> DailyCheckin:
        """
        Create a new daily check-in for a user.
        
        Args:
            user_id: User ID.
            checkin_data: Check-in data from request.
            
        Returns:
            Created DailyCheckin instance.
            
        Raises:
            ValueError: If user already has a check-in for today.
        """
        # Check if user already has a check-in for today
        today = datetime.now().date()
        existing_checkin = self.db.query(DailyCheckin).filter(
            and_(
                DailyCheckin.user_id == user_id,
                func.date(DailyCheckin.timestamp) == today
            )
        ).first()
        
        if existing_checkin:
            raise ValueError("User already has a check-in for today")
        
        # Create new check-in
        checkin = DailyCheckin(
            user_id=user_id,
            mood_rating=checkin_data.mood_rating,
            mood_category=checkin_data.mood_category,
            keywords=checkin_data.keywords or [],
            notes=checkin_data.notes,
            location=checkin_data.location,
            weather=checkin_data.weather,
            energy_level=checkin_data.energy_level,
            stress_level=checkin_data.stress_level,
            sleep_quality=checkin_data.sleep_quality,
            social_interaction=checkin_data.social_interaction
        )
        
        self.db.add(checkin)
        self.db.commit()
        self.db.refresh(checkin)
        
        return checkin
    
    def update_checkin(self, checkin_id: int, user_id: int, 
                      update_data: DailyCheckinUpdate) -> Optional[DailyCheckin]:
        """
        Update an existing check-in.
        
        Args:
            checkin_id: Check-in ID.
            user_id: User ID.
            update_data: Update data.
            
        Returns:
            Updated DailyCheckin instance or None if not found.
        """
        checkin = self.db.query(DailyCheckin).filter(
            and_(
                DailyCheckin.checkin_id == checkin_id,
                DailyCheckin.user_id == user_id
            )
        ).first()
        
        if not checkin:
            return None
        
        # Update fields if provided
        update_fields = update_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(checkin, field, value)
        
        self.db.commit()
        self.db.refresh(checkin)
        
        return checkin
    
    def get_checkin_by_id(self, checkin_id: int, user_id: int) -> Optional[DailyCheckin]:
        """
        Get a check-in by ID.
        
        Args:
            checkin_id: Check-in ID.
            user_id: User ID.
            
        Returns:
            DailyCheckin instance or None if not found.
        """
        return self.db.query(DailyCheckin).filter(
            and_(
                DailyCheckin.checkin_id == checkin_id,
                DailyCheckin.user_id == user_id
            )
        ).first()
    
    def get_user_checkins(self, user_id: int, limit: int = 30, 
                         offset: int = 0) -> List[DailyCheckin]:
        """
        Get user's check-ins with pagination.
        
        Args:
            user_id: User ID.
            limit: Number of check-ins to return.
            offset: Number of check-ins to skip.
            
        Returns:
            List of DailyCheckin instances.
        """
        return self.db.query(DailyCheckin).filter(
            DailyCheckin.user_id == user_id
        ).order_by(DailyCheckin.timestamp.desc()).limit(limit).offset(offset).all()
    
    def get_todays_checkin(self, user_id: int) -> Optional[DailyCheckin]:
        """
        Get today's check-in for a user.
        
        Args:
            user_id: User ID.
            
        Returns:
            DailyCheckin instance or None if not found.
        """
        today = datetime.now().date()
        return self.db.query(DailyCheckin).filter(
            and_(
                DailyCheckin.user_id == user_id,
                func.date(DailyCheckin.timestamp) == today
            )
        ).first()
    
    def get_checkin_streak(self, user_id: int) -> CheckinStreak:
        """
        Calculate user's check-in streak.
        
        Args:
            user_id: User ID.
            
        Returns:
            CheckinStreak instance with streak information.
        """
        # Get all check-ins ordered by date
        checkins = self.db.query(DailyCheckin).filter(
            DailyCheckin.user_id == user_id
        ).order_by(DailyCheckin.timestamp.desc()).all()
        
        if not checkins:
            return CheckinStreak(
                current_streak=0,
                longest_streak=0,
                total_checkins=0,
                streak_start_date=None,
                days_since_last_checkin=0
            )
        
        # Calculate current streak
        current_streak = 0
        longest_streak = 0
        streak_start_date = None
        
        today = datetime.now().date()
        current_date = today
        
        # Check for consecutive days
        for checkin in checkins:
            checkin_date = checkin.timestamp.date()
            
            if checkin_date == current_date:
                current_streak += 1
                if current_streak == 1:
                    streak_start_date = checkin_date
                current_date -= timedelta(days=1)
            else:
                break
        
        # Calculate longest streak
        temp_streak = 0
        prev_date = None
        
        for checkin in reversed(checkins):
            checkin_date = checkin.timestamp.date()
            
            if prev_date is None or checkin_date == prev_date + timedelta(days=1):
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
            
            prev_date = checkin_date
        
        # Calculate days since last check-in
        last_checkin_date = checkins[0].timestamp.date()
        days_since_last_checkin = (today - last_checkin_date).days
        
        return CheckinStreak(
            current_streak=current_streak,
            longest_streak=longest_streak,
            total_checkins=len(checkins),
            streak_start_date=streak_start_date,
            days_since_last_checkin=days_since_last_checkin
        )
    
    def get_mood_analytics(self, user_id: int, period: str = "monthly") -> MoodAnalytics:
        """
        Get mood analytics for a user.
        
        Args:
            user_id: User ID.
            period: Analysis period (daily, weekly, monthly).
            
        Returns:
            MoodAnalytics instance with trend analysis.
        """
        # Determine date range based on period
        end_date = datetime.now()
        if period == "daily":
            start_date = end_date - timedelta(days=7)
        elif period == "weekly":
            start_date = end_date - timedelta(weeks=4)
        else:  # monthly
            start_date = end_date - timedelta(days=90)
        
        # Get check-ins in the period
        checkins = self.db.query(DailyCheckin).filter(
            and_(
                DailyCheckin.user_id == user_id,
                DailyCheckin.timestamp >= start_date,
                DailyCheckin.timestamp <= end_date
            )
        ).order_by(DailyCheckin.timestamp.asc()).all()
        
        if not checkins:
            return MoodAnalytics(
                period=period,
                average_mood=0.0,
                mood_range={"min": 0.0, "max": 0.0},
                most_common_category=None,
                trend_direction="stable",
                trend_data=[],
                keyword_frequency={},
                correlation_insights={}
            )
        
        # Calculate basic statistics
        mood_ratings = [c.mood_rating for c in checkins]
        average_mood = sum(mood_ratings) / len(mood_ratings)
        mood_range = {"min": min(mood_ratings), "max": max(mood_ratings)}
        
        # Find most common category
        categories = [c.mood_category for c in checkins if c.mood_category]
        most_common_category = max(set(categories), key=categories.count) if categories else None
        
        # Calculate trend direction
        if len(mood_ratings) < 2:
            trend_direction = "stable"
        else:
            first_half = mood_ratings[:len(mood_ratings)//2]
            second_half = mood_ratings[len(mood_ratings)//2:]
            
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg > first_avg + 0.5:
                trend_direction = "improving"
            elif second_avg < first_avg - 0.5:
                trend_direction = "declining"
            else:
                trend_direction = "stable"
        
        # Create trend data
        trend_data = []
        for checkin in checkins:
            trend_data.append(MoodTrend(
                date=checkin.timestamp.date().isoformat(),
                mood_rating=checkin.mood_rating,
                energy_level=checkin.energy_level,
                stress_level=checkin.stress_level,
                sleep_quality=checkin.sleep_quality
            ))
        
        # Calculate keyword frequency
        keyword_frequency = {}
        for checkin in checkins:
            for keyword in checkin.keywords:
                keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        
        # Basic correlation insights
        correlation_insights = self._calculate_correlations(checkins)
        
        return MoodAnalytics(
            period=period,
            average_mood=average_mood,
            mood_range=mood_range,
            most_common_category=most_common_category,
            trend_direction=trend_direction,
            trend_data=trend_data,
            keyword_frequency=keyword_frequency,
            correlation_insights=correlation_insights
        )
    
    def _calculate_correlations(self, checkins: List[DailyCheckin]) -> Dict[str, Any]:
        """
        Calculate basic correlations between mood and other factors.
        
        Args:
            checkins: List of check-ins.
            
        Returns:
            Dictionary with correlation insights.
        """
        if len(checkins) < 5:
            return {}
        
        # Extract data for correlation analysis
        mood_data = []
        energy_data = []
        stress_data = []
        sleep_data = []
        
        for checkin in checkins:
            mood_data.append(checkin.mood_rating)
            energy_data.append(checkin.energy_level or 5.0)
            stress_data.append(checkin.stress_level or 5.0)
            sleep_data.append(checkin.sleep_quality or 5.0)
        
        # Simple correlation calculation (Pearson)
        def simple_correlation(x, y):
            n = len(x)
            if n == 0:
                return 0.0
            
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            
            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
            denominator = (sum((x[i] - mean_x) ** 2 for i in range(n)) * 
                          sum((y[i] - mean_y) ** 2 for i in range(n))) ** 0.5
            
            return numerator / denominator if denominator != 0 else 0.0
        
        correlations = {
            "mood_energy": simple_correlation(mood_data, energy_data),
            "mood_stress": simple_correlation(mood_data, stress_data),
            "mood_sleep": simple_correlation(mood_data, sleep_data)
        }
        
        # Generate insights based on correlations
        insights = {}
        
        if correlations["mood_energy"] > 0.3:
            insights["energy"] = "Your mood tends to be higher when your energy levels are good"
        elif correlations["mood_energy"] < -0.3:
            insights["energy"] = "Your mood tends to be lower when your energy levels are low"
        
        if correlations["mood_stress"] < -0.3:
            insights["stress"] = "Higher stress levels appear to negatively impact your mood"
        
        if correlations["mood_sleep"] > 0.3:
            insights["sleep"] = "Good sleep quality seems to positively influence your mood"
        
        return insights
    
    def validate_checkin_data(self, checkin_data: DailyCheckinCreate) -> List[str]:
        """
        Validate check-in data and return list of validation errors.
        
        Args:
            checkin_data: Check-in data to validate.
            
        Returns:
            List of validation error messages.
        """
        errors = []
        
        # Validate mood rating
        if not (1.0 <= checkin_data.mood_rating <= 10.0):
            errors.append("Mood rating must be between 1.0 and 10.0")
        
        # Validate optional ratings
        for field_name, field_value in [
            ("energy_level", checkin_data.energy_level),
            ("stress_level", checkin_data.stress_level),
            ("sleep_quality", checkin_data.sleep_quality),
            ("social_interaction", checkin_data.social_interaction)
        ]:
            if field_value is not None and not (1.0 <= field_value <= 10.0):
                errors.append(f"{field_name} must be between 1.0 and 10.0")
        
        # Validate keywords
        if checkin_data.keywords:
            if len(checkin_data.keywords) > 20:
                errors.append("Maximum 20 keywords allowed")
            
            for keyword in checkin_data.keywords:
                if len(keyword) > 50:
                    errors.append(f"Keyword '{keyword}' is too long (max 50 characters)")
        
        # Validate notes length
        if checkin_data.notes and len(checkin_data.notes) > 2000:
            errors.append("Notes must be 2000 characters or less")
        
        return errors 