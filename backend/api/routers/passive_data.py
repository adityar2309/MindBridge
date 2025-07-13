"""
Passive data router for MindBridge backend.

This module provides REST API endpoints for passive data
ingestion, retrieval, and aggregation operations.
"""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Path, BackgroundTasks
from sqlalchemy.orm import Session

from models.database import get_db
from core.passive_data_service import PassiveDataService
from core.exceptions import NotFoundException, ValidationException, DataProcessingException
from schemas.passive_data_schemas import (
    PassiveDataCreate, PassiveDataUpdate, PassiveDataResponse,
    PassiveDataBulkCreate, DataAggregation, HealthMetrics,
    BulkIngestResponse
)


router = APIRouter()


def get_passive_data_service(db: Session = Depends(get_db)) -> PassiveDataService:
    """
    Dependency to get PassiveDataService instance.
    
    Args:
        db: Database session.
        
    Returns:
        PassiveDataService instance.
    """
    return PassiveDataService(db)


@router.post("/", response_model=PassiveDataResponse, status_code=201)
async def ingest_data_point(
    data_point: PassiveDataCreate,
    user_id: int = Query(..., description="User ID"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Ingest a single passive data point.
    
    Args:
        data_point: Passive data point from request body.
        user_id: User ID from query parameter.
        service: PassiveDataService dependency.
        
    Returns:
        Created data point.
        
    Raises:
        HTTPException: If validation fails or duplicate detected.
    """
    try:
        created_point = service.ingest_data_point(user_id, data_point)
        return PassiveDataResponse.from_orm(created_point)
    except ValueError as e:
        raise ValidationException(str(e))


@router.post("/bulk", response_model=BulkIngestResponse, status_code=201)
async def bulk_ingest_data(
    bulk_data: PassiveDataBulkCreate,
    background_tasks: BackgroundTasks,
    user_id: int = Query(..., description="User ID"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Bulk ingest multiple passive data points.
    
    Args:
        bulk_data: Bulk data containing multiple data points.
        user_id: User ID from query parameter.
        background_tasks: Background tasks for processing.
        service: PassiveDataService dependency.
        
    Returns:
        Bulk ingest results with success/error counts.
    """
    try:
        created_points = service.bulk_ingest(user_id, bulk_data)
        
        # Schedule background processing if specified
        if bulk_data.process_async:
            background_tasks.add_task(
                _process_data_points_async,
                [point.data_point_id for point in created_points],
                service
            )
        
        return BulkIngestResponse(
            success_count=len(created_points),
            error_count=len(bulk_data.data_points) - len(created_points),
            total_count=len(bulk_data.data_points),
            created_ids=[point.data_point_id for point in created_points],
            processing_async=bulk_data.process_async
        )
    except Exception as e:
        raise DataProcessingException("bulk_ingest", str(e))


@router.get("/{data_point_id}", response_model=PassiveDataResponse)
async def get_data_point(
    data_point_id: int = Path(..., description="Data point ID"),
    user_id: int = Query(..., description="User ID"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Get a specific data point by ID.
    
    Args:
        data_point_id: Data point ID from path.
        user_id: User ID from query parameter.
        service: PassiveDataService dependency.
        
    Returns:
        Data point information.
        
    Raises:
        HTTPException: If data point not found.
    """
    # Get data points with filter by ID
    data_points = service.get_data_points(user_id, limit=1, offset=0)
    data_point = next((dp for dp in data_points if dp.data_point_id == data_point_id), None)
    
    if not data_point:
        raise NotFoundException("Data point", str(data_point_id))
    
    return PassiveDataResponse.from_orm(data_point)


@router.put("/{data_point_id}", response_model=PassiveDataResponse)
async def update_data_point(
    update_data: PassiveDataUpdate,
    data_point_id: int = Path(..., description="Data point ID"),
    user_id: int = Query(..., description="User ID"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Update an existing data point.
    
    Args:
        update_data: Update data from request body.
        data_point_id: Data point ID from path.
        user_id: User ID from query parameter.
        service: PassiveDataService dependency.
        
    Returns:
        Updated data point.
        
    Raises:
        HTTPException: If data point not found.
    """
    data_point = service.update_data_point(data_point_id, user_id, update_data)
    if not data_point:
        raise NotFoundException("Data point", str(data_point_id))
    
    return PassiveDataResponse.from_orm(data_point)


@router.get("/", response_model=List[PassiveDataResponse])
async def get_data_points(
    user_id: int = Query(..., description="User ID"),
    data_type: Optional[str] = Query(None, description="Filter by data type"),
    source: Optional[str] = Query(None, description="Filter by data source"),
    start_date: Optional[datetime] = Query(None, description="Filter start date"),
    end_date: Optional[datetime] = Query(None, description="Filter end date"),
    limit: int = Query(100, ge=1, le=1000, description="Number of data points to return"),
    offset: int = Query(0, ge=0, description="Number of data points to skip"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Get passive data points with filters and pagination.
    
    Args:
        user_id: User ID from query parameter.
        data_type: Optional data type filter.
        source: Optional source filter.
        start_date: Optional start date filter.
        end_date: Optional end date filter.
        limit: Maximum number of results.
        offset: Number of results to skip.
        service: PassiveDataService dependency.
        
    Returns:
        List of data points.
    """
    data_points = service.get_data_points(
        user_id=user_id,
        data_type=data_type,
        source=source,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    
    return [PassiveDataResponse.from_orm(point) for point in data_points]


@router.get("/aggregate/", response_model=List[DataAggregation])
async def get_aggregated_data(
    user_id: int = Query(..., description="User ID"),
    data_type: str = Query(..., description="Data type to aggregate"),
    period: str = Query("daily", pattern="^(hourly|daily|weekly|monthly)$", description="Aggregation period"),
    start_date: Optional[datetime] = Query(None, description="Start date for aggregation"),
    end_date: Optional[datetime] = Query(None, description="End date for aggregation"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Get aggregated passive data by time period.
    
    Args:
        user_id: User ID from query parameter.
        data_type: Data type to aggregate.
        period: Aggregation period (hourly, daily, weekly, monthly).
        start_date: Optional start date.
        end_date: Optional end date.
        service: PassiveDataService dependency.
        
    Returns:
        List of aggregated data points.
    """
    try:
        return service.aggregate_data(
            user_id=user_id,
            data_type=data_type,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        raise DataProcessingException("data_aggregation", str(e))


@router.get("/health-metrics/", response_model=HealthMetrics)
async def get_health_metrics(
    user_id: int = Query(..., description="User ID"),
    date: Optional[datetime] = Query(None, description="Specific date for metrics"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Get aggregated health metrics for a user.
    
    Args:
        user_id: User ID from query parameter.
        date: Optional specific date for metrics.
        service: PassiveDataService dependency.
        
    Returns:
        Health metrics summary.
    """
    return service.get_health_metrics(user_id, date)


@router.post("/process/{data_point_id}")
async def mark_data_processed(
    data_point_id: int = Path(..., description="Data point ID"),
    user_id: int = Query(..., description="User ID"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Mark a data point as processed.
    
    Args:
        data_point_id: Data point ID from path.
        user_id: User ID from query parameter.
        service: PassiveDataService dependency.
        
    Returns:
        Success message.
    """
    processed_count = service.mark_processed([data_point_id])
    
    if processed_count == 0:
        raise NotFoundException("Data point", str(data_point_id))
    
    return {"message": "Data point marked as processed", "data_point_id": data_point_id}


@router.get("/unprocessed/", response_model=List[PassiveDataResponse])
async def get_unprocessed_data(
    limit: int = Query(1000, ge=1, le=10000, description="Maximum number of unprocessed items"),
    service: PassiveDataService = Depends(get_passive_data_service)
):
    """
    Get unprocessed data points for batch processing.
    
    Args:
        limit: Maximum number of unprocessed items to return.
        service: PassiveDataService dependency.
        
    Returns:
        List of unprocessed data points.
    """
    unprocessed_points = service.get_unprocessed_data(limit)
    return [PassiveDataResponse.from_orm(point) for point in unprocessed_points]


async def _process_data_points_async(data_point_ids: List[int], service: PassiveDataService):
    """
    Background task to process data points asynchronously.
    
    Args:
        data_point_ids: List of data point IDs to process.
        service: PassiveDataService instance.
    """
    try:
        # Mark data points as processed
        processed_count = service.mark_processed(data_point_ids)
        print(f"Processed {processed_count} data points in background")
    except Exception as e:
        print(f"Error processing data points in background: {str(e)}") 