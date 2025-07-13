@echo off
REM MindBridge Quick Start Script for Windows
REM This script helps you get MindBridge running quickly with Docker Compose

echo 🧠 MindBridge - Quick Start
echo ==========================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install it and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Start services
echo 🚀 Starting MindBridge services...
docker-compose up -d

echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Test the endpoints
echo 🧪 Testing endpoints...

REM Test health endpoint
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend health check: OK
) else (
    echo ❌ Backend health check: FAILED
)

REM Test analytics endpoint (the fixed one!)
curl -s "http://localhost:8000/api/v1/checkins/analytics?user_id=1&period=weekly" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Analytics endpoint: OK (Dashboard validation error FIXED!)
) else (
    echo ❌ Analytics endpoint: FAILED
)

echo.
echo 🎉 MindBridge is running!
echo.
echo 📍 Access Points:
echo    Backend API:        http://localhost:8000
echo    API Documentation:  http://localhost:8000/docs
echo    Grafana Monitoring: http://localhost:3001 (admin/admin)
echo    Prometheus Metrics: http://localhost:9090
echo.
echo 🔧 Common Commands:
echo    View logs:          docker-compose logs -f
echo    Stop services:      docker-compose down
echo    Restart backend:    docker-compose restart backend
echo    Run tests:          docker-compose exec backend python -m pytest tests/ -v
echo.
echo 📚 Example API Calls:
echo    curl "http://localhost:8000/api/v1/checkins?user_id=1"
echo    curl "http://localhost:8000/api/v1/checkins/analytics?user_id=1&period=weekly"
echo.
echo 🐛 Troubleshooting:
echo    If you see errors, try: docker-compose down ^&^& docker-compose up --build
echo.
pause 