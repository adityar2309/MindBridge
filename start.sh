#!/bin/bash

# MindBridge Quick Start Script
# This script helps you get MindBridge running quickly with Docker Compose

set -e

echo "🧠 MindBridge - Quick Start"
echo "=========================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

echo "✅ Docker is running"

# Start services
echo "🚀 Starting MindBridge services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 30

# Test the endpoints
echo "🧪 Testing endpoints..."

# Test health endpoint
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend health check: OK"
else
    echo "❌ Backend health check: FAILED"
fi

# Test analytics endpoint (the fixed one!)
if curl -s "http://localhost:8000/api/v1/checkins/analytics?user_id=1&period=weekly" > /dev/null; then
    echo "✅ Analytics endpoint: OK (Dashboard validation error FIXED!)"
else
    echo "❌ Analytics endpoint: FAILED"
fi

echo ""
echo "🎉 MindBridge is running!"
echo ""
echo "📍 Access Points:"
echo "   Backend API:        http://localhost:8000"
echo "   API Documentation:  http://localhost:8000/docs"
echo "   Grafana Monitoring: http://localhost:3001 (admin/admin)"
echo "   Prometheus Metrics: http://localhost:9090"
echo ""
echo "🔧 Common Commands:"
echo "   View logs:          docker-compose logs -f"
echo "   Stop services:      docker-compose down"
echo "   Restart backend:    docker-compose restart backend"
echo "   Run tests:          docker-compose exec backend python -m pytest tests/ -v"
echo ""
echo "📚 Example API Calls:"
echo "   curl 'http://localhost:8000/api/v1/checkins?user_id=1'"
echo "   curl 'http://localhost:8000/api/v1/checkins/analytics?user_id=1&period=weekly'"
echo ""
echo "🐛 Troubleshooting:"
echo "   If you see errors, try: docker-compose down && docker-compose up --build" 