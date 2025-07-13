"""
Custom exception classes for MindBridge application.

This module defines custom exceptions with standardized error handling,
logging, and response formatting.
"""

from typing import Optional, Dict, Any


class MindBridgeException(Exception):
    """
    Base exception class for MindBridge application.
    
    Provides standardized error handling with status codes,
    error codes, and detailed error information.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize MindBridge exception.
        
        Args:
            message: Human-readable error message.
            error_code: Machine-readable error code.
            status_code: HTTP status code.
            details: Additional error details.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class ValidationException(MindBridgeException):
    """Exception raised for data validation errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class NotFoundException(MindBridgeException):
    """Exception raised when a resource is not found."""
    
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' not found",
            error_code="RESOURCE_NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": identifier}
        )


class ConflictException(MindBridgeException):
    """Exception raised for resource conflicts."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="RESOURCE_CONFLICT",
            status_code=409,
            details=details
        )


class AuthenticationException(MindBridgeException):
    """Exception raised for authentication errors."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401
        )


class AuthorizationException(MindBridgeException):
    """Exception raised for authorization errors."""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403
        )


class RateLimitException(MindBridgeException):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429
        )


class ServiceUnavailableException(MindBridgeException):
    """Exception raised when a service is unavailable."""
    
    def __init__(self, service: str, message: Optional[str] = None):
        default_message = f"{service} service is currently unavailable"
        super().__init__(
            message=message or default_message,
            error_code="SERVICE_UNAVAILABLE",
            status_code=503,
            details={"service": service}
        )


class DataProcessingException(MindBridgeException):
    """Exception raised for data processing errors."""
    
    def __init__(self, operation: str, message: Optional[str] = None):
        default_message = f"Error processing data in operation: {operation}"
        super().__init__(
            message=message or default_message,
            error_code="DATA_PROCESSING_ERROR",
            status_code=422,
            details={"operation": operation}
        ) 