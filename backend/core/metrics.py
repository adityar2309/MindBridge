"""
Metrics collection and monitoring for MindBridge application.

This module provides Prometheus metrics collection for monitoring
application performance, health, and business metrics.
"""

import time
from typing import Dict, Any, Optional
from functools import wraps

from prometheus_client import (
    Counter, Histogram, Gauge, Info, 
    generate_latest, CONTENT_TYPE_LATEST
)
from fastapi import Request, Response
import structlog

logger = structlog.get_logger()

# HTTP Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently being processed',
    ['method', 'endpoint']
)

# Database Metrics
database_connections_active = Gauge(
    'database_connections_active',
    'Number of active database connections'
)

database_connections_total = Counter(
    'database_connections_total',
    'Total database connections created'
)

database_query_duration_seconds = Histogram(
    'database_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

database_errors_total = Counter(
    'database_errors_total',
    'Total database errors',
    ['operation', 'error_type']
)

# Business Metrics
checkins_created_total = Counter(
    'checkins_created_total',
    'Total number of check-ins created',
    ['user_type']
)

mood_ratings = Histogram(
    'mood_ratings',
    'Distribution of mood ratings',
    buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
)

passive_data_points_ingested = Counter(
    'passive_data_points_ingested_total',
    'Total passive data points ingested',
    ['data_type', 'source']
)

ai_insights_generated = Counter(
    'ai_insights_generated_total',
    'Total AI insights generated',
    ['insight_type', 'priority']
)

# System Metrics
application_info = Info(
    'application_info',
    'Application information'
)

memory_usage_bytes = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

# Cache Metrics
cache_operations_total = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'result']
)

cache_hit_ratio = Gauge(
    'cache_hit_ratio',
    'Cache hit ratio'
)

# Background Task Metrics
background_tasks_total = Counter(
    'background_tasks_total',
    'Total background tasks',
    ['task_type', 'status']
)

background_task_duration_seconds = Histogram(
    'background_task_duration_seconds',
    'Background task duration in seconds',
    ['task_type']
)


class MetricsCollector:
    """
    Centralized metrics collector for the application.
    
    Provides methods to record various types of metrics
    and middleware for automatic HTTP metrics collection.
    """
    
    def __init__(self):
        """Initialize the metrics collector."""
        self.start_time = time.time()
        self._cache_stats = {"hits": 0, "misses": 0}
        
        # Set application info
        application_info.info({
            'version': '1.0.0',
            'environment': 'production',
            'service': 'mindbridge-backend'
        })
    
    def record_http_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """
        Record HTTP request metrics.
        
        Args:
            method: HTTP method.
            endpoint: API endpoint.
            status_code: HTTP status code.
            duration: Request duration in seconds.
        """
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
    
    def record_database_query(self, operation: str, table: str, duration: float, success: bool = True):
        """
        Record database query metrics.
        
        Args:
            operation: Database operation (SELECT, INSERT, etc.).
            table: Database table name.
            duration: Query duration in seconds.
            success: Whether the query was successful.
        """
        database_query_duration_seconds.labels(
            operation=operation,
            table=table
        ).observe(duration)
        
        if not success:
            database_errors_total.labels(
                operation=operation,
                error_type="query_error"
            ).inc()
    
    def record_checkin_created(self, user_type: str = "regular"):
        """
        Record check-in creation.
        
        Args:
            user_type: Type of user creating the check-in.
        """
        checkins_created_total.labels(user_type=user_type).inc()
    
    def record_mood_rating(self, rating: float):
        """
        Record mood rating.
        
        Args:
            rating: Mood rating value.
        """
        mood_ratings.observe(rating)
    
    def record_passive_data_ingestion(self, data_type: str, source: str):
        """
        Record passive data point ingestion.
        
        Args:
            data_type: Type of data being ingested.
            source: Source of the data.
        """
        passive_data_points_ingested.labels(
            data_type=data_type,
            source=source
        ).inc()
    
    def record_ai_insight(self, insight_type: str, priority: str):
        """
        Record AI insight generation.
        
        Args:
            insight_type: Type of insight generated.
            priority: Priority level of the insight.
        """
        ai_insights_generated.labels(
            insight_type=insight_type,
            priority=priority
        ).inc()
    
    def record_cache_operation(self, operation: str, hit: bool):
        """
        Record cache operation.
        
        Args:
            operation: Cache operation (get, set, delete).
            hit: Whether it was a cache hit.
        """
        result = "hit" if hit else "miss"
        cache_operations_total.labels(
            operation=operation,
            result=result
        ).inc()
        
        # Update cache stats
        if operation == "get":
            if hit:
                self._cache_stats["hits"] += 1
            else:
                self._cache_stats["misses"] += 1
            
            # Update hit ratio
            total = self._cache_stats["hits"] + self._cache_stats["misses"]
            if total > 0:
                ratio = self._cache_stats["hits"] / total
                cache_hit_ratio.set(ratio)
    
    def record_background_task(self, task_type: str, status: str, duration: Optional[float] = None):
        """
        Record background task execution.
        
        Args:
            task_type: Type of background task.
            status: Task status (success, failure, etc.).
            duration: Task duration in seconds.
        """
        background_tasks_total.labels(
            task_type=task_type,
            status=status
        ).inc()
        
        if duration is not None:
            background_task_duration_seconds.labels(
                task_type=task_type
            ).observe(duration)
    
    def update_system_metrics(self):
        """Update system-level metrics."""
        import psutil
        
        # Memory usage
        process = psutil.Process()
        memory_usage_bytes.set(process.memory_info().rss)
        
        # Database connections (if available)
        try:
            # This would need to be implemented based on your connection pool
            # database_connections_active.set(connection_pool.active_connections)
            pass
        except Exception:
            pass
    
    async def middleware(self, request: Request, call_next):
        """
        FastAPI middleware for automatic metrics collection.
        
        Args:
            request: FastAPI request object.
            call_next: Next middleware/endpoint function.
            
        Returns:
            Response with metrics recorded.
        """
        start_time = time.time()
        method = request.method
        endpoint = request.url.path
        
        # Track requests in progress
        http_requests_in_progress.labels(
            method=method,
            endpoint=endpoint
        ).inc()
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            logger.error("Request failed", error=str(e), method=method, endpoint=endpoint)
            status_code = 500
            raise
        finally:
            # Record metrics
            duration = time.time() - start_time
            self.record_http_request(method, endpoint, status_code, duration)
            
            # Decrement in-progress counter
            http_requests_in_progress.labels(
                method=method,
                endpoint=endpoint
            ).dec()
        
        return response


def timed_operation(operation_type: str, table: Optional[str] = None):
    """
    Decorator to time database operations.
    
    Args:
        operation_type: Type of operation being timed.
        table: Database table being operated on.
        
    Returns:
        Decorator function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                logger.error(
                    "Database operation failed",
                    operation=operation_type,
                    table=table,
                    error=str(e)
                )
                raise
            finally:
                duration = time.time() - start_time
                metrics_collector.record_database_query(
                    operation_type,
                    table or "unknown",
                    duration,
                    success
                )
        
        return wrapper
    return decorator


# Global metrics collector instance
metrics_collector = MetricsCollector()


def get_metrics():
    """
    Get Prometheus metrics in the correct format.
    
    Returns:
        Prometheus metrics data.
    """
    # Update system metrics before generating
    metrics_collector.update_system_metrics()
    
    return generate_latest() 
