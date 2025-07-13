"""
Unit tests for health check endpoints.

Tests for the health monitoring and status endpoints to ensure
proper system health reporting and monitoring capabilities.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from tests.utils import APITestHelpers


@pytest.mark.unit
@pytest.mark.health
class TestHealthEndpoints:
    """Test suite for health check endpoints."""
    
    def test_basic_health_check(self, client: TestClient):
        """
        Test basic health endpoint returns success.
        
        Expected:
        - Status 200
        - Success status in response
        - Timestamp present
        """
        response = client.get("/health/")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["status", "timestamp"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_readiness_check_healthy(self, client: TestClient):
        """
        Test readiness endpoint when services are healthy.
        
        Expected:
        - Status 200
        - Ready status
        - All dependencies healthy
        """
        with patch('backend.models.database.engine.execute') as mock_db:
            mock_db.return_value = True
            
            response = client.get("/health/ready")
            
            assert response.status_code == 200
            data = response.json()
            
            expected_keys = ["status", "timestamp", "checks"]
            APITestHelpers.assert_response_structure(data, expected_keys)
            
            assert data["status"] == "ready"
            assert isinstance(data["checks"], dict)
    
    def test_readiness_check_unhealthy_database(self, client: TestClient):
        """
        Test readiness endpoint when database is unhealthy.
        
        Expected:
        - Status 503
        - Not ready status
        - Database check failure
        """
        with patch('backend.models.database.engine.execute') as mock_db:
            mock_db.side_effect = Exception("Database connection failed")
            
            response = client.get("/health/ready")
            
            assert response.status_code == 503
            data = response.json()
            
            assert data["status"] == "not ready"
            assert "checks" in data
            assert data["checks"]["database"]["status"] == "unhealthy"
    
    def test_liveness_check(self, client: TestClient):
        """
        Test liveness endpoint functionality.
        
        Expected:
        - Status 200
        - Alive status
        - Process information
        """
        response = client.get("/health/live")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = ["status", "timestamp", "uptime"]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        assert data["status"] == "alive"
        assert isinstance(data["uptime"], (int, float))
    
    def test_detailed_health_check(self, client: TestClient):
        """
        Test detailed health endpoint with comprehensive checks.
        
        Expected:
        - Status 200
        - Detailed service information
        - Memory and performance metrics
        """
        response = client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_keys = [
            "status", "timestamp", "version", "environment",
            "services", "system", "metrics"
        ]
        APITestHelpers.assert_response_structure(data, expected_keys)
        
        # Check service statuses
        assert isinstance(data["services"], dict)
        assert "database" in data["services"]
        
        # Check system metrics
        assert isinstance(data["system"], dict)
        assert "memory" in data["system"]
        assert "cpu" in data["system"]
    
    @patch('backend.core.metrics.metrics_collector.get_metrics')
    def test_detailed_health_with_metrics(self, mock_metrics, client: TestClient):
        """
        Test detailed health check includes metrics data.
        
        Expected:
        - Metrics information included
        - Performance data present
        """
        mock_metrics.return_value = {
            "http_requests_total": 100,
            "response_time_avg": 0.15,
            "active_connections": 5
        }
        
        response = client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "metrics" in data
        assert isinstance(data["metrics"], dict)
    
    def test_health_check_error_handling(self, client: TestClient):
        """
        Test health check error handling and resilience.
        
        Expected:
        - Graceful error handling
        - Partial success when possible
        """
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.side_effect = Exception("Memory check failed")
            
            response = client.get("/health/detailed")
            
            # Should still return 200 but with error information
            assert response.status_code == 200
            data = response.json()
            
            assert data["status"] in ["healthy", "degraded"]
    
    def test_health_endpoint_response_time(self, client: TestClient):
        """
        Test that health endpoints respond quickly.
        
        Expected:
        - Fast response times
        - No performance degradation
        """
        import time
        
        start_time = time.time()
        response = client.get("/health/")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_health_concurrent_requests(self, client: TestClient):
        """
        Test health endpoints handle concurrent requests.
        
        Expected:
        - All requests succeed
        - No race conditions
        """
        import threading
        
        results = []
        
        def make_request():
            response = client.get("/health/")
            results.append(response.status_code)
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 10


@pytest.mark.unit
@pytest.mark.health
class TestHealthServiceChecks:
    """Test individual health service checks."""
    
    @patch('backend.models.database.engine.execute')
    def test_database_health_check_success(self, mock_execute, client: TestClient):
        """Test database health check success case."""
        mock_execute.return_value = True
        
        response = client.get("/health/ready")
        data = response.json()
        
        assert data["checks"]["database"]["status"] == "healthy"
        assert "response_time" in data["checks"]["database"]
    
    @patch('backend.models.database.engine.execute')
    def test_database_health_check_failure(self, mock_execute, client: TestClient):
        """Test database health check failure case."""
        mock_execute.side_effect = Exception("Connection timeout")
        
        response = client.get("/health/ready")
        data = response.json()
        
        assert data["checks"]["database"]["status"] == "unhealthy"
        assert "error" in data["checks"]["database"]
    
    def test_memory_check(self, client: TestClient):
        """Test system memory health check."""
        response = client.get("/health/detailed")
        data = response.json()
        
        assert "system" in data
        assert "memory" in data["system"]
        
        memory_info = data["system"]["memory"]
        expected_memory_keys = ["total", "available", "percent"]
        
        for key in expected_memory_keys:
            assert key in memory_info
            assert isinstance(memory_info[key], (int, float))
    
    def test_cpu_check(self, client: TestClient):
        """Test CPU usage health check."""
        response = client.get("/health/detailed")
        data = response.json()
        
        assert "system" in data
        assert "cpu" in data["system"]
        
        cpu_info = data["system"]["cpu"]
        assert "percent" in cpu_info
        assert isinstance(cpu_info["percent"], (int, float))
        assert 0 <= cpu_info["percent"] <= 100 