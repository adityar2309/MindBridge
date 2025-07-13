"""
Test utilities and helper functions for MindBridge backend tests.

This module provides common testing utilities, mock data generators,
and helper functions used across the test suite.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from faker import Faker

fake = Faker()


class TestDataGenerator:
    """Generate realistic test data for various entities."""
    
    @staticmethod
    def random_user_data() -> Dict[str, Any]:
        """Generate random user data."""
        return {
            "username": fake.user_name(),
            "email": fake.email(),
            "full_name": fake.name(),
            "age": random.randint(18, 80),
            "gender": random.choice(["male", "female", "non-binary"]),
            "timezone": fake.timezone(),
            "language_preference": random.choice(["en", "es", "fr", "de"])
        }
    
    @staticmethod
    def random_checkin_data() -> Dict[str, Any]:
        """Generate random check-in data."""
        return {
            "mood_rating": random.randint(1, 10),
            "energy_level": random.randint(1, 10),
            "stress_level": random.randint(1, 10),
            "sleep_hours": round(random.uniform(4.0, 12.0), 1),
            "sleep_quality": random.randint(1, 10),
            "notes": fake.text(max_nb_chars=200),
            "activities": random.sample([
                "exercise", "reading", "cooking", "socializing", 
                "work", "meditation", "music", "gaming"
            ], k=random.randint(1, 4)),
            "mood_triggers": random.sample([
                "stress", "work", "relationships", "weather", 
                "health", "finances", "family"
            ], k=random.randint(0, 3)),
            "location": random.choice(["home", "work", "gym", "outdoors"]),
            "weather": random.choice(["sunny", "cloudy", "rainy", "snowy"])
        }
    
    @staticmethod
    def random_passive_data() -> Dict[str, Any]:
        """Generate random passive data point."""
        data_types = {
            "heart_rate": {"value": random.randint(60, 120), "unit": "bpm"},
            "steps": {"value": random.randint(1000, 20000), "unit": "steps"},
            "sleep": {"value": round(random.uniform(4.0, 12.0), 1), "unit": "hours"},
            "activity": {"value": random.randint(0, 240), "unit": "minutes"}
        }
        
        data_type = random.choice(list(data_types.keys()))
        data_info = data_types[data_type]
        
        return {
            "data_type": data_type,
            "value": data_info["value"],
            "unit": data_info["unit"],
            "source": random.choice(["fitbit", "apple_watch", "samsung_health"]),
            "metadata": {"confidence": round(random.uniform(0.7, 1.0), 2)},
            "location": {
                "lat": round(random.uniform(-90, 90), 6),
                "lng": round(random.uniform(-180, 180), 6)
            }
        }
    
    @staticmethod
    def random_quiz_responses() -> Dict[str, Any]:
        """Generate random quiz responses."""
        quiz_types = {
            "DASS21": 21,
            "PHQ9": 9,
            "GAD7": 7
        }
        
        quiz_type = random.choice(list(quiz_types.keys()))
        num_questions = quiz_types[quiz_type]
        
        responses = {}
        for i in range(1, num_questions + 1):
            responses[f"q{i}"] = random.randint(0, 3)
        
        return {
            "quiz_type": quiz_type,
            "responses": responses
        }
    
    @staticmethod
    def random_date_range(days_back: int = 30) -> List[datetime]:
        """Generate random dates within a range."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        dates = []
        current_date = start_date
        while current_date <= end_date:
            if random.random() < 0.7:  # 70% chance of having data for each day
                dates.append(current_date)
            current_date += timedelta(days=1)
        
        return dates


class APITestHelpers:
    """Helper functions for API testing."""
    
    @staticmethod
    def assert_response_structure(response_data: Dict, expected_keys: List[str]):
        """Assert that response contains expected keys."""
        for key in expected_keys:
            assert key in response_data, f"Missing key '{key}' in response"
    
    @staticmethod
    def assert_error_response(response_data: Dict, expected_status: int):
        """Assert error response structure."""
        assert "error" in response_data
        assert "message" in response_data
        assert response_data.get("status_code") == expected_status
    
    @staticmethod
    def assert_pagination_response(response_data: Dict):
        """Assert pagination response structure."""
        expected_keys = ["items", "total", "page", "size", "pages"]
        APITestHelpers.assert_response_structure(response_data, expected_keys)
        
        assert isinstance(response_data["items"], list)
        assert isinstance(response_data["total"], int)
        assert isinstance(response_data["page"], int)
        assert isinstance(response_data["size"], int)
        assert isinstance(response_data["pages"], int)


class DatabaseTestHelpers:
    """Helper functions for database testing."""
    
    @staticmethod
    def create_test_users(session, count: int = 5) -> List:
        """Create multiple test users."""
        from backend.models.user import User
        
        users = []
        for _ in range(count):
            user_data = TestDataGenerator.random_user_data()
            user = User(**user_data)
            session.add(user)
            users.append(user)
        
        session.commit()
        for user in users:
            session.refresh(user)
        
        return users
    
    @staticmethod
    def create_test_checkins(session, user, count: int = 10) -> List:
        """Create multiple test check-ins for a user."""
        from backend.models.checkin import DailyCheckin
        
        checkins = []
        dates = TestDataGenerator.random_date_range(count)
        
        for date in dates:
            checkin_data = TestDataGenerator.random_checkin_data()
            checkin_data["user_id"] = user.id
            checkin_data["created_at"] = date
            
            checkin = DailyCheckin(**checkin_data)
            session.add(checkin)
            checkins.append(checkin)
        
        session.commit()
        for checkin in checkins:
            session.refresh(checkin)
        
        return checkins


class MockServices:
    """Mock external services for testing."""
    
    @staticmethod
    def mock_ai_service_response():
        """Mock AI service response."""
        return {
            "mood_prediction": round(random.uniform(1.0, 10.0), 1),
            "confidence": round(random.uniform(0.6, 1.0), 2),
            "insights": [
                fake.sentence() for _ in range(random.randint(1, 3))
            ],
            "recommendations": [
                fake.sentence() for _ in range(random.randint(1, 3))
            ]
        }
    
    @staticmethod
    def mock_notification_service():
        """Mock notification service."""
        return {"sent": True, "message_id": fake.uuid4()}
    
    @staticmethod
    def mock_external_api_error():
        """Mock external API error response."""
        return {
            "error": "External service unavailable",
            "status_code": 503,
            "retry_after": 30
        }


def assert_datetime_recent(dt: datetime, tolerance_seconds: int = 60):
    """Assert that a datetime is recent (within tolerance)."""
    now = datetime.now()
    if dt.tzinfo is None and now.tzinfo is not None:
        now = now.replace(tzinfo=None)
    elif dt.tzinfo is not None and now.tzinfo is None:
        dt = dt.replace(tzinfo=None)
    
    diff = abs((now - dt).total_seconds())
    assert diff <= tolerance_seconds, f"Datetime {dt} is not recent (diff: {diff}s)"


def assert_valid_uuid(uuid_string: str):
    """Assert that a string is a valid UUID."""
    import uuid
    try:
        uuid.UUID(uuid_string)
    except ValueError:
        pytest.fail(f"'{uuid_string}' is not a valid UUID")


def create_mock_request_data(**kwargs) -> Dict[str, Any]:
    """Create mock request data with default values."""
    defaults = {
        "timestamp": datetime.now().isoformat(),
        "request_id": fake.uuid4(),
        "user_agent": fake.user_agent(),
        "ip_address": fake.ipv4()
    }
    defaults.update(kwargs)
    return defaults 