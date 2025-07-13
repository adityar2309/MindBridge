"""
Unit tests for metrics endpoints.

Tests for the Prometheus metrics collection and monitoring endpoints
to ensure proper metrics exposure and monitoring capabilities.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from tests.utils import APITestHelpers


@pytest.mark.unit
@pytest.mark.api
class TestMetricsEndpoints:
    """Test suite for metrics API endpoints."""
    
    def test_get_metrics_endpoint(self, client: TestClient):
        """
        Test Prometheus metrics endpoint.
        
        Expected:
        - Status 200
        - Prometheus format output
        - Standard metrics included
        """
        response = client.get("/metrics")
        
        assert response.status_code == 200
        
        # Check content type
        assert response.headers.get("content-type") == "text/plain; version=0.0.4; charset=utf-8"
        
        # Check for standard Prometheus metrics
        metrics_text = response.text
        assert "http_requests_total" in metrics_text
        assert "http_request_duration_seconds" in metrics_text
    
    def test_metrics_content_format(self, client: TestClient):
        """
        Test metrics content follows Prometheus format.
        
        Expected:
        - Proper metric naming
        - Help and type annotations
        - Valid metric values
        """
        response = client.get("/metrics")
        metrics_text = response.text
        
        # Check for HELP and TYPE lines
        assert "# HELP" in metrics_text
        assert "# TYPE" in metrics_text
        
        # Check for valid metric names (no invalid characters)
        lines = metrics_text.split('\n')
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            # Metric lines should contain metric_name value
            if ' ' in line:
                metric_name = line.split(' ')[0]
                # Metric names should only contain valid characters
                assert all(c.isalnum() or c in '_:' for c in metric_name)
    
    @patch('backend.core.metrics.metrics_collector.get_all_metrics')
    def test_custom_metrics_included(self, mock_metrics, client: TestClient):
        """
        Test custom application metrics are included.
        
        Expected:
        - Business metrics present
        - Database metrics present
        - Cache metrics present
        """
        mock_metrics.return_value = {
            "mindbridge_checkins_total": 100,
            "mindbridge_users_active": 25,
            "mindbridge_database_queries_total": 500,
            "mindbridge_cache_hits_total": 300,
            "mindbridge_cache_misses_total": 50
        }
        
        response = client.get("/metrics")
        metrics_text = response.text
        
        # Check for custom metrics
        assert "mindbridge_checkins_total" in metrics_text
        assert "mindbridge_users_active" in metrics_text
        assert "mindbridge_database_queries_total" in metrics_text
        assert "mindbridge_cache_hits_total" in metrics_text
    
    def test_metrics_endpoint_performance(self, client: TestClient):
        """
        Test metrics endpoint responds quickly.
        
        Expected:
        - Fast response time
        - No performance degradation
        """
        import time
        
        start_time = time.time()
        response = client.get("/metrics")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0  # Should respond within 2 seconds
    
    def test_metrics_endpoint_concurrent_access(self, client: TestClient):
        """
        Test metrics endpoint handles concurrent requests.
        
        Expected:
        - All requests succeed
        - No race conditions
        - Consistent response format
        """
        import threading
        
        results = []
        
        def make_request():
            response = client.get("/metrics")
            results.append({
                "status_code": response.status_code,
                "has_content": len(response.text) > 0
            })
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(result["status_code"] == 200 for result in results)
        assert all(result["has_content"] for result in results)
        assert len(results) == 5
    
    def test_metrics_counter_increments(self, client: TestClient):
        """
        Test that metrics counters increment properly.
        
        Expected:
        - Request counters increase
        - Proper metric tracking
        """
        # Make some API calls to generate metrics
        client.get("/health/")
        client.get("/health/ready")
        
        response = client.get("/metrics")
        metrics_text = response.text
        
        # Should have recorded the health check requests
        assert "http_requests_total" in metrics_text
        
        # Extract counter value (basic check)
        lines = metrics_text.split('\n')
        request_total_lines = [line for line in lines if line.startswith('http_requests_total')]
        assert len(request_total_lines) > 0
    
    @patch('backend.core.metrics.metrics_collector.record_request')
    def test_request_metrics_recording(self, mock_record, client: TestClient):
        """
        Test that HTTP requests are properly recorded in metrics.
        
        Expected:
        - Request method recorded
        - Response status recorded
        - Response time recorded
        """
        response = client.get("/health/")
        
        # Verify that metrics recording was called
        mock_record.assert_called()
        
        # Check call arguments include expected information
        call_args = mock_record.call_args
        assert call_args is not None
    
    def test_error_metrics_recording(self, client: TestClient):
        """
        Test that error responses are recorded in metrics.
        
        Expected:
        - 404 errors tracked
        - Error counters incremented
        """
        # Generate a 404 error
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        
        # Check metrics include error counts
        metrics_response = client.get("/metrics")
        metrics_text = metrics_response.text
        
        # Should have recorded the error
        assert "http_requests_total" in metrics_text


@pytest.mark.unit
class TestMetricsCollection:
    """Test suite for metrics collection functionality."""
    
    @patch('backend.core.metrics.metrics_collector')
    def test_business_metrics_collection(self, mock_collector):
        """Test collection of business-specific metrics."""
        from backend.core.metrics import record_checkin_created, record_user_active
        
        # Test checkin metrics
        record_checkin_created("user123", 8)
        mock_collector.record_checkin.assert_called_with("user123", 8)
        
        # Test user activity metrics
        record_user_active("user123")
        mock_collector.record_user_activity.assert_called_with("user123")
    
    @patch('backend.core.metrics.metrics_collector')
    def test_database_metrics_collection(self, mock_collector):
        """Test collection of database performance metrics."""
        from backend.core.metrics import record_database_query
        
        record_database_query("SELECT", 0.05, True)
        mock_collector.record_database_query.assert_called_with("SELECT", 0.05, True)
    
    @patch('backend.core.metrics.metrics_collector')
    def test_cache_metrics_collection(self, mock_collector):
        """Test collection of cache performance metrics."""
        from backend.core.metrics import record_cache_operation
        
        # Test cache hit
        record_cache_operation("user_data", "hit")
        mock_collector.record_cache_hit.assert_called_with("user_data")
        
        # Test cache miss
        record_cache_operation("user_data", "miss")
        mock_collector.record_cache_miss.assert_called_with("user_data")
    
    def test_metrics_data_types(self, client: TestClient):
        """
        Test that metrics contain proper data types.
        
        Expected:
        - Counters are numeric
        - Gauges are numeric
        - Histograms have proper buckets
        """
        response = client.get("/metrics")
        metrics_text = response.text
        
        lines = metrics_text.split('\n')
        for line in lines:
            if line.startswith('#') or not line.strip():
                continue
            
            if ' ' in line:
                parts = line.split(' ')
                if len(parts) >= 2:
                    metric_value = parts[1]
                    try:
                        float(metric_value)
                    except ValueError:
                        # Special case for special values
                        assert metric_value in ['+Inf', '-Inf', 'NaN']
    
    def test_metrics_labels(self, client: TestClient):
        """
        Test that metrics include proper labels.
        
        Expected:
        - Method labels for HTTP metrics
        - Status code labels
        - Endpoint labels
        """
        # Make requests to generate labeled metrics
        client.get("/health/")
        client.post("/api/checkins/", json={})  # This will fail but generate metrics
        
        response = client.get("/metrics")
        metrics_text = response.text
        
        # Check for labeled metrics
        assert 'method=' in metrics_text
        assert 'status=' in metrics_text
        assert 'endpoint=' in metrics_text 