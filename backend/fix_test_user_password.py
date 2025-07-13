#!/usr/bin/env python3
"""
Script to fix the test user's password hash.
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

def fix_test_user_password():
    """Fix the test user's password hash."""
    
    # Create session
    db = SessionLocal()
    
    try:
        # Get the test user
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("❌ Test user not found!")
            return
        
        # Update password hash
        new_password_hash = pwd_context.hash("Password1")
        user.password_hash = new_password_hash
        
        db.commit()
        db.refresh(user)
        
        # Verify the password now works
        verification_result = pwd_context.verify("Password1", user.password_hash)
        
        print("✅ Test user password updated successfully!")
        print(f"   Email: {user.email}")
        print(f"   User ID: {user.user_id}")
        print(f"   Password verification: {verification_result}")
        
        return user
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error fixing test user password: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Fixing test user password...")
    fix_test_user_password()
    print("✨ Done!") 