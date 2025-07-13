# MindBridge Backend Testing Guide

This document provides comprehensive information about testing the MindBridge backend system, including setup, execution, and best practices.

## Overview

The MindBridge backend test suite consists of multiple layers of testing to ensure reliability, performance, and maintainability:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **Load Tests**: Test performance under various load conditions
- **Health Tests**: Test monitoring and health check endpoints
- **Code Quality**: Linting, type checking, and security checks

## Quick Start

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run quick test suite (unit + health)
python scripts/run_tests.py --quick

# Run all tests
python scripts/run_tests.py --all --verbose
```

### Docker Testing

```bash
# Run unit tests (fast)
docker-compose -f docker-compose.test.yml up unit-tests

# Run all tests
docker-compose -f docker-compose.test.yml up backend-tests

# Run specific test types
docker-compose -f docker-compose.test.yml up integration-tests
docker-compose -f docker-compose.test.yml up load-tests
docker-compose -f docker-compose.test.yml up quality-checks
```

## Test Structure

```
backend/tests/
├── __init__.py                 # Test package
├── conftest.py                 # Global test configuration
├── utils.py                    # Test utilities and helpers
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_health_endpoints.py
│   ├── test_checkin_endpoints.py
│   ├── test_passive_data_endpoints.py
│   └── test_metrics_endpoints.py
├── integration/                # Integration tests
│   ├── __init__.py
│   └── test_database_integration.py
└── load/                       # Load and performance tests
    ├── __init__.py
    └── test_performance.py
```

## Test Configuration

### pytest.ini

The test configuration is defined in `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests for individual components
    integration: Integration tests with database
    api: API endpoint tests
    slow: Slow running tests
    load: Load and performance tests
    health: Health check tests
asyncio_mode = auto
```

### Test Markers

Use markers to categorize and filter tests:

```python
@pytest.mark.unit          # Unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.load          # Load tests
@pytest.mark.slow          # Slow running tests
@pytest.mark.health        # Health check tests
@pytest.mark.api           # API endpoint tests
```

## Test Runner Script

The `scripts/run_tests.py` script provides a unified interface for running tests:

### Basic Usage

```bash
# Run specific test types
python scripts/run_tests.py --unit           # Unit tests only
python scripts/run_tests.py --integration    # Integration tests only
python scripts/run_tests.py --load           # Load tests only
python scripts/run_tests.py --health         # Health check tests only

# Run test combinations
python scripts/run_tests.py --quick          # Unit + health tests
python scripts/run_tests.py --all            # All tests

# Run specific test patterns
python scripts/run_tests.py -k "health"      # Tests matching "health"
python scripts/run_tests.py -k "checkin and create"  # Specific patterns
```

### Code Quality Checks

```bash
python scripts/run_tests.py --lint           # Code formatting and linting
python scripts/run_tests.py --type-check     # Type checking with mypy
python scripts/run_tests.py --security       # Security vulnerability checks
```

### Test Reports

```bash
python scripts/run_tests.py --report         # Generate comprehensive report
```

This generates:
- `htmlcov/index.html` - HTML coverage report
- `test-report.html` - Detailed test report
- `test-results.xml` - JUnit XML for CI/CD

### Options

```bash
-v, --verbose           # Verbose output
--no-coverage          # Disable coverage reporting
--install-deps         # Install test dependencies
--cleanup              # Clean up test artifacts
```

## Test Fixtures and Utilities

### Available Fixtures

The test suite provides comprehensive fixtures in `conftest.py`:

```python
# Database and app fixtures
test_db                 # Test database session
app                     # FastAPI app instance
client                  # Synchronous test client
async_client           # Asynchronous test client

# Data fixtures
sample_user_data       # Sample user data
sample_checkin_data    # Sample check-in data
sample_passive_data    # Sample passive data
sample_quiz_data       # Sample quiz data

# Database objects
test_user              # Test user in database
test_checkin           # Test check-in in database
test_passive_data      # Test passive data in database

# Utilities
auth_headers           # Mock authentication headers
mock_ai_response       # Mock AI service response
```

### Test Utilities

The `tests/utils.py` module provides helper classes and functions:

```python
# Data generation
TestDataGenerator.random_user_data()
TestDataGenerator.random_checkin_data()
TestDataGenerator.random_passive_data()

# API testing helpers
APITestHelpers.assert_response_structure(data, keys)
APITestHelpers.assert_error_response(data, status)
APITestHelpers.assert_pagination_response(data)

# Database helpers
DatabaseTestHelpers.create_test_users(session, count)
DatabaseTestHelpers.create_test_checkins(session, user, count)

# Mock services
MockServices.mock_ai_service_response()
MockServices.mock_notification_service()
```

## Test Categories

### Unit Tests

Test individual components in isolation:

```bash
python scripts/run_tests.py --unit -v
```

**Coverage includes:**
- API endpoint handlers
- Request/response validation
- Business logic functions
- Error handling
- Health check endpoints
- Metrics collection

**Example:**
```python
@pytest.mark.unit
@pytest.mark.api
def test_create_checkin_success(client, test_user, sample_checkin_data):
    """Test successful check-in creation."""
    response = client.post("/api/checkins/", json=sample_checkin_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["mood_rating"] == sample_checkin_data["mood_rating"]
```

### Integration Tests

Test interactions between components:

```bash
python scripts/run_tests.py --integration -v
```

**Coverage includes:**
- Database operations and transactions
- API workflow integration
- Service layer interactions
- Complex queries and joins
- Data integrity constraints

**Example:**
```python
@pytest.mark.integration
def test_checkin_creation_with_relationships(test_db, test_user):
    """Test check-in creation with proper user relationships."""
    checkin = DailyCheckin(user_id=test_user.id, mood_rating=7)
    test_db.add(checkin)
    test_db.commit()
    
    assert checkin.user.id == test_user.id
    assert len(test_user.checkins) > 0
```

### Load Tests

Test performance under various load conditions:

```bash
python scripts/run_tests.py --load -v
```

**Coverage includes:**
- API endpoint performance
- Database query performance
- Concurrent request handling
- Memory usage monitoring
- Throughput benchmarking

**Example:**
```python
@pytest.mark.load
@pytest.mark.slow
def test_concurrent_requests_performance(client):
    """Test API performance with concurrent requests."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [future.result() for future in futures]
    
    assert all(r["success"] for r in results)
    assert mean(r["response_time"] for r in results) < 0.2
```

### Health Tests

Test monitoring and health check functionality:

```bash
python scripts/run_tests.py --health -v
```

**Coverage includes:**
- Basic health endpoint
- Readiness checks
- Liveness checks
- Detailed health information
- Service dependency checks

## Docker Testing Environment

### Test Services

The `docker-compose.test.yml` provides isolated testing environment:

- `test-postgres`: Test database (PostgreSQL)
- `test-redis`: Test cache (Redis)
- `backend-tests`: Full test suite
- `unit-tests`: Fast unit tests only
- `integration-tests`: Integration tests
- `load-tests`: Performance tests
- `quality-checks`: Code quality validation
- `test-reports`: Test report generation
- `test-results-server`: Web server for viewing reports

### Running Specific Test Services

```bash
# Fast unit tests (no external dependencies)
docker-compose -f docker-compose.test.yml up unit-tests

# Integration tests (with database)
docker-compose -f docker-compose.test.yml up integration-tests

# Load tests
docker-compose -f docker-compose.test.yml up load-tests

# Code quality checks
docker-compose -f docker-compose.test.yml up quality-checks

# Generate and serve test reports
docker-compose -f docker-compose.test.yml up test-reports
docker-compose -f docker-compose.test.yml up test-results-server
# View reports at http://localhost:8080
```

### Environment Variables

Test environment is configured with:

```yaml
TESTING: "true"
DATABASE_URL: postgresql://test_user:test_password@test-postgres:5432/mindbridge_test
REDIS_URL: redis://test-redis:6379/0
LOG_LEVEL: DEBUG
DISABLE_EXTERNAL_APIS: "true"
MOCK_AI_SERVICES: "true"
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test_password
          POSTGRES_USER: test_user
          POSTGRES_DB: mindbridge_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python scripts/run_tests.py --all --verbose
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/mindbridge_test
        TESTING: true
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
```

## Best Practices

### Writing Tests

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **Use descriptive test names**: Test purpose should be clear
3. **Test one thing at a time**: Single responsibility per test
4. **Use appropriate fixtures**: Reuse common test data
5. **Mock external dependencies**: Isolate components under test

### Test Data

1. **Use factories for test data**: `TestDataGenerator` for realistic data
2. **Clean up after tests**: Database cleanup handled automatically
3. **Avoid hardcoded values**: Use random/generated data when possible
4. **Test edge cases**: Boundary conditions and error scenarios

### Performance Testing

1. **Set realistic thresholds**: Based on actual requirements
2. **Test under load**: Concurrent requests and high volume
3. **Monitor resource usage**: Memory, CPU, database connections
4. **Document benchmarks**: Track performance over time

### Code Quality

1. **Maintain high coverage**: Aim for >90% test coverage
2. **Run linting regularly**: Code formatting and style consistency
3. **Type checking**: Use mypy for type safety
4. **Security scanning**: Check for vulnerabilities

## Troubleshooting

### Common Issues

**Tests fail with database connection errors:**
```bash
# Ensure test database is running
docker-compose -f docker-compose.test.yml up test-postgres

# Check database URL configuration
echo $DATABASE_URL
```

**Import errors in tests:**
```bash
# Set Python path
export PYTHONPATH="/path/to/backend:$PYTHONPATH"

# Or use the test runner script
python scripts/run_tests.py --unit
```

**Slow test execution:**
```bash
# Run only fast tests
python scripts/run_tests.py --quick

# Skip load tests
python scripts/run_tests.py --unit --integration
```

**Coverage report issues:**
```bash
# Generate coverage report manually
pytest --cov=backend --cov-report=html tests/
```

### Debug Mode

Run tests with debug output:

```bash
# Verbose pytest output
python scripts/run_tests.py --unit -v

# Python debug mode
python -d scripts/run_tests.py --unit

# Database query logging
LOG_LEVEL=DEBUG python scripts/run_tests.py --integration
```

## Performance Targets

The test suite enforces these performance targets:

- **Health endpoints**: < 100ms average response time
- **API endpoints**: < 500ms for CRUD operations
- **Database queries**: < 100ms for simple queries
- **Bulk operations**: > 200 records/second throughput
- **Concurrent requests**: Support 50+ concurrent users
- **Memory usage**: < 100MB increase under sustained load

## Test Coverage

Target coverage metrics:

- **Overall coverage**: > 90%
- **Unit test coverage**: > 95%
- **API endpoint coverage**: 100%
- **Business logic coverage**: > 95%
- **Error handling coverage**: > 85%

View coverage reports:
```bash
# Generate and view coverage report
python scripts/run_tests.py --report
open htmlcov/index.html
```

## Maintenance

### Regular Tasks

1. **Update test dependencies**: Keep pytest and related packages current
2. **Review test performance**: Monitor test execution times
3. **Clean up test data**: Remove obsolete fixtures and test data
4. **Update documentation**: Keep testing docs current
5. **Review coverage**: Identify and test uncovered code paths

### Test Data Refresh

Periodically refresh test data to ensure realistic scenarios:

```bash
# Update test data generators
vim tests/utils.py

# Regenerate test fixtures
python scripts/run_tests.py --cleanup
python scripts/run_tests.py --unit
```

## Getting Help

- **Test failures**: Check test output and logs for specific error messages
- **Performance issues**: Use load tests to identify bottlenecks
- **Coverage gaps**: Review coverage reports to identify untested code
- **Environment issues**: Verify test configuration and dependencies

For additional support, refer to the main project documentation or contact the development team. 