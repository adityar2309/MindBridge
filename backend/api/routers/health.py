"""
Health check router for MindBridge backend.

This module provides health check endpoints for monitoring
application status and dependencies.
"""

import os
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from models.database import get_db
from schemas.user_schemas import HealthCheckResponse


router = APIRouter()


@router.get("/", response_model=HealthCheckResponse)
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        Health status with timestamp and basic information.
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )


@router.get("/ready", response_model=HealthCheckResponse)
async def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check endpoint for Kubernetes.
    
    Checks if the application is ready to serve requests
    by verifying database connectivity.
    
    Args:
        db: Database session dependency.
        
    Returns:
        Readiness status with dependencies check.
        
    Raises:
        HTTPException: If application is not ready.
    """
    checks = {}
    
    # Database connectivity check
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        raise HTTPException(
            status_code=503,
            detail="Database connectivity check failed"
        )
    
    return HealthCheckResponse(
        status="ready",
        timestamp=datetime.now(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development"),
        details={"checks": checks}
    )


@router.get("/live", response_model=HealthCheckResponse)
async def liveness_check():
    """
    Liveness check endpoint for Kubernetes.
    
    Simple check to verify the application process is alive.
    
    Returns:
        Liveness status.
    """
    return HealthCheckResponse(
        status="alive",
        timestamp=datetime.now(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Detailed health check with comprehensive system information.
    
    Args:
        db: Database session dependency.
        
    Returns:
        Detailed health information including system metrics.
    """
    import psutil
    import sys
    
    checks = {}
    
    # Database check
    try:
        result = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        checks["database"] = {
            "status": "healthy",
            "user_count": result,
            "connection_pool": "active"
        }
    except Exception as e:
        checks["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # System metrics
    checks["system"] = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "python_version": sys.version,
        "process_id": os.getpid()
    }
    
    # Environment info
    checks["environment"] = {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "database_url": "configured" if os.getenv("DATABASE_URL") else "not_configured"
    }
    
    overall_status = "healthy" if all(
        check.get("status") == "healthy" if isinstance(check, dict) else True
        for check in checks.values()
    ) else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "checks": checks
    } 