# Changelog

All notable changes to MindBridge will be documented in this file.

## [2024-01-13] - Dashboard Validation Fix & Docker Setup

### Fixed
- **🐛 Dashboard Validation Error**: Fixed FastAPI routing conflict where `/api/v1/checkins/analytics` was incorrectly parsed as `/api/v1/checkins/{checkin_id}` with "analytics" as the ID parameter
  - Moved specific routes (`/analytics/`, `/trends/`, `/today/`, `/streak/`) before the generic `/{checkin_id}` route
  - This resolves the "Request validation failed: Input should be a valid integer, unable to parse string as an integer" error

### Added
- **🐳 Comprehensive Docker Setup**: Complete Docker Compose configuration with:
  - PostgreSQL database with automatic schema initialization
  - Redis for caching and background tasks
  - Backend API with hot reload for development
  - Celery workers and beat scheduler
  - Prometheus + Grafana monitoring stack
- **📚 Enhanced Documentation**: 
  - Updated README with Docker-first approach
  - Added quick start scripts (`start.sh` for Linux/Mac, `start.bat` for Windows)
  - Comprehensive Docker development workflow documentation
  - Fixed API examples with correct `user_id` parameters
- **🧪 Docker-based Testing**: Updated all testing instructions to use Docker containers

### Changed
- **📖 README Structure**: Reorganized to prioritize Docker Compose setup over manual installation
- **🔧 Development Workflow**: Docker is now the recommended development environment
- **📊 API Examples**: Updated all endpoint examples to include required `user_id` query parameters

### Technical Details
- **Route Order Fix**: Specific routes must be defined before parameterized routes in FastAPI
- **Database**: Auto-initializes with `schema.sql` on first startup
- **Monitoring**: Grafana dashboards available at http://localhost:3001 (admin/admin)
- **API Documentation**: Interactive docs at http://localhost:8000/docs

### Migration Guide
If upgrading from manual setup:
1. Stop any running uvicorn processes
2. Run `docker-compose up -d` to start with Docker
3. Database and Redis are now containerized
4. All previous API endpoints work the same, just ensure `user_id` parameter is included

### Testing the Fix
```bash
# Quick test
docker-compose up -d
curl "http://localhost:8000/api/v1/checkins/analytics?user_id=1&period=weekly"
# Should return 200 OK instead of 422 validation error
``` 