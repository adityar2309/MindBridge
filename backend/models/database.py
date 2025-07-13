"""
Database configuration and base model setup for MindBridge.

This module provides the database session management and base model
configuration for the MindBridge application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# Database URL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://mindbridge:mindbridge@localhost/mindbridge"
)

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base model class
Base = declarative_base()


def get_db() -> Generator:
    """
    Get database session.
    
    Yields:
        Database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.
    
    This function should be called during application startup
    to ensure all tables are created.
    """
    Base.metadata.create_all(bind=engine) 