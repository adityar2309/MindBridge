"""
Authentication router for MindBridge backend.

This module provides REST API endpoints for user authentication,
including registration, login, and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from models.database import get_db
from core.auth_service import AuthService
from core.exceptions import AuthenticationException, ValidationException, ConflictException
from schemas.user_schemas import (
    UserCreate, UserLogin, TokenResponse, UserResponse,
    PasswordChange
)


router = APIRouter()
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """
    Dependency to get AuthService instance.
    
    Args:
        db: Database session.
        
    Returns:
        AuthService instance.
    """
    return AuthService(db)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service)
):
    """
    Dependency to get current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials.
        service: AuthService dependency.
        
    Returns:
        Current user instance.
        
    Raises:
        HTTPException: If authentication fails.
    """
    try:
        return service.get_current_user(credentials.credentials)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data from request body.
        service: AuthService dependency.
        
    Returns:
        Token response with access token and user data.
        
    Raises:
        HTTPException: If registration fails.
    """
    try:
        return service.register_user(user_data)
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user and generate access token.
    
    Args:
        login_data: User login credentials from request body.
        service: AuthService dependency.
        
    Returns:
        Token response with access token and user data.
        
    Raises:
        HTTPException: If authentication fails.
    """
    try:
        return service.login_user(login_data)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user = Depends(get_current_user)
):
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user dependency.
        
    Returns:
        User profile data.
    """
    return UserResponse.model_validate(current_user)


@router.post("/verify-token")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_auth_service)
):
    """
    Verify JWT token validity.
    
    Args:
        credentials: HTTP authorization credentials.
        service: AuthService dependency.
        
    Returns:
        Token verification result.
        
    Raises:
        HTTPException: If token is invalid.
    """
    try:
        payload = service.verify_token(credentials.credentials)
        return {
            "valid": True,
            "user_id": payload.get("sub"),
            "expires": payload.get("exp")
        }
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
):
    """
    Change user password.
    
    Args:
        password_data: Password change data from request body.
        current_user: Current authenticated user dependency.
        service: AuthService dependency.
        
    Returns:
        Success message.
        
    Raises:
        HTTPException: If password change fails.
    """
    try:
        service.change_password(
            current_user.user_id,
            password_data.current_password,
            password_data.new_password
        )
        return {"message": "Password changed successfully"}
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.post("/logout")
async def logout(current_user = Depends(get_current_user)):
    """
    Logout current user.
    
    Note: With JWT tokens, logout is typically handled client-side
    by removing the token. This endpoint exists for consistency
    and potential future token blacklisting.
    
    Args:
        current_user: Current authenticated user dependency.
        
    Returns:
        Success message.
    """
    return {"message": "Logged out successfully"} 
