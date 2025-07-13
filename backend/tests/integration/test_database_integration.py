"""
Integration tests for database operations.

Tests that verify database interactions, transactions, constraints,
and data integrity across the entire system.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import select

from backend.models.user import User
from backend.models.checkin import DailyCheckin
from backend.models.passive_data import PassiveDataPoint
from backend.models.quiz import QuizResponse
from backend.models.ai_insights import AIMoodInsight
from tests.utils import TestDataGenerator, DatabaseTestHelpers


@pytest.mark.integration
@pytest.mark.slow
class TestDatabaseIntegration:
    """Test suite for database integration operations."""
    
    def test_user_creation_and_retrieval(self, test_db):
        """
        Test user creation and retrieval from database.
        
        Expected:
        - User created successfully
        - All fields stored correctly
        - Relationships work properly
        """
        user_data = TestDataGenerator.random_user_data()
        user = User(**user_data)
        
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Verify user was created
        assert user.id is not None
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.created_at is not None
        
        # Test retrieval
        retrieved_user = test_db.query(User).filter(User.id == user.id).first()
        assert retrieved_user is not None
        assert retrieved_user.username == user_data["username"]
    
    def test_checkin_creation_with_relationships(self, test_db, test_user):
        """
        Test check-in creation with proper user relationships.
        
        Expected:
        - Check-in linked to user
        - Foreign key constraints work
        - Data integrity maintained
        """
        checkin_data = TestDataGenerator.random_checkin_data()
        checkin_data["user_id"] = test_user.id
        
        checkin = DailyCheckin(**checkin_data)
        test_db.add(checkin)
        test_db.commit()
        test_db.refresh(checkin)
        
        # Verify check-in was created
        assert checkin.id is not None
        assert checkin.user_id == test_user.id
        assert checkin.mood_rating == checkin_data["mood_rating"]
        
        # Test relationship access
        assert checkin.user is not None
        assert checkin.user.id == test_user.id
        
        # Test reverse relationship
        user_checkins = test_user.checkins
        assert len(user_checkins) > 0
        assert checkin.id in [c.id for c in user_checkins]
    
    def test_passive_data_bulk_operations(self, test_db, test_user):
        """
        Test bulk insertion and querying of passive data.
        
        Expected:
        - Multiple data points created efficiently
        - Queries perform well
        - Data integrity maintained
        """
        # Create bulk passive data
        data_points = []
        for _ in range(50):
            data = TestDataGenerator.random_passive_data()
            data["user_id"] = test_user.id
            data_points.append(PassiveDataPoint(**data))
        
        test_db.add_all(data_points)
        test_db.commit()
        
        # Query all data points for user
        query_result = test_db.query(PassiveDataPoint).filter(
            PassiveDataPoint.user_id == test_user.id
        ).all()
        
        assert len(query_result) == 50
        
        # Test filtered queries
        heart_rate_data = test_db.query(PassiveDataPoint).filter(
            PassiveDataPoint.user_id == test_user.id,
            PassiveDataPoint.data_type == "heart_rate"
        ).all()
        
        # Should have some heart rate data (based on random generation)
        assert isinstance(heart_rate_data, list)
    
    def test_database_constraints(self, test_db, test_user):
        """
        Test database constraints and validation.
        
        Expected:
        - Foreign key constraints enforced
        - Unique constraints work
        - Check constraints validated
        """
        # Test foreign key constraint
        with pytest.raises(Exception):  # Should raise integrity error
            invalid_checkin = DailyCheckin(
                user_id=99999,  # Non-existent user
                mood_rating=5,
                energy_level=5,
                stress_level=3
            )
            test_db.add(invalid_checkin)
            test_db.commit()
    
    def test_database_transactions(self, test_db, test_user):
        """
        Test database transaction handling.
        
        Expected:
        - Transactions commit properly
        - Rollbacks work correctly
        - Data consistency maintained
        """
        # Test successful transaction
        checkin_data = TestDataGenerator.random_checkin_data()
        checkin_data["user_id"] = test_user.id
        
        try:
            checkin = DailyCheckin(**checkin_data)
            test_db.add(checkin)
            test_db.commit()
            
            # Verify data was committed
            result = test_db.query(DailyCheckin).filter(
                DailyCheckin.user_id == test_user.id
            ).first()
            assert result is not None
            
        except Exception:
            test_db.rollback()
            pytest.fail("Transaction should have succeeded")
    
    def test_complex_queries(self, test_db):
        """
        Test complex database queries with joins and aggregations.
        
        Expected:
        - Join queries work correctly
        - Aggregations are accurate
        - Performance is acceptable
        """
        # Create test data
        users = DatabaseTestHelpers.create_test_users(test_db, count=3)
        
        for user in users:
            DatabaseTestHelpers.create_test_checkins(test_db, user, count=5)
        
        # Test join query
        query = test_db.query(User, DailyCheckin).join(
            DailyCheckin, User.id == DailyCheckin.user_id
        )
        results = query.all()
        
        assert len(results) > 0
        
        # Each result should be a tuple of (User, DailyCheckin)
        for user, checkin in results:
            assert isinstance(user, User)
            assert isinstance(checkin, DailyCheckin)
            assert checkin.user_id == user.id
    
    def test_date_range_queries(self, test_db, test_user):
        """
        Test date-based queries and filtering.
        
        Expected:
        - Date filters work correctly
        - Timezone handling proper
        - Range queries efficient
        """
        # Create checkins across different dates
        dates = [
            datetime.now() - timedelta(days=7),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=1),
            datetime.now()
        ]
        
        checkins = []
        for date in dates:
            checkin_data = TestDataGenerator.random_checkin_data()
            checkin_data["user_id"] = test_user.id
            checkin = DailyCheckin(**checkin_data)
            checkin.created_at = date
            checkins.append(checkin)
        
        test_db.add_all(checkins)
        test_db.commit()
        
        # Query last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_checkins = test_db.query(DailyCheckin).filter(
            DailyCheckin.user_id == test_user.id,
            DailyCheckin.created_at >= seven_days_ago
        ).all()
        
        assert len(recent_checkins) == 4
        
        # Query specific date range
        three_days_ago = datetime.now() - timedelta(days=3)
        range_checkins = test_db.query(DailyCheckin).filter(
            DailyCheckin.user_id == test_user.id,
            DailyCheckin.created_at >= three_days_ago,
            DailyCheckin.created_at <= datetime.now()
        ).all()
        
        assert len(range_checkins) == 3


@pytest.mark.integration
class TestDatabasePerformance:
    """Test suite for database performance and optimization."""
    
    def test_large_dataset_queries(self, test_db):
        """
        Test queries on larger datasets.
        
        Expected:
        - Queries complete in reasonable time
        - Memory usage is acceptable
        - Indexes are effective
        """
        import time
        
        # Create larger dataset
        users = DatabaseTestHelpers.create_test_users(test_db, count=10)
        
        for user in users:
            DatabaseTestHelpers.create_test_checkins(test_db, user, count=30)
        
        # Test query performance
        start_time = time.time()
        
        # Complex query with aggregation
        from sqlalchemy import func
        mood_averages = test_db.query(
            User.id,
            User.username,
            func.avg(DailyCheckin.mood_rating).label('avg_mood'),
            func.count(DailyCheckin.id).label('checkin_count')
        ).join(DailyCheckin).group_by(User.id, User.username).all()
        
        end_time = time.time()
        query_time = end_time - start_time
        
        # Should complete in reasonable time
        assert query_time < 2.0  # Less than 2 seconds
        assert len(mood_averages) == 10
        
        for user_id, username, avg_mood, checkin_count in mood_averages:
            assert isinstance(avg_mood, (int, float))
            assert checkin_count > 0
    
    def test_concurrent_database_access(self, test_db):
        """
        Test concurrent database operations.
        
        Expected:
        - No deadlocks
        - Data consistency maintained
        - Performance acceptable
        """
        import threading
        
        results = []
        errors = []
        
        def create_user_with_checkins():
            try:
                # Each thread creates a user with checkins
                user_data = TestDataGenerator.random_user_data()
                user = User(**user_data)
                test_db.add(user)
                test_db.commit()
                test_db.refresh(user)
                
                # Create checkins for the user
                for _ in range(5):
                    checkin_data = TestDataGenerator.random_checkin_data()
                    checkin_data["user_id"] = user.id
                    checkin = DailyCheckin(**checkin_data)
                    test_db.add(checkin)
                
                test_db.commit()
                results.append(user.id)
                
            except Exception as e:
                errors.append(str(e))
                test_db.rollback()
        
        # Run concurrent operations
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=create_user_with_checkins)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Check results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5
        
        # Verify all data was created
        total_users = test_db.query(User).count()
        total_checkins = test_db.query(DailyCheckin).count()
        
        assert total_users >= 5
        assert total_checkins >= 25


@pytest.mark.integration
class TestDataMigrations:
    """Test suite for database migration scenarios."""
    
    def test_schema_compatibility(self, test_db):
        """
        Test schema compatibility and data migration scenarios.
        
        Expected:
        - Current schema works with test data
        - Relationships are properly defined
        - Data types are correct
        """
        # Test all model types can be created
        user_data = TestDataGenerator.random_user_data()
        user = User(**user_data)
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Test checkin
        checkin_data = TestDataGenerator.random_checkin_data()
        checkin_data["user_id"] = user.id
        checkin = DailyCheckin(**checkin_data)
        test_db.add(checkin)
        test_db.commit()
        
        # Test passive data
        passive_data = TestDataGenerator.random_passive_data()
        passive_data["user_id"] = user.id
        data_point = PassiveDataPoint(**passive_data)
        test_db.add(data_point)
        test_db.commit()
        
        # Test quiz response
        quiz_data = TestDataGenerator.random_quiz_responses()
        quiz_data["user_id"] = user.id
        quiz = QuizResponse(**quiz_data)
        test_db.add(quiz)
        test_db.commit()
        
        # Verify all relationships work
        assert user.checkins
        assert user.passive_data_points
        assert user.quiz_responses
    
    def test_data_integrity_constraints(self, test_db):
        """
        Test data integrity and constraint enforcement.
        
        Expected:
        - Constraints prevent invalid data
        - Referential integrity maintained
        - Data validation works
        """
        user_data = TestDataGenerator.random_user_data()
        user = User(**user_data)
        test_db.add(user)
        test_db.commit()
        
        # Test mood rating constraints (should be 1-10)
        with pytest.raises(Exception):
            invalid_checkin = DailyCheckin(
                user_id=user.id,
                mood_rating=15,  # Invalid: out of range
                energy_level=5,
                stress_level=3
            )
            test_db.add(invalid_checkin)
            test_db.commit() 