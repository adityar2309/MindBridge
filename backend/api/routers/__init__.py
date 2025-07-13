"""
API routers for MindBridge backend services.

This module contains FastAPI router definitions for different
service endpoints.
"""

from .auth import router as auth_router
from .checkin import router as checkin_router
from .passive_data import router as passive_data_router
from .health import router as health_router
from .metrics import router as metrics_router

__all__ = ["auth_router", "checkin_router", "passive_data_router", "health_router", "metrics_router"] 