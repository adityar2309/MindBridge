"""
Pytest configuration and fixtures for MindBridge backend tests.

This module provides shared fixtures, test database setup, and common
test utilities for the entire test suite.
"""

import asyncio
import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.api.main import create_app
from backend.models.database import Base, get_db
from backend.models.user import User
from backend.models.checkin import DailyCheckin
from backend.models.passive_data import PassiveDataPoint
from backend.models.quiz import QuizResponse
from backend.models.ai_insights import AIMoodInsight


# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine with in-memory SQLite
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db():
    """Create and clean up test database for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Provide the database session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def app(test_db):
    """Create FastAPI app instance for testing."""
    app = create_app()
    
    # Override database dependency
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    return app


@pytest.fixture(scope="function")
def client(app) -> TestClient:
    """Create test client for synchronous tests."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client for async tests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "age": 25,
        "gender": "non-binary",
        "timezone": "UTC",
        "language_preference": "en"
    }


@pytest.fixture
def sample_checkin_data():
    """Sample check-in data for testing."""
    return {
        "mood_rating": 7,
        "energy_level": 6,
        "stress_level": 4,
        "sleep_hours": 8.0,
        "sleep_quality": 8,
        "notes": "Feeling good today",
        "activities": ["exercise", "reading"],
        "mood_triggers": [],
        "location": "home",
        "weather": "sunny"
    }


@pytest.fixture
def sample_passive_data():
    """Sample passive data for testing."""
    return {
        "data_type": "heart_rate",
        "value": 72.5,
        "unit": "bpm",
        "source": "fitbit",
        "metadata": {"confidence": 0.95},
        "location": {"lat": 40.7128, "lng": -74.0060}
    }


@pytest.fixture
def sample_quiz_data():
    """Sample quiz response data for testing."""
    return {
        "quiz_type": "DASS21",
        "responses": {
            "q1": 2,
            "q2": 1,
            "q3": 3,
            "q4": 0,
            "q5": 2
        }
    }


@pytest.fixture
def auth_headers():
    """Mock authentication headers for testing."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def mock_ai_response():
    """Mock AI service response for testing."""
    return {
        "mood_prediction": 7.2,
        "confidence": 0.85,
        "insights": ["You seem to be doing well today"],
        "recommendations": ["Continue your current routine"]
    }


# Database fixtures for creating test data
@pytest.fixture
def test_user(test_db, sample_user_data):
    """Create a test user in the database."""
    user = User(**sample_user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_checkin(test_db, test_user, sample_checkin_data):
    """Create a test check-in in the database."""
    checkin_data = sample_checkin_data.copy()
    checkin_data["user_id"] = test_user.id
    checkin = DailyCheckin(**checkin_data)
    test_db.add(checkin)
    test_db.commit()
    test_db.refresh(checkin)
    return checkin


@pytest.fixture
def test_passive_data(test_db, test_user, sample_passive_data):
    """Create test passive data in the database."""
    passive_data = sample_passive_data.copy()
    passive_data["user_id"] = test_user.id
    data_point = PassiveDataPoint(**passive_data)
    test_db.add(data_point)
    test_db.commit()
    test_db.refresh(data_point)
    return data_point


# Environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ["TESTING"] = "true"
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    yield
    # Cleanup
    if "TESTING" in os.environ:
        del os.environ["TESTING"] 