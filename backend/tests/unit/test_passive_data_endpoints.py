"""
Unit tests for passive data endpoints.

Tests for the passive data ingestion and retrieval functionality
including fitness data, device data, and external integrations.
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from tests.utils import APITestHelpers, TestDataGenerator, assert_datetime_recent


@pytest.mark.unit
@pytest.mark.api
class TestPassiveDataEndpoints:
    """Test suite for passive data API endpoints."""
    
    def test_create_passive_data_success(self, client: TestClient, test_user, sample_passive_data):
        """
        Test successful passive data creation.
        
        Expected:
        - Status 201
        - Passive data returned
        - Proper validation
        """
        passive_data = sample_passive_data.copy()
        passive_data["user_id"] = test_user.id
        
        response = client.post("/api/passive-data/", json=passive_data)
        
        assert response.status_code == 201
        data = response.json()
        
        expected_keys = [
            "id", "user_id", "data_type", "value", 
            "unit", "source", "created_at"
        ]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert data["user_id"] == test_user.id
        assert data["data_type"] == passive_data["data_type"]
        assert data["value"] == passive_data["value"]
        assert_datetime_recent(datetime.fromisoformat(data["created_at"]))
    
    def test_create_passive_data_validation_errors(self, client: TestClient, test_user):
        """
        Test passive data creation with validation errors.
        
        Expected:
        - Status 422
        - Validation error details
        """
        # Invalid data type
        invalid_data = {
            "user_id": test_user.id,
            "data_type": "",  # Empty data type
            "value": 72.5,
            "unit": "bpm",
            "source": "fitbit"
        }
        
        response = client.post("/api/passive-data/", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_create_passive_data_missing_fields(self, client: TestClient, test_user):
        """
        Test passive data creation with missing required fields.
        
        Expected:
        - Status 422
        - Field validation errors
        """
        incomplete_data = {
            "user_id": test_user.id,
            "data_type": "heart_rate"
            # Missing: value, unit, source
        }
        
        response = client.post("/api/passive-data/", json=incomplete_data)
        
        assert response.status_code == 422
    
    def test_bulk_create_passive_data(self, client: TestClient, test_user):
        """
        Test bulk creation of passive data points.
        
        Expected:
        - Status 201
        - Multiple data points created
        """
        bulk_data = []
        for _ in range(5):
            data_point = TestDataGenerator.random_passive_data()
            data_point["user_id"] = test_user.id
            bulk_data.append(data_point)
        
        response = client.post("/api/passive-data/bulk", json=bulk_data)
        
        assert response.status_code == 201
        result = response.json()
        
        assert "created" in result
        assert result["created"] == 5
    
    def test_get_user_passive_data(self, client: TestClient, test_user, test_passive_data):
        """
        Test retrieving user's passive data.
        
        Expected:
        - Status 200
        - List of passive data points
        - Proper pagination
        """
        response = client.get(f"/api/passive-data/user/{test_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        APITestHelpers.assert_pagination_response(data)
        
        # Should have at least one data point
        assert len(data["items"]) >= 1
        
        # Verify data structure
        data_point = data["items"][0]
        expected_keys = [
            "id", "data_type", "value", "unit", "source", "created_at"
        ]
        APITestHelpers.assert_response_structure(data_point, expected_keys)
    
    def test_get_passive_data_by_type(self, client: TestClient, test_user):
        """
        Test retrieving passive data filtered by data type.
        
        Expected:
        - Filtered results by data type
        - Proper data type handling
        """
        response = client.get(
            f"/api/passive-data/user/{test_user.id}?data_type=heart_rate"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned items should be of the specified type
        for item in data["items"]:
            assert item["data_type"] == "heart_rate"
    
    def test_get_passive_data_date_range(self, client: TestClient, test_user):
        """
        Test passive data retrieval with date range filtering.
        
        Expected:
        - Filtered results by date
        - Proper date handling
        """
        start_date = (datetime.now() - timedelta(days=7)).date()
        end_date = datetime.now().date()
        
        response = client.get(
            f"/api/passive-data/user/{test_user.id}"
            f"?start_date={start_date}&end_date={end_date}"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all data points are within date range
        for item in data["items"]:
            item_date = datetime.fromisoformat(item["created_at"]).date()
            assert start_date <= item_date <= end_date
    
    def test_get_passive_data_by_source(self, client: TestClient, test_user):
        """
        Test passive data retrieval filtered by source.
        
        Expected:
        - Filtered results by source
        - Source validation
        """
        response = client.get(
            f"/api/passive-data/user/{test_user.id}?source=fitbit"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned items should be from the specified source
        for item in data["items"]:
            assert item["source"] == "fitbit"
    
    def test_get_passive_data_by_id(self, client: TestClient, test_passive_data):
        """
        Test retrieving specific passive data point by ID.
        
        Expected:
        - Status 200
        - Complete data point information
        """
        response = client.get(f"/api/passive-data/{test_passive_data.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == test_passive_data.id
        assert data["data_type"] == test_passive_data.data_type
        assert data["value"] == test_passive_data.value
    
    def test_get_passive_data_not_found(self, client: TestClient):
        """
        Test retrieving non-existent passive data point.
        
        Expected:
        - Status 404
        - Error message
        """
        response = client.get("/api/passive-data/99999")
        
        assert response.status_code == 404
        data = response.json()
        APITestHelpers.assert_error_response(data, 404)
    
    def test_update_passive_data(self, client: TestClient, test_passive_data):
        """
        Test updating passive data point.
        
        Expected:
        - Status 200
        - Updated data returned
        """
        update_data = {
            "value": 85.0,
            "metadata": {"updated": True}
        }
        
        response = client.put(
            f"/api/passive-data/{test_passive_data.id}", 
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["value"] == 85.0
        assert data["metadata"]["updated"] is True
    
    def test_delete_passive_data(self, client: TestClient, test_passive_data):
        """
        Test deleting passive data point.
        
        Expected:
        - Status 204
        - Data point removed from database
        """
        response = client.delete(f"/api/passive-data/{test_passive_data.id}")
        
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/passive-data/{test_passive_data.id}")
        assert get_response.status_code == 404


@pytest.mark.unit
@pytest.mark.api
class TestPassiveDataAnalytics:
    """Test suite for passive data analytics endpoints."""
    
    def test_get_data_summary(self, client: TestClient, test_user):
        """
        Test retrieving passive data summary.
        
        Expected:
        - Status 200
        - Summary statistics by data type
        """
        response = client.get(f"/api/passive-data/user/{test_user.id}/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["data_types", "total_points", "date_range"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert isinstance(data["data_types"], dict)
        assert isinstance(data["total_points"], int)
    
    def test_get_trends_by_type(self, client: TestClient, test_user):
        """
        Test retrieving trends for specific data type.
        
        Expected:
        - Status 200
        - Trend data and statistics
        """
        response = client.get(
            f"/api/passive-data/user/{test_user.id}/trends?data_type=heart_rate"
        )
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["data_type", "trends", "statistics"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert data["data_type"] == "heart_rate"
        assert isinstance(data["trends"], list)
    
    def test_get_correlations(self, client: TestClient, test_user):
        """
        Test retrieving correlations between data types.
        
        Expected:
        - Status 200
        - Correlation analysis
        """
        response = client.get(f"/api/passive-data/user/{test_user.id}/correlations")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["correlations", "period"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert isinstance(data["correlations"], dict)


@pytest.mark.unit
@pytest.mark.api
class TestPassiveDataValidation:
    """Test suite for passive data validation."""
    
    def test_data_type_validation(self, client: TestClient, test_user):
        """Test data type field validation."""
        valid_types = ["heart_rate", "steps", "sleep", "activity"]
        
        for data_type in valid_types:
            passive_data = {
                "user_id": test_user.id,
                "data_type": data_type,
                "value": 100,
                "unit": "units",
                "source": "test"
            }
            
            response = client.post("/api/passive-data/", json=passive_data)
            assert response.status_code == 201
    
    def test_value_validation(self, client: TestClient, test_user):
        """Test value field validation."""
        test_cases = [
            (-1, 422),       # Negative value (invalid for most types)
            (0, 201),        # Zero (valid)
            (100.5, 201),    # Decimal value
            ("invalid", 422) # String value (invalid)
        ]
        
        for value, expected_status in test_cases:
            passive_data = {
                "user_id": test_user.id,
                "data_type": "heart_rate",
                "value": value,
                "unit": "bpm",
                "source": "test"
            }
            
            response = client.post("/api/passive-data/", json=passive_data)
            assert response.status_code == expected_status
    
    def test_source_validation(self, client: TestClient, test_user):
        """Test source field validation."""
        valid_sources = ["fitbit", "apple_watch", "samsung_health", "manual"]
        
        for source in valid_sources:
            passive_data = {
                "user_id": test_user.id,
                "data_type": "heart_rate",
                "value": 72,
                "unit": "bpm",
                "source": source
            }
            
            response = client.post("/api/passive-data/", json=passive_data)
            assert response.status_code == 201
    
    def test_metadata_validation(self, client: TestClient, test_user):
        """Test metadata field validation."""
        # Valid metadata (JSON object)
        passive_data = {
            "user_id": test_user.id,
            "data_type": "heart_rate",
            "value": 72,
            "unit": "bpm",
            "source": "test",
            "metadata": {
                "confidence": 0.95,
                "device_id": "abc123",
                "calibrated": True
            }
        }
        
        response = client.post("/api/passive-data/", json=passive_data)
        assert response.status_code == 201
        
        # Empty metadata (should be valid)
        passive_data["metadata"] = {}
        response = client.post("/api/passive-data/", json=passive_data)
        assert response.status_code == 201
    
    def test_location_validation(self, client: TestClient, test_user):
        """Test location field validation."""
        # Valid location
        passive_data = {
            "user_id": test_user.id,
            "data_type": "steps",
            "value": 1000,
            "unit": "steps",
            "source": "test",
            "location": {
                "lat": 40.7128,
                "lng": -74.0060
            }
        }
        
        response = client.post("/api/passive-data/", json=passive_data)
        assert response.status_code == 201
        
        # Invalid location (out of range)
        passive_data["location"] = {"lat": 91, "lng": 181}  # Invalid coordinates
        response = client.post("/api/passive-data/", json=passive_data)
        assert response.status_code == 422


@pytest.mark.unit
@pytest.mark.api
class TestPassiveDataIntegration:
    """Test suite for passive data external integrations."""
    
    @patch('backend.core.passive_data_service.fitbit_client')
    def test_fitbit_integration(self, mock_fitbit, client: TestClient, test_user):
        """
        Test Fitbit data integration.
        
        Expected:
        - Successful data import
        - Proper data transformation
        """
        mock_fitbit.get_heart_rate.return_value = [
            {"time": "2024-01-01T10:00:00", "value": 72},
            {"time": "2024-01-01T11:00:00", "value": 75}
        ]
        
        response = client.post(
            f"/api/passive-data/user/{test_user.id}/import/fitbit",
            json={"data_types": ["heart_rate"], "days": 1}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "imported" in data
        assert data["imported"] > 0
    
    @patch('backend.core.passive_data_service.apple_health_client')
    def test_apple_health_integration(self, mock_apple, client: TestClient, test_user):
        """
        Test Apple Health data integration.
        
        Expected:
        - Successful data import
        - Proper data mapping
        """
        mock_apple.get_steps.return_value = [
            {"date": "2024-01-01", "value": 8500},
            {"date": "2024-01-02", "value": 9200}
        ]
        
        response = client.post(
            f"/api/passive-data/user/{test_user.id}/import/apple-health",
            json={"data_types": ["steps"], "days": 2}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "imported" in data
        assert data["imported"] > 0
    
    def test_data_export(self, client: TestClient, test_user):
        """
        Test passive data export functionality.
        
        Expected:
        - Status 200
        - Exportable data format
        """
        response = client.get(
            f"/api/passive-data/user/{test_user.id}/export",
            params={"format": "csv", "data_types": "heart_rate,steps"}
        )
        
        assert response.status_code == 200
        
        # Check response headers for file download
        assert "attachment" in response.headers.get("content-disposition", "")
    
    def test_data_sync_status(self, client: TestClient, test_user):
        """
        Test data synchronization status.
        
        Expected:
        - Status 200
        - Sync status information
        """
        response = client.get(f"/api/passive-data/user/{test_user.id}/sync-status")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["sources", "last_sync", "status"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert isinstance(data["sources"], dict) 