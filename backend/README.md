# MindBridge Backend

This is the backend microservice for the MindBridge Mood & Mental Health Tracker application.

## Architecture

The backend is built with:
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database
- **Redis** - Caching and task queue
- **Celery** - Background task processing
- **Prometheus** - Metrics collection
- **Alembic** - Database migrations

## Features

- ✅ Daily check-in API with mood tracking
- ✅ Passive data ingestion (health, activity, etc.)
- ✅ Real-time health monitoring
- ✅ Comprehensive error handling
- ✅ Metrics collection and monitoring
- ✅ Database migrations
- ✅ Container-ready with Docker
- ✅ Kubernetes deployment manifests
- ✅ Background task processing
- ✅ API Gateway configuration

## Quick Start

### Local Development with Docker Compose

1. **Clone and navigate to the project:**
   ```bash
   cd MindBridge
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health/
   - Metrics: http://localhost:8000/metrics

### Manual Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export DATABASE_URL="postgresql://postgres:password@localhost:5432/mindbridge_dev"
   export REDIS_URL="redis://localhost:6379/0"
   ```

3. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start the application:**
   ```bash
   uvicorn api.main:app --reload
   ```

## API Endpoints

### Health & Monitoring
- `GET /health/` - Basic health check
- `GET /health/ready` - Readiness check with dependencies
- `GET /health/live` - Liveness check for Kubernetes
- `GET /health/detailed` - Detailed health information
- `GET /metrics` - Prometheus metrics

### Check-ins
- `POST /api/v1/checkins/` - Create daily check-in
- `GET /api/v1/checkins/{id}` - Get specific check-in
- `PUT /api/v1/checkins/{id}` - Update check-in
- `GET /api/v1/checkins/` - List user check-ins
- `GET /api/v1/checkins/today/` - Get today's check-in
- `GET /api/v1/checkins/streak/` - Get check-in streak
- `GET /api/v1/checkins/analytics/` - Get mood analytics

### Passive Data
- `POST /api/v1/passive-data/` - Ingest single data point
- `POST /api/v1/passive-data/bulk` - Bulk data ingestion
- `GET /api/v1/passive-data/` - List data points with filters
- `GET /api/v1/passive-data/aggregate/` - Get aggregated data
- `GET /api/v1/passive-data/health-metrics/` - Get health metrics

## Database Schema

The application uses PostgreSQL with the following main tables:
- `users` - User accounts and settings
- `daily_checkins` - Daily mood check-ins
- `passive_data_points` - Passive data collection
- `quiz_questions` & `quiz_sessions` - Interactive assessments
- `ai_mood_insights` - AI-generated insights
- `conversation_logs` - AI assistant conversations

## Environment Variables

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string

### Optional
- `ENVIRONMENT` - Environment name (default: development)
- `DEBUG` - Debug mode (default: false)
- `ALLOWED_ORIGINS` - CORS allowed origins
- `TRUSTED_HOSTS` - Trusted host names
- `JWT_SECRET_KEY` - JWT signing key
- `OPENAI_API_KEY` - OpenAI API key for AI features

## Monitoring

### Metrics
The application exposes Prometheus metrics at `/metrics` including:
- HTTP request metrics (count, duration, status codes)
- Database query metrics
- Business metrics (check-ins, mood ratings, etc.)
- System metrics (memory, CPU usage)
- Cache hit ratios

### Health Checks
Multiple health check endpoints for different use cases:
- Basic health check for load balancers
- Readiness check for Kubernetes (includes dependency checks)
- Liveness check for Kubernetes
- Detailed health check with system information

### Alerting
Prometheus alerting rules are configured for:
- High error rates
- High response times
- Database connection failures
- High resource usage
- SSL certificate expiry

## Deployment

### Docker
```bash
# Build production image
docker build -f Dockerfile -t mindbridge/backend:latest .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e REDIS_URL="redis://..." \
  mindbridge/backend:latest
```

### Kubernetes
```bash
# Apply manifests
kubectl apply -f infrastructure/kubernetes/

# Check deployment status
kubectl get pods -n mindbridge
```

## Development

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=backend tests/
```

### Code Quality
```bash
# Format code
black backend/

# Sort imports
isort backend/

# Lint code
flake8 backend/

# Type checking
mypy backend/
```

## Background Tasks

The application uses Celery for background processing:

### Worker
```bash
celery -A core.celery_app worker --loglevel=info
```

### Beat Scheduler
```bash
celery -A core.celery_app beat --loglevel=info
```

### Monitoring
```bash
celery -A core.celery_app flower
```

## Performance

### Optimization
- Connection pooling for database
- Redis caching for frequently accessed data
- Background processing for heavy operations
- Horizontal pod autoscaling in Kubernetes

### Scaling
- Stateless application design
- Database connection pooling
- Redis for shared state
- Kubernetes HPA for automatic scaling

## Security

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- CORS configuration
- Rate limiting via ingress
- Secrets management with Kubernetes
- Non-root container execution

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check DATABASE_URL environment variable
   - Verify PostgreSQL service is running
   - Check network connectivity

2. **Redis connection errors**
   - Check REDIS_URL environment variable
   - Verify Redis service is running
   - Check network connectivity

3. **High memory usage**
   - Check for memory leaks in application logs
   - Monitor database connection pool
   - Review Prometheus metrics

### Logs
```bash
# View application logs
kubectl logs -f deployment/backend-deployment -n mindbridge

# View all pod logs
kubectl logs -l app=backend -n mindbridge
```

## Contributing

1. Follow the code style (Black, isort, flake8)
2. Add tests for new features
3. Update documentation
4. Ensure all health checks pass
5. Test with Docker Compose locally

## License

This project is part of the MindBridge application suite. 