"""
Check-in router for MindBridge backend.

This module provides REST API endpoints for daily check-in
operations including creation, updates, and analytics.
"""

from typing import List, Optional
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from models.database import get_db
from core.checkin_service import CheckinService
from core.exceptions import NotFoundException, ConflictException, ValidationException
from schemas.checkin_schemas import (
    DailyCheckinCreate, DailyCheckinUpdate, DailyCheckinResponse,
    MoodAnalytics, CheckinStreak, MoodTrend
)


router = APIRouter()


def get_checkin_service(db: Session = Depends(get_db)) -> CheckinService:
    """
    Dependency to get CheckinService instance.
    
    Args:
        db: Database session.
        
    Returns:
        CheckinService instance.
    """
    return CheckinService(db)


@router.post("/", response_model=DailyCheckinResponse, status_code=201)
async def create_checkin(
    checkin_data: DailyCheckinCreate,
    user_id: int = Query(..., description="User ID"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Create a new daily check-in.
    
    Args:
        checkin_data: Check-in data from request body.
        user_id: User ID from query parameter.
        service: CheckinService dependency.
        
    Returns:
        Created check-in data.
        
    Raises:
        HTTPException: If validation fails or duplicate exists.
    """
    try:
        checkin = service.create_checkin(user_id, checkin_data)
        return DailyCheckinResponse.model_validate(checkin)
    except ValueError as e:
        if "already has a check-in" in str(e):
            raise ConflictException(str(e))
        else:
            raise ValidationException(str(e))


@router.get("/{checkin_id}", response_model=DailyCheckinResponse)
async def get_checkin(
    checkin_id: int = Path(..., description="Check-in ID"),
    user_id: int = Query(..., description="User ID"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Get a specific check-in by ID.
    
    Args:
        checkin_id: Check-in ID from path.
        user_id: User ID from query parameter.
        service: CheckinService dependency.
        
    Returns:
        Check-in data.
        
    Raises:
        HTTPException: If check-in not found.
    """
    checkin = service.get_checkin_by_id(checkin_id, user_id)
    if not checkin:
        raise NotFoundException("Check-in", str(checkin_id))
    
    return DailyCheckinResponse.model_validate(checkin)


@router.put("/{checkin_id}", response_model=DailyCheckinResponse)
async def update_checkin(
    update_data: DailyCheckinUpdate,
    checkin_id: int = Path(..., description="Check-in ID"),
    user_id: int = Query(..., description="User ID"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Update an existing check-in.
    
    Args:
        update_data: Update data from request body.
        checkin_id: Check-in ID from path.
        user_id: User ID from query parameter.
        service: CheckinService dependency.
        
    Returns:
        Updated check-in data.
        
    Raises:
        HTTPException: If check-in not found.
    """
    checkin = service.update_checkin(checkin_id, user_id, update_data)
    if not checkin:
        raise NotFoundException("Check-in", str(checkin_id))
    
    return DailyCheckinResponse.model_validate(checkin)


@router.get("/", response_model=List[DailyCheckinResponse])
async def get_user_checkins(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(30, ge=1, le=100, description="Number of check-ins to return"),
    offset: int = Query(0, ge=0, description="Number of check-ins to skip"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Get user's check-ins with pagination.
    
    Args:
        user_id: User ID from query parameter.
        limit: Maximum number of results.
        offset: Number of results to skip.
        service: CheckinService dependency.
        
    Returns:
        List of check-ins.
    """
    checkins = service.get_user_checkins(user_id, limit, offset)
    return [DailyCheckinResponse.model_validate(checkin) for checkin in checkins]


@router.get("/today/", response_model=Optional[DailyCheckinResponse])
async def get_todays_checkin(
    user_id: int = Query(..., description="User ID"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Get today's check-in for a user.
    
    Args:
        user_id: User ID from query parameter.
        service: CheckinService dependency.
        
    Returns:
        Today's check-in data or None if not found.
    """
    checkin = service.get_todays_checkin(user_id)
    if checkin:
        return DailyCheckinResponse.model_validate(checkin)
    return None


@router.get("/streak/", response_model=CheckinStreak)
async def get_checkin_streak(
    user_id: int = Query(..., description="User ID"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Get user's check-in streak information.
    
    Args:
        user_id: User ID from query parameter.
        service: CheckinService dependency.
        
    Returns:
        Check-in streak data.
    """
    return service.get_checkin_streak(user_id)


@router.get("/analytics/", response_model=MoodAnalytics)
async def get_mood_analytics(
    user_id: int = Query(..., description="User ID"),
    period: str = Query("monthly", pattern="^(daily|weekly|monthly)$", description="Analysis period"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Get mood analytics for a user.
    
    Args:
        user_id: User ID from query parameter.
        period: Analysis period (daily, weekly, monthly).
        service: CheckinService dependency.
        
    Returns:
        Mood analytics data.
    """
    return service.get_mood_analytics(user_id, period)


@router.get("/trends/", response_model=List[MoodTrend])
async def get_mood_trends(
    user_id: int = Query(..., description="User ID"),
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    service: CheckinService = Depends(get_checkin_service)
):
    """
    Get mood trends over a specified period.
    
    Args:
        user_id: User ID from query parameter.
        days: Number of days to analyze.
        service: CheckinService dependency.
        
    Returns:
        List of mood trend data points.
    """
    analytics = service.get_mood_analytics(user_id, "daily")
    # Extract trend data from analytics
    return analytics.trends if hasattr(analytics, 'trends') else [] 
