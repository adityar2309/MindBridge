"""
Metrics router for Prometheus monitoring.

This module provides endpoints for Prometheus to scrape
application metrics and health information.
"""

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse

from core.metrics import get_metrics, CONTENT_TYPE_LATEST


router = APIRouter()


@router.get("/metrics")
async def prometheus_metrics():
    """
    Endpoint for Prometheus metrics scraping.
    
    Returns:
        Prometheus metrics in the correct format.
    """
    metrics_data = get_metrics()
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST
    )


@router.get("/metrics/health")
async def metrics_health():
    """
    Health check endpoint specifically for metrics collection.
    
    Returns:
        Simple health status for metrics monitoring.
    """
    return PlainTextResponse("metrics_ok") 
