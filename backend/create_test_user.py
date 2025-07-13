#!/usr/bin/env python3
"""
Script to create a test user for development and testing purposes.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from models.database import Base
from models.user import User

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mindbridge_dev")

# Create database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    """Create a test user in the database."""
    
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("✅ Test user already exists!")
            print(f"   Email: {existing_user.email}")
            print(f"   User ID: {existing_user.user_id}")
            return existing_user
        
        # Hash password
        hashed_password = pwd_context.hash("Password1")
        
        # Create default settings
        default_settings = {
            "notifications": {
                "daily_reminder": True,
                "weekly_summary": True,
                "mood_alerts": True,
                "reminder_time": "09:00"
            },
            "privacy": {
                "data_sharing": False,
                "anonymous_analytics": True
            },
            "ui": {
                "theme": "auto",
                "font_size": "medium",
                "animations": True
            }
        }
        
        # Create new user
        test_user = User(
            name="Test User",
            email="test@example.com",
            password_hash=hashed_password,
            timezone="UTC",
            language="en",
            settings=default_settings,
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print(f"   Email: {test_user.email}")
        print(f"   User ID: {test_user.user_id}")
        print(f"   Name: {test_user.name}")
        print("   Password: Password1")
        
        return test_user
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test user: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creating test user for MindBridge...")
    create_test_user()
    print("✨ Done!") 