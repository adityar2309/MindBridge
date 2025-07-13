"""
Load and performance tests for MindBridge backend.

Tests that verify system performance under various load conditions,
stress testing, and performance benchmarking for optimization.
"""

import pytest
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor
from statistics import mean, median
from fastapi.testclient import TestClient

from tests.utils import TestDataGenerator, APITestHelpers


@pytest.mark.load
@pytest.mark.slow
class TestAPIPerformance:
    """Test suite for API endpoint performance."""
    
    def test_health_endpoint_performance(self, client: TestClient):
        """
        Test health endpoint performance under load.
        
        Expected:
        - Consistent response times
        - No degradation under load
        - Low latency
        """
        response_times = []
        
        for _ in range(100):
            start_time = time.time()
            response = client.get("/health/")
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Performance assertions
        avg_time = mean(response_times)
        median_time = median(response_times)
        max_time = max(response_times)
        
        assert avg_time < 0.1, f"Average response time too high: {avg_time}s"
        assert median_time < 0.05, f"Median response time too high: {median_time}s"
        assert max_time < 0.5, f"Max response time too high: {max_time}s"
    
    def test_concurrent_requests_performance(self, client: TestClient):
        """
        Test API performance with concurrent requests.
        
        Expected:
        - Handle concurrent requests efficiently
        - No significant latency increase
        - No errors under concurrent load
        """
        def make_request():
            start_time = time.time()
            response = client.get("/health/")
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200
            }
        
        # Test with 50 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [future.result() for future in futures]
        
        # Analyze results
        success_count = sum(1 for r in results if r["success"])
        response_times = [r["response_time"] for r in results]
        
        assert success_count == 50, f"Only {success_count}/50 requests succeeded"
        assert mean(response_times) < 0.2, "Average response time too high under load"
        assert max(response_times) < 1.0, "Max response time too high under load"
    
    def test_checkin_creation_performance(self, client: TestClient, test_user):
        """
        Test check-in creation performance.
        
        Expected:
        - Fast check-in creation
        - Consistent performance
        - Database operations efficient
        """
        response_times = []
        checkin_data = TestDataGenerator.random_checkin_data()
        checkin_data["user_id"] = test_user.id
        
        for _ in range(20):
            # Use different data for each request
            test_data = checkin_data.copy()
            test_data["mood_rating"] = (test_data["mood_rating"] % 10) + 1
            
            start_time = time.time()
            response = client.post("/api/checkins/", json=test_data)
            end_time = time.time()
            
            assert response.status_code == 201
            response_times.append(end_time - start_time)
        
        # Performance assertions
        avg_time = mean(response_times)
        assert avg_time < 0.5, f"Check-in creation too slow: {avg_time}s"
    
    def test_data_retrieval_performance(self, client: TestClient, test_user):
        """
        Test data retrieval performance with pagination.
        
        Expected:
        - Fast data retrieval
        - Efficient pagination
        - Consistent query times
        """
        # First create some test data
        for _ in range(10):
            checkin_data = TestDataGenerator.random_checkin_data()
            checkin_data["user_id"] = test_user.id
            client.post("/api/checkins/", json=checkin_data)
        
        response_times = []
        
        # Test retrieval performance
        for page in range(1, 6):
            start_time = time.time()
            response = client.get(f"/api/checkins/user/{test_user.id}?page={page}&size=5")
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        avg_time = mean(response_times)
        assert avg_time < 0.3, f"Data retrieval too slow: {avg_time}s"


@pytest.mark.load
@pytest.mark.slow
class TestDatabasePerformance:
    """Test suite for database performance under load."""
    
    def test_bulk_insert_performance(self, test_db, test_user):
        """
        Test bulk insert performance.
        
        Expected:
        - Efficient bulk operations
        - Good throughput
        - Reasonable memory usage
        """
        from backend.models.passive_data import PassiveDataPoint
        
        # Test bulk insert of 1000 records
        start_time = time.time()
        
        data_points = []
        for _ in range(1000):
            data = TestDataGenerator.random_passive_data()
            data["user_id"] = test_user.id
            data_points.append(PassiveDataPoint(**data))
        
        test_db.add_all(data_points)
        test_db.commit()
        
        end_time = time.time()
        insert_time = end_time - start_time
        
        # Should handle 1000 inserts efficiently
        assert insert_time < 5.0, f"Bulk insert too slow: {insert_time}s"
        
        # Calculate throughput
        throughput = 1000 / insert_time
        assert throughput > 200, f"Throughput too low: {throughput} records/s"
    
    def test_complex_query_performance(self, test_db):
        """
        Test complex query performance.
        
        Expected:
        - Complex queries execute efficiently
        - Good response times for analytics
        - Proper index utilization
        """
        from backend.models.user import User
        from backend.models.checkin import DailyCheckin
        from sqlalchemy import func
        
        # Create test dataset
        from tests.utils import DatabaseTestHelpers
        users = DatabaseTestHelpers.create_test_users(test_db, count=20)
        
        for user in users:
            DatabaseTestHelpers.create_test_checkins(test_db, user, count=25)
        
        # Test complex aggregation query
        start_time = time.time()
        
        query = test_db.query(
            User.id,
            User.username,
            func.avg(DailyCheckin.mood_rating).label('avg_mood'),
            func.max(DailyCheckin.mood_rating).label('max_mood'),
            func.min(DailyCheckin.mood_rating).label('min_mood'),
            func.count(DailyCheckin.id).label('total_checkins'),
            func.stddev(DailyCheckin.mood_rating).label('mood_variance')
        ).join(DailyCheckin).group_by(User.id, User.username).order_by('avg_mood')
        
        results = query.all()
        
        end_time = time.time()
        query_time = end_time - start_time
        
        assert len(results) == 20
        assert query_time < 2.0, f"Complex query too slow: {query_time}s"
    
    def test_concurrent_database_operations(self, test_db):
        """
        Test database performance under concurrent access.
        
        Expected:
        - No deadlocks
        - Reasonable performance degradation
        - Data consistency maintained
        """
        import threading
        from backend.models.user import User
        from backend.models.checkin import DailyCheckin
        
        results = []
        errors = []
        
        def database_operation():
            try:
                start_time = time.time()
                
                # Create user
                user_data = TestDataGenerator.random_user_data()
                user = User(**user_data)
                test_db.add(user)
                test_db.commit()
                test_db.refresh(user)
                
                # Create multiple checkins
                for _ in range(10):
                    checkin_data = TestDataGenerator.random_checkin_data()
                    checkin_data["user_id"] = user.id
                    checkin = DailyCheckin(**checkin_data)
                    test_db.add(checkin)
                
                test_db.commit()
                
                end_time = time.time()
                results.append(end_time - start_time)
                
            except Exception as e:
                errors.append(str(e))
                test_db.rollback()
        
        # Run 10 concurrent database operations
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=database_operation)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Analyze results
        assert len(errors) == 0, f"Database errors occurred: {errors}"
        assert len(results) == 10
        
        avg_time = mean(results)
        assert avg_time < 3.0, f"Concurrent operations too slow: {avg_time}s"


@pytest.mark.load
@pytest.mark.slow 
class TestMemoryPerformance:
    """Test suite for memory usage and optimization."""
    
    def test_memory_usage_under_load(self, client: TestClient, test_user):
        """
        Test memory usage under sustained load.
        
        Expected:
        - Memory usage stays reasonable
        - No significant memory leaks
        - Garbage collection works properly
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simulate sustained load
        for i in range(100):
            # Create check-in
            checkin_data = TestDataGenerator.random_checkin_data()
            checkin_data["user_id"] = test_user.id
            response = client.post("/api/checkins/", json=checkin_data)
            assert response.status_code == 201
            
            # Retrieve data
            response = client.get(f"/api/checkins/user/{test_user.id}")
            assert response.status_code == 200
            
            # Check memory every 25 iterations
            if i % 25 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_increase = current_memory - initial_memory
                
                # Memory shouldn't increase too much
                assert memory_increase < 100, f"Memory usage increased by {memory_increase}MB"
    
    def test_large_response_handling(self, client: TestClient, test_user):
        """
        Test handling of large response payloads.
        
        Expected:
        - Handle large datasets efficiently
        - Memory usage controlled
        - Response streaming works
        """
        # Create large dataset
        for _ in range(200):
            checkin_data = TestDataGenerator.random_checkin_data()
            checkin_data["user_id"] = test_user.id
            # Add large notes to increase payload size
            checkin_data["notes"] = "Large note content " * 50  # ~1KB per note
            client.post("/api/checkins/", json=checkin_data)
        
        # Test large response retrieval
        start_time = time.time()
        response = client.get(f"/api/checkins/user/{test_user.id}?size=200")
        end_time = time.time()
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response
        assert len(data["items"]) == 200
        
        # Performance check
        response_time = end_time - start_time
        assert response_time < 3.0, f"Large response too slow: {response_time}s"


@pytest.mark.load
class TestStressTesting:
    """Test suite for stress testing and breaking points."""
    
    def test_request_rate_limits(self, client: TestClient):
        """
        Test system behavior under high request rates.
        
        Expected:
        - Graceful handling of high request rates
        - Proper rate limiting (if implemented)
        - No system crashes
        """
        # Rapid fire requests
        start_time = time.time()
        responses = []
        
        for _ in range(500):
            response = client.get("/health/")
            responses.append(response.status_code)
        
        end_time = time.time()
        total_time = end_time - start_time
        request_rate = 500 / total_time
        
        # Most requests should succeed
        success_rate = sum(1 for status in responses if status == 200) / len(responses)
        assert success_rate > 0.95, f"Success rate too low: {success_rate}"
        
        # Should handle reasonable request rates
        assert request_rate > 100, f"Request rate too low: {request_rate} req/s"
    
    def test_error_handling_under_load(self, client: TestClient):
        """
        Test error handling under load conditions.
        
        Expected:
        - Proper error responses under load
        - System stability maintained
        - Error rates acceptable
        """
        error_responses = []
        
        # Generate various types of errors under load
        for _ in range(100):
            # Mix of valid and invalid requests
            if _ % 4 == 0:
                # Invalid endpoint
                response = client.get("/nonexistent")
                error_responses.append(response.status_code)
            elif _ % 4 == 1:
                # Invalid data
                response = client.post("/api/checkins/", json={"invalid": "data"})
                error_responses.append(response.status_code)
            else:
                # Valid request
                response = client.get("/health/")
                error_responses.append(response.status_code)
        
        # System should handle errors gracefully
        server_errors = sum(1 for status in error_responses if status >= 500)
        assert server_errors == 0, f"Server errors occurred: {server_errors}"
        
        # Expected client errors should be properly handled
        client_errors = sum(1 for status in error_responses if 400 <= status < 500)
        assert client_errors > 0, "No client errors detected (test may be invalid)"


@pytest.mark.load
class TestScalabilityBenchmarks:
    """Benchmarking tests for scalability assessment."""
    
    def test_throughput_benchmarks(self, client: TestClient, test_user):
        """
        Benchmark system throughput for various operations.
        
        Expected:
        - Document baseline performance
        - Identify performance bottlenecks
        - Establish performance targets
        """
        benchmarks = {}
        
        # Benchmark check-in creation
        checkin_data = TestDataGenerator.random_checkin_data()
        checkin_data["user_id"] = test_user.id
        
        start_time = time.time()
        for _ in range(50):
            response = client.post("/api/checkins/", json=checkin_data)
            assert response.status_code == 201
        end_time = time.time()
        
        checkin_throughput = 50 / (end_time - start_time)
        benchmarks["checkin_creation_throughput"] = checkin_throughput
        
        # Benchmark data retrieval
        start_time = time.time()
        for _ in range(50):
            response = client.get(f"/api/checkins/user/{test_user.id}")
            assert response.status_code == 200
        end_time = time.time()
        
        retrieval_throughput = 50 / (end_time - start_time)
        benchmarks["data_retrieval_throughput"] = retrieval_throughput
        
        # Log benchmarks for analysis
        print(f"Performance Benchmarks: {benchmarks}")
        
        # Basic performance assertions
        assert checkin_throughput > 10, f"Check-in throughput too low: {checkin_throughput}"
        assert retrieval_throughput > 20, f"Retrieval throughput too low: {retrieval_throughput}" 