"""
Unit tests for check-in endpoints.

Tests for the daily mood check-in functionality including
creation, retrieval, updating, and analysis of check-in data.
"""

import pytest
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from tests.utils import APITestHelpers, TestDataGenerator, assert_datetime_recent


@pytest.mark.unit
@pytest.mark.api
class TestCheckinEndpoints:
    """Test suite for check-in API endpoints."""
    
    def test_create_checkin_success(self, client: TestClient, test_user, sample_checkin_data):
        """
        Test successful check-in creation.
        
        Expected:
        - Status 201
        - Check-in data returned
        - Proper validation
        """
        checkin_data = sample_checkin_data.copy()
        checkin_data["user_id"] = test_user.id
        
        response = client.post("/api/checkins/", json=checkin_data)
        
        assert response.status_code == 201
        data = response.json()
        
        expected_keys = [
            "id", "user_id", "mood_rating", "energy_level", 
            "stress_level", "sleep_hours", "created_at"
        ]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert data["user_id"] == test_user.id
        assert data["mood_rating"] == checkin_data["mood_rating"]
        assert data["energy_level"] == checkin_data["energy_level"]
        assert_datetime_recent(datetime.fromisoformat(data["created_at"]))
    
    def test_create_checkin_validation_errors(self, client: TestClient, test_user):
        """
        Test check-in creation with validation errors.
        
        Expected:
        - Status 422
        - Validation error details
        """
        # Invalid mood rating (out of range)
        invalid_data = {
            "user_id": test_user.id,
            "mood_rating": 15,  # Invalid: should be 1-10
            "energy_level": 5,
            "stress_level": 3
        }
        
        response = client.post("/api/checkins/", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_create_checkin_missing_required_fields(self, client: TestClient, test_user):
        """
        Test check-in creation with missing required fields.
        
        Expected:
        - Status 422
        - Field validation errors
        """
        incomplete_data = {
            "user_id": test_user.id,
            # Missing required fields: mood_rating, energy_level, stress_level
        }
        
        response = client.post("/api/checkins/", json=incomplete_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_get_user_checkins(self, client: TestClient, test_user, test_checkin):
        """
        Test retrieving user's check-ins.
        
        Expected:
        - Status 200
        - List of check-ins
        - Proper pagination
        """
        response = client.get(f"/api/checkins/user/{test_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        APITestHelpers.assert_pagination_response(data)
        
        # Should have at least one check-in
        assert len(data["items"]) >= 1
        
        # Verify check-in structure
        checkin = data["items"][0]
        expected_keys = [
            "id", "mood_rating", "energy_level", "stress_level", "created_at"
        ]
        APITestHelpers.assert_response_structure(checkin, expected_keys)
    
    def test_get_user_checkins_with_pagination(self, client: TestClient, test_user):
        """
        Test check-in retrieval with pagination parameters.
        
        Expected:
        - Proper pagination handling
        - Correct page size limits
        """
        response = client.get(f"/api/checkins/user/{test_user.id}?page=1&size=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["page"] == 1
        assert data["size"] == 5
        assert len(data["items"]) <= 5
    
    def test_get_user_checkins_date_range(self, client: TestClient, test_user):
        """
        Test check-in retrieval with date range filtering.
        
        Expected:
        - Filtered results by date
        - Proper date handling
        """
        start_date = (datetime.now() - timedelta(days=7)).date()
        end_date = datetime.now().date()
        
        response = client.get(
            f"/api/checkins/user/{test_user.id}"
            f"?start_date={start_date}&end_date={end_date}"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all returned check-ins are within date range
        for checkin in data["items"]:
            checkin_date = datetime.fromisoformat(checkin["created_at"]).date()
            assert start_date <= checkin_date <= end_date
    
    def test_get_checkin_by_id(self, client: TestClient, test_checkin):
        """
        Test retrieving specific check-in by ID.
        
        Expected:
        - Status 200
        - Complete check-in data
        """
        response = client.get(f"/api/checkins/{test_checkin.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == test_checkin.id
        assert data["mood_rating"] == test_checkin.mood_rating
        assert data["energy_level"] == test_checkin.energy_level
    
    def test_get_checkin_not_found(self, client: TestClient):
        """
        Test retrieving non-existent check-in.
        
        Expected:
        - Status 404
        - Error message
        """
        response = client.get("/api/checkins/99999")
        
        assert response.status_code == 404
        data = response.json()
        APITestHelpers.assert_error_response(data, 404)
    
    def test_update_checkin(self, client: TestClient, test_checkin):
        """
        Test updating an existing check-in.
        
        Expected:
        - Status 200
        - Updated data returned
        """
        update_data = {
            "mood_rating": 8,
            "notes": "Updated notes"
        }
        
        response = client.put(f"/api/checkins/{test_checkin.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["mood_rating"] == 8
        assert data["notes"] == "Updated notes"
    
    def test_update_checkin_validation(self, client: TestClient, test_checkin):
        """
        Test check-in update with validation errors.
        
        Expected:
        - Status 422
        - Validation error details
        """
        invalid_update = {
            "mood_rating": -1,  # Invalid value
        }
        
        response = client.put(f"/api/checkins/{test_checkin.id}", json=invalid_update)
        
        assert response.status_code == 422
    
    def test_delete_checkin(self, client: TestClient, test_checkin):
        """
        Test deleting a check-in.
        
        Expected:
        - Status 204
        - Check-in removed from database
        """
        response = client.delete(f"/api/checkins/{test_checkin.id}")
        
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/checkins/{test_checkin.id}")
        assert get_response.status_code == 404
    
    def test_delete_checkin_not_found(self, client: TestClient):
        """
        Test deleting non-existent check-in.
        
        Expected:
        - Status 404
        - Error message
        """
        response = client.delete("/api/checkins/99999")
        
        assert response.status_code == 404


@pytest.mark.unit
@pytest.mark.api
class TestCheckinAnalytics:
    """Test suite for check-in analytics endpoints."""
    
    def test_get_mood_trends(self, client: TestClient, test_user):
        """
        Test retrieving mood trends for a user.
        
        Expected:
        - Status 200
        - Trend data with statistics
        """
        response = client.get(f"/api/checkins/user/{test_user.id}/trends")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["period", "trends", "statistics"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert isinstance(data["trends"], list)
        assert isinstance(data["statistics"], dict)
    
    def test_get_mood_trends_with_period(self, client: TestClient, test_user):
        """
        Test mood trends with specific time period.
        
        Expected:
        - Filtered trends by period
        - Proper date handling
        """
        response = client.get(
            f"/api/checkins/user/{test_user.id}/trends?period=7d"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["period"] == "7d"
    
    def test_get_checkin_summary(self, client: TestClient, test_user):
        """
        Test retrieving check-in summary statistics.
        
        Expected:
        - Status 200
        - Summary statistics
        """
        response = client.get(f"/api/checkins/user/{test_user.id}/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = [
            "total_checkins", "avg_mood", "avg_energy", 
            "avg_stress", "recent_streak"
        ]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        # Verify numeric values
        assert isinstance(data["total_checkins"], int)
        assert isinstance(data["avg_mood"], (int, float))
    
    @patch('backend.core.checkin_service.generate_insights')
    def test_get_ai_insights(self, mock_insights, client: TestClient, test_user):
        """
        Test retrieving AI-generated insights for check-ins.
        
        Expected:
        - Status 200
        - AI insights data
        """
        mock_insights.return_value = {
            "mood_prediction": 7.5,
            "insights": ["Your mood has been stable"],
            "recommendations": ["Continue current routine"]
        }
        
        response = client.get(f"/api/checkins/user/{test_user.id}/insights")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["mood_prediction", "insights", "recommendations"]
        APITestHelpers.assert_response_structure(data, expected_keys)


@pytest.mark.unit
@pytest.mark.api
class TestCheckinValidation:
    """Test suite for check-in data validation."""
    
    def test_mood_rating_validation(self, client: TestClient, test_user):
        """Test mood rating field validation."""
        test_cases = [
            (0, 422),    # Below minimum
            (1, 201),    # Valid minimum
            (5, 201),    # Valid middle
            (10, 201),   # Valid maximum
            (11, 422),   # Above maximum
            ("invalid", 422)  # Wrong type
        ]
        
        for mood_rating, expected_status in test_cases:
            checkin_data = {
                "user_id": test_user.id,
                "mood_rating": mood_rating,
                "energy_level": 5,
                "stress_level": 3
            }
            
            response = client.post("/api/checkins/", json=checkin_data)
            assert response.status_code == expected_status
    
    def test_sleep_hours_validation(self, client: TestClient, test_user):
        """Test sleep hours field validation."""
        test_cases = [
            (-1, 422),     # Negative value
            (0, 201),      # Zero (valid)
            (8.5, 201),    # Decimal value
            (24, 201),     # Maximum reasonable
            (25, 422),     # Above reasonable limit
        ]
        
        for sleep_hours, expected_status in test_cases:
            checkin_data = {
                "user_id": test_user.id,
                "mood_rating": 5,
                "energy_level": 5,
                "stress_level": 3,
                "sleep_hours": sleep_hours
            }
            
            response = client.post("/api/checkins/", json=checkin_data)
            assert response.status_code == expected_status
    
    def test_activities_validation(self, client: TestClient, test_user):
        """Test activities field validation."""
        valid_checkin = {
            "user_id": test_user.id,
            "mood_rating": 5,
            "energy_level": 5,
            "stress_level": 3,
            "activities": ["exercise", "reading", "meditation"]
        }
        
        response = client.post("/api/checkins/", json=valid_checkin)
        assert response.status_code == 201
        
        # Test empty activities list (should be valid)
        valid_checkin["activities"] = []
        response = client.post("/api/checkins/", json=valid_checkin)
        assert response.status_code == 201
    
    def test_notes_length_validation(self, client: TestClient, test_user):
        """Test notes field length validation."""
        # Very long note (should fail)
        long_note = "x" * 1001  # Assuming 1000 char limit
        
        checkin_data = {
            "user_id": test_user.id,
            "mood_rating": 5,
            "energy_level": 5,
            "stress_level": 3,
            "notes": long_note
        }
        
        response = client.post("/api/checkins/", json=checkin_data)
        assert response.status_code == 422
        
        # Normal length note (should pass)
        checkin_data["notes"] = "This is a normal note"
        response = client.post("/api/checkins/", json=checkin_data)
        assert response.status_code == 201 