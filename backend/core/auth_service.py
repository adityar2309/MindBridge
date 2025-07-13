"""
Authentication service for MindBridge application.

This module provides core business logic for user authentication,
including registration, login, password hashing, and JWT token management.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from models.user import User
from schemas.user_schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from core.exceptions import AuthenticationException, ValidationException, ConflictException


class AuthService:
    """
    Service class for handling authentication operations.
    
    This class provides methods for user registration, login, password
    hashing, and JWT token management.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the authentication service.
        
        Args:
            db: Database session instance.
        """
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    def register_user(self, user_data: UserCreate) -> TokenResponse:
        """
        Register a new user.
        
        Args:
            user_data: User registration data.
            
        Returns:
            Token response with access token and user data.
            
        Raises:
            ConflictException: If user already exists.
            ValidationException: If validation fails.
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictException("User with this email already exists")
        
        # Hash password
        hashed_password = self._hash_password(user_data.password)
        
        # Create new user
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            timezone=user_data.timezone,
            language=user_data.language,
            settings=user_data.settings.dict() if user_data.settings else None
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except Exception as e:
            self.db.rollback()
            raise ValidationException(f"Failed to create user: {str(e)}")
        
        # Generate access token
        access_token = self._create_access_token(data={"sub": str(db_user.user_id)})
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.access_token_expire_minutes * 60,
            user=UserResponse.from_orm(db_user)
        )
    
    def login_user(self, login_data: UserLogin) -> TokenResponse:
        """
        Authenticate user and generate access token.
        
        Args:
            login_data: User login credentials.
            
        Returns:
            Token response with access token and user data.
            
        Raises:
            AuthenticationException: If authentication fails.
        """
        # Get user by email
        user = self.db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise AuthenticationException("Invalid email or password")
        
        # Verify password
        if not self._verify_password(login_data.password, user.password_hash):
            raise AuthenticationException("Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            raise AuthenticationException("User account is deactivated")
        
        # Update last login
        user.last_login = datetime.now()
        self.db.commit()
        
        # Generate access token
        access_token = self._create_access_token(data={"sub": str(user.user_id)})
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.access_token_expire_minutes * 60,
            user=UserResponse.from_orm(user)
        )
    
    def get_current_user(self, token: str) -> User:
        """
        Get current user from JWT token.
        
        Args:
            token: JWT access token.
            
        Returns:
            User instance.
            
        Raises:
            AuthenticationException: If token is invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise AuthenticationException("Invalid token")
        except JWTError:
            raise AuthenticationException("Invalid token")
        
        user = self.db.query(User).filter(User.user_id == int(user_id)).first()
        if user is None:
            raise AuthenticationException("User not found")
        
        if not user.is_active:
            raise AuthenticationException("User account is deactivated")
        
        return user
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token and return payload.
        
        Args:
            token: JWT access token.
            
        Returns:
            Token payload.
            
        Raises:
            AuthenticationException: If token is invalid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise AuthenticationException("Invalid token")
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password.
            
        Returns:
            Hashed password.
        """
        return self.pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password.
            hashed_password: Hashed password.
            
        Returns:
            True if password matches, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def _create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Data to encode in token.
            expires_delta: Token expiration time delta.
            
        Returns:
            JWT access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID.
            current_password: Current password.
            new_password: New password.
            
        Returns:
            True if password changed successfully.
            
        Raises:
            AuthenticationException: If current password is incorrect.
            ValidationException: If user not found.
        """
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValidationException("User not found")
        
        # Verify current password
        if not self._verify_password(current_password, user.password_hash):
            raise AuthenticationException("Current password is incorrect")
        
        # Update password
        user.password_hash = self._hash_password(new_password)
        self.db.commit()
        
        return True
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate user account.
        
        Args:
            user_id: User ID.
            
        Returns:
            True if user deactivated successfully.
            
        Raises:
            ValidationException: If user not found.
        """
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValidationException("User not found")
        
        user.is_active = False
        self.db.commit()
        
        return True 