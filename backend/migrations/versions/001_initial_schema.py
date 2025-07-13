"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    
    # Enable UUID extension for PostgreSQL
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('registration_date', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('settings', postgresql.JSONB(), nullable=True, server_default=sa.text("""'{
            "notifications": {
                "daily_reminder": true,
                "weekly_summary": true,
                "mood_alerts": true,
                "reminder_time": "09:00"
            },
            "privacy": {
                "data_sharing": false,
                "anonymous_analytics": true
            },
            "ui": {
                "theme": "auto",
                "font_size": "medium",
                "animations": true
            }
        }'::jsonb""")),
        sa.Column('last_login', sa.TIMESTAMP(), nullable=True),
        sa.Column('timezone', sa.String(50), nullable=True, server_default='UTC'),
        sa.Column('language', sa.String(10), nullable=True, server_default='en'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create indexes for users table
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_is_active', 'users', ['is_active'])
    op.create_index('idx_users_registration_date', 'users', ['registration_date'])
    
    # Daily check-ins table
    op.create_table(
        'daily_checkins',
        sa.Column('checkin_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('mood_rating', sa.DECIMAL(3, 2), nullable=False),
        sa.Column('mood_category', sa.String(50), nullable=True),
        sa.Column('keywords', postgresql.JSONB(), nullable=True, server_default=sa.text("'[]'::jsonb")),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('weather', sa.String(50), nullable=True),
        sa.Column('energy_level', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('stress_level', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('sleep_quality', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('social_interaction', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.CheckConstraint('mood_rating >= 1.0 AND mood_rating <= 10.0', name='chk_mood_rating'),
        sa.CheckConstraint('energy_level >= 1.0 AND energy_level <= 10.0', name='chk_energy_level'),
        sa.CheckConstraint('stress_level >= 1.0 AND stress_level <= 10.0', name='chk_stress_level'),
        sa.CheckConstraint('sleep_quality >= 1.0 AND sleep_quality <= 10.0', name='chk_sleep_quality'),
        sa.CheckConstraint('social_interaction >= 1.0 AND social_interaction <= 10.0', name='chk_social_interaction')
    )
    
    # Create indexes for daily_checkins table
    op.create_index('idx_daily_checkins_user_id', 'daily_checkins', ['user_id'])
    op.create_index('idx_daily_checkins_timestamp', 'daily_checkins', ['timestamp'])
    op.create_index('idx_daily_checkins_mood_rating', 'daily_checkins', ['mood_rating'])
    op.create_index('idx_daily_checkins_mood_category', 'daily_checkins', ['mood_category'])
    op.create_unique_index('idx_daily_checkins_user_date', 'daily_checkins', [
        'user_id', 
        sa.text('DATE(timestamp)')
    ])
    
    # Passive data points table
    op.create_table(
        'passive_data_points',
        sa.Column('data_point_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_type', sa.String(50), nullable=False),
        sa.Column('value', postgresql.JSONB(), nullable=False),
        sa.Column('source', sa.String(50), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column('quality_score', sa.DECIMAL(3, 2), nullable=True, server_default='1.0'),
        sa.Column('processed', sa.Boolean(), nullable=True, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.CheckConstraint('quality_score >= 0.0 AND quality_score <= 1.0', name='chk_quality_score')
    )
    
    # Create indexes for passive_data_points table
    op.create_index('idx_passive_data_user_id', 'passive_data_points', ['user_id'])
    op.create_index('idx_passive_data_timestamp', 'passive_data_points', ['timestamp'])
    op.create_index('idx_passive_data_type', 'passive_data_points', ['data_type'])
    op.create_index('idx_passive_data_source', 'passive_data_points', ['source'])
    op.create_index('idx_passive_data_processed', 'passive_data_points', ['processed'])
    op.create_index('idx_passive_data_quality', 'passive_data_points', ['quality_score'])
    
    # Quiz questions table
    op.create_table(
        'quiz_questions',
        sa.Column('question_id', sa.Integer(), primary_key=True),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('question_type', sa.String(50), nullable=False),
        sa.Column('options', postgresql.JSONB(), nullable=True),
        sa.Column('min_value', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('max_value', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('tags', postgresql.JSONB(), nullable=True, server_default=sa.text("'[]'::jsonb")),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('TRUE')),
        sa.Column('difficulty_level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('expected_response_time', sa.Integer(), nullable=True, server_default='30'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint('difficulty_level >= 1 AND difficulty_level <= 5', name='chk_difficulty_level'),
        sa.CheckConstraint('expected_response_time >= 5 AND expected_response_time <= 300', name='chk_response_time')
    )
    
    # Create indexes for quiz_questions table
    op.create_index('idx_quiz_questions_category', 'quiz_questions', ['category'])
    op.create_index('idx_quiz_questions_type', 'quiz_questions', ['question_type'])
    op.create_index('idx_quiz_questions_is_active', 'quiz_questions', ['is_active'])
    op.create_index('idx_quiz_questions_difficulty', 'quiz_questions', ['difficulty_level'])
    
    # Quiz sessions table
    op.create_table(
        'quiz_sessions',
        sa.Column('session_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('quiz_type', sa.String(50), nullable=False),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
        sa.Column('completion_rate', sa.DECIMAL(5, 2), nullable=True, server_default='0.0'),
        sa.Column('final_mood_score', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('session_context', postgresql.JSONB(), nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column('adaptive_flow', sa.Boolean(), nullable=True, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.CheckConstraint('completion_rate >= 0.0 AND completion_rate <= 100.0', name='chk_completion_rate'),
        sa.CheckConstraint('final_mood_score >= 1.0 AND final_mood_score <= 10.0', name='chk_final_mood_score')
    )
    
    # Create indexes for quiz_sessions table
    op.create_index('idx_quiz_sessions_user_id', 'quiz_sessions', ['user_id'])
    op.create_index('idx_quiz_sessions_quiz_type', 'quiz_sessions', ['quiz_type'])
    op.create_index('idx_quiz_sessions_start_time', 'quiz_sessions', ['start_time'])
    op.create_index('idx_quiz_sessions_completion_rate', 'quiz_sessions', ['completion_rate'])
    
    # Quiz responses table
    op.create_table(
        'quiz_responses',
        sa.Column('response_id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('user_answer', postgresql.JSONB(), nullable=False),
        sa.Column('response_time', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('confidence_score', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['session_id'], ['quiz_sessions.session_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.question_id'], ondelete='CASCADE'),
        sa.CheckConstraint('confidence_score >= 1.0 AND confidence_score <= 10.0', name='chk_confidence_score')
    )
    
    # Create indexes for quiz_responses table
    op.create_index('idx_quiz_responses_session_id', 'quiz_responses', ['session_id'])
    op.create_index('idx_quiz_responses_question_id', 'quiz_responses', ['question_id'])
    op.create_index('idx_quiz_responses_timestamp', 'quiz_responses', ['timestamp'])
    op.create_index('idx_quiz_responses_response_time', 'quiz_responses', ['response_time'])
    
    # AI mood insights table
    op.create_table(
        'ai_mood_insights',
        sa.Column('insight_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('insight_type', sa.String(50), nullable=False),
        sa.Column('mood_score_prediction', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('confidence_score', sa.DECIMAL(3, 2), nullable=False),
        sa.Column('contributing_factors', postgresql.JSONB(), nullable=True, server_default=sa.text("'[]'::jsonb")),
        sa.Column('recommendation', sa.Text(), nullable=True),
        sa.Column('recommendation_type', sa.String(50), nullable=True),
        sa.Column('priority_level', sa.String(20), nullable=True, server_default='medium'),
        sa.Column('is_actionable', sa.Boolean(), nullable=True, server_default=sa.text('TRUE')),
        sa.Column('feedback_score', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('model_version', sa.String(50), nullable=True),
        sa.Column('data_sources', postgresql.JSONB(), nullable=True, server_default=sa.text("'[]'::jsonb")),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.CheckConstraint('mood_score_prediction >= 1.0 AND mood_score_prediction <= 10.0', name='chk_mood_prediction'),
        sa.CheckConstraint('confidence_score >= 0.0 AND confidence_score <= 1.0', name='chk_ai_confidence_score'),
        sa.CheckConstraint("priority_level IN ('low', 'medium', 'high', 'urgent')", name='chk_priority_level'),
        sa.CheckConstraint('feedback_score >= 1.0 AND feedback_score <= 5.0', name='chk_feedback_score')
    )
    
    # Create indexes for ai_mood_insights table
    op.create_index('idx_ai_insights_user_id', 'ai_mood_insights', ['user_id'])
    op.create_index('idx_ai_insights_timestamp', 'ai_mood_insights', ['timestamp'])
    op.create_index('idx_ai_insights_insight_type', 'ai_mood_insights', ['insight_type'])
    op.create_index('idx_ai_insights_priority', 'ai_mood_insights', ['priority_level'])
    op.create_index('idx_ai_insights_confidence', 'ai_mood_insights', ['confidence_score'])
    op.create_index('idx_ai_insights_is_actionable', 'ai_mood_insights', ['is_actionable'])
    
    # Conversation logs table
    op.create_table(
        'conversation_logs',
        sa.Column('log_id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(255), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('user_message', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=False),
        sa.Column('context_data', postgresql.JSONB(), nullable=True, server_default=sa.text("'{}'::jsonb")),
        sa.Column('response_quality', sa.DECIMAL(3, 2), nullable=True),
        sa.Column('user_feedback', sa.String(20), nullable=True),
        sa.Column('model_version', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.CheckConstraint('response_quality >= 1.0 AND response_quality <= 5.0', name='chk_response_quality'),
        sa.CheckConstraint("user_feedback IN ('positive', 'negative', 'neutral')", name='chk_user_feedback')
    )
    
    # Create indexes for conversation_logs table
    op.create_index('idx_conversation_logs_user_id', 'conversation_logs', ['user_id'])
    op.create_index('idx_conversation_logs_session_id', 'conversation_logs', ['session_id'])
    op.create_index('idx_conversation_logs_timestamp', 'conversation_logs', ['timestamp'])
    op.create_index('idx_conversation_logs_user_feedback', 'conversation_logs', ['user_feedback'])


def downgrade() -> None:
    """Drop all tables and extensions."""
    
    # Drop tables in reverse order
    op.drop_table('conversation_logs')
    op.drop_table('ai_mood_insights')
    op.drop_table('quiz_responses')
    op.drop_table('quiz_sessions')
    op.drop_table('quiz_questions')
    op.drop_table('passive_data_points')
    op.drop_table('daily_checkins')
    op.drop_table('users')
    
    # Note: We don't drop the UUID extension as it might be used by other applications 