#!/usr/bin/env python3
"""
Simple Test Demonstration for MindBridge Testing Infrastructure
Shows the testing framework in action with basic functionality.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import json

# Simple test for basic functionality
def test_basic_functionality():
    """Test basic Python functionality to verify testing framework."""
    # Test basic calculations
    assert 2 + 2 == 4
    assert 10 * 5 == 50
    
    # Test string operations
    test_string = "MindBridge Health Tracker"
    assert "Health" in test_string
    assert test_string.startswith("MindBridge")
    
    print("✅ Basic functionality tests passed!")

def test_datetime_operations():
    """Test datetime operations commonly used in health tracking."""
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    tomorrow = now + timedelta(days=1)
    
    # Test date comparisons
    assert yesterday < now < tomorrow
    assert (tomorrow - yesterday).days == 2
    
    # Test date formatting
    date_str = now.strftime("%Y-%m-%d")
    assert len(date_str) == 10
    assert "-" in date_str
    
    print("✅ Datetime operations tests passed!")

def test_data_structures():
    """Test data structures used in health tracking."""
    # Test mood tracking data
    mood_entry = {
        "timestamp": datetime.now().isoformat(),
        "mood_score": 7,
        "anxiety_level": 3,
        "stress_level": 4,
        "notes": "Feeling good today"
    }
    
    # Validate structure
    assert isinstance(mood_entry["mood_score"], int)
    assert 1 <= mood_entry["mood_score"] <= 10
    assert mood_entry["notes"] is not None
    
    # Test list operations
    mood_history = [mood_entry]
    mood_history.append({
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
        "mood_score": 6,
        "anxiety_level": 4,
        "stress_level": 5,
        "notes": "Moderate day"
    })
    
    assert len(mood_history) == 2
    assert all("mood_score" in entry for entry in mood_history)
    
    print("✅ Data structure tests passed!")

@pytest.mark.asyncio
async def test_async_functionality():
    """Test async functionality for API operations."""
    
    async def mock_api_call(delay=0.1):
        """Mock API call with delay."""
        await asyncio.sleep(delay)
        return {"status": "success", "data": "mock_response"}
    
    # Test async call
    result = await mock_api_call()
    assert result["status"] == "success"
    assert "data" in result
    
    # Test multiple async calls
    tasks = [mock_api_call(0.05) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 3
    assert all(r["status"] == "success" for r in results)
    
    print("✅ Async functionality tests passed!")

def test_mock_external_service():
    """Test mocking external services like AI or health APIs."""
    
    # Mock AI service
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "insights": "Based on your mood pattern, consider meditation",
            "confidence": 0.85
        }
        mock_post.return_value.status_code = 200
        
        # Simulate AI service call
        import requests
        response = requests.post("https://api.ai-service.com/analyze", 
                               json={"mood_data": [7, 6, 8, 5]})
        
        result = response.json()
        assert "insights" in result
        assert result["confidence"] > 0.5
        assert mock_post.called
    
    print("✅ External service mocking tests passed!")

def test_health_data_validation():
    """Test health data validation logic."""
    
    def validate_mood_score(score):
        """Validate mood score range."""
        return isinstance(score, int) and 1 <= score <= 10
    
    def validate_checkin_data(data):
        """Validate check-in data structure."""
        required_fields = ["timestamp", "mood_score", "anxiety_level"]
        return all(field in data for field in required_fields)
    
    # Test valid data
    valid_checkin = {
        "timestamp": datetime.now().isoformat(),
        "mood_score": 7,
        "anxiety_level": 3,
        "stress_level": 4
    }
    
    assert validate_mood_score(7)
    assert not validate_mood_score(11)
    assert not validate_mood_score("high")
    assert validate_checkin_data(valid_checkin)
    
    # Test invalid data
    invalid_checkin = {"mood_score": 7}  # Missing required fields
    assert not validate_checkin_data(invalid_checkin)
    
    print("✅ Health data validation tests passed!")

class TestHealthMetrics:
    """Test class for health metrics calculations."""
    
    def test_mood_trends(self):
        """Test mood trend calculations."""
        mood_data = [6, 7, 5, 8, 7, 9, 6]
        
        # Calculate average
        average_mood = sum(mood_data) / len(mood_data)
        assert 6.0 <= average_mood <= 8.0
        
        # Calculate trend (simplified)
        trend = mood_data[-1] - mood_data[0]  # Last vs first
        assert isinstance(trend, int)
        
        print(f"✅ Average mood: {average_mood:.1f}, Trend: {trend}")
    
    def test_wellness_score(self):
        """Test overall wellness score calculation."""
        metrics = {
            "mood": 7,
            "anxiety": 3,  # Lower is better
            "stress": 4,   # Lower is better
            "sleep_quality": 8,
            "energy_level": 6
        }
        
        # Calculate wellness score (simplified formula)
        positive_metrics = metrics["mood"] + metrics["sleep_quality"] + metrics["energy_level"]
        negative_metrics = metrics["anxiety"] + metrics["stress"]
        wellness_score = (positive_metrics - negative_metrics) / 3
        
        assert 0 <= wellness_score <= 10
        print(f"✅ Wellness score: {wellness_score:.1f}")

if __name__ == "__main__":
    print("🧪 MindBridge Testing Infrastructure Demo")
    print("=" * 50)
    
    # Run basic tests
    test_basic_functionality()
    test_datetime_operations()
    test_data_structures()
    test_mock_external_service()
    test_health_data_validation()
    
    # Run class-based tests
    health_test = TestHealthMetrics()
    health_test.test_mood_trends()
    health_test.test_wellness_score()
    
    print("\n🎉 All demonstration tests passed!")
    print("Testing infrastructure is working correctly.")
    print("\nTo run with pytest:")
    print("python -m pytest test_demo_simple.py -v") 