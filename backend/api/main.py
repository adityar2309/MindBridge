"""
Main FastAPI application for MindBridge backend.

This module sets up the main FastAPI application with middleware,
CORS, error handling, and routing configuration.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog

from .routers import checkin_router, passive_data_router, health_router, metrics_router
from ..models.database import engine, Base
from ..core.exceptions import MindBridgeException
from ..core.metrics import metrics_collector


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Manages startup and shutdown operations for the FastAPI application.
    """
    # Startup
    logger.info("Starting MindBridge backend application")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down MindBridge backend application")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance.
    """
    # Application configuration
    app_config = {
        "title": "MindBridge Backend API",
        "description": "Backend microservices for MindBridge Mood & Mental Health Tracker",
        "version": "1.0.0",
        "docs_url": "/docs" if os.getenv("ENVIRONMENT", "development") != "production" else None,
        "redoc_url": "/redoc" if os.getenv("ENVIRONMENT", "development") != "production" else None,
        "lifespan": lifespan
    }
    
    app = FastAPI(**app_config)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    trusted_hosts = os.getenv("TRUSTED_HOSTS", "*").split(",")
    if trusted_hosts != ["*"]:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)
    
    # Metrics middleware
    app.middleware("http")(metrics_collector.middleware)
    
    # Include routers
    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(metrics_router, tags=["monitoring"])
    app.include_router(checkin_router, prefix="/api/v1/checkins", tags=["checkins"])
    app.include_router(passive_data_router, prefix="/api/v1/passive-data", tags=["passive-data"])
    
    # Exception handlers
    @app.exception_handler(MindBridgeException)
    async def mindbridge_exception_handler(request: Request, exc: MindBridgeException):
        """Handle custom MindBridge exceptions."""
        logger.error(
            "MindBridge exception occurred",
            error_type=type(exc).__name__,
            error_message=str(exc),
            path=request.url.path
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        logger.warning(
            "Request validation error",
            errors=exc.errors(),
            path=request.url.path
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.warning(
            "HTTP exception occurred",
            status_code=exc.status_code,
            detail=exc.detail,
            path=request.url.path
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP_ERROR",
                "message": exc.detail,
                "details": None
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(
            "Unexpected exception occurred",
            error_type=type(exc).__name__,
            error_message=str(exc),
            path=request.url.path,
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": None if os.getenv("ENVIRONMENT") == "production" else str(exc)
            }
        )
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests."""
        start_time = request.state.start_time = structlog.processors.TimeStamper()._stamper()
        
        logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
            client_ip=request.client.host if request.client else None
        )
        
        response = await call_next(request)
        
        process_time = structlog.processors.TimeStamper()._stamper() - start_time
        
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=process_time
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    return app


# Create the application instance
app = create_app() 