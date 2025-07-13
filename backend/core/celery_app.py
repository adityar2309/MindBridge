"""
Celery application configuration for MindBridge background tasks.

This module configures Celery for handling asynchronous tasks
like data processing, AI insights generation, and notifications.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Configure Celery
celery_app = Celery(
    "mindbridge",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    include=[
        "backend.core.tasks.data_processing",
        "backend.core.tasks.ai_insights",
        "backend.core.tasks.notifications"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_backend_transport_options={
        "master_name": "mymaster",
        "retry_on_timeout": True,
    },
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Beat schedule
    beat_schedule={
        "process_passive_data": {
            "task": "backend.core.tasks.data_processing.process_unprocessed_data",
            "schedule": crontab(minute="*/15"),  # Every 15 minutes
        },
        "generate_daily_insights": {
            "task": "backend.core.tasks.ai_insights.generate_daily_insights",
            "schedule": crontab(hour=8, minute=0),  # Daily at 8 AM UTC
        },
        "send_reminder_notifications": {
            "task": "backend.core.tasks.notifications.send_daily_reminders",
            "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM UTC
        },
        "cleanup_old_data": {
            "task": "backend.core.tasks.data_processing.cleanup_old_data",
            "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM UTC
        },
    },
) 
