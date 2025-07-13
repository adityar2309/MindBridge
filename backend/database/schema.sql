-- MindBridge Database Schema
-- SQL DDL statements for all database tables

-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    settings JSONB DEFAULT '{
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
    }'::jsonb,
    last_login TIMESTAMP,
    timezone VARCHAR(50) DEFAULT 'UTC',
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);
CREATE INDEX idx_users_registration_date ON users(registration_date);

-- Daily check-ins table
CREATE TABLE daily_checkins (
    checkin_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    mood_rating DECIMAL(3,2) NOT NULL CHECK (mood_rating >= 1.0 AND mood_rating <= 10.0),
    mood_category VARCHAR(50),
    keywords JSONB DEFAULT '[]'::jsonb,
    notes TEXT,
    location VARCHAR(100),
    weather VARCHAR(50),
    energy_level DECIMAL(3,2) CHECK (energy_level >= 1.0 AND energy_level <= 10.0),
    stress_level DECIMAL(3,2) CHECK (stress_level >= 1.0 AND stress_level <= 10.0),
    sleep_quality DECIMAL(3,2) CHECK (sleep_quality >= 1.0 AND sleep_quality <= 10.0),
    social_interaction DECIMAL(3,2) CHECK (social_interaction >= 1.0 AND social_interaction <= 10.0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for daily_checkins table
CREATE INDEX idx_daily_checkins_user_id ON daily_checkins(user_id);
CREATE INDEX idx_daily_checkins_timestamp ON daily_checkins(timestamp);
CREATE INDEX idx_daily_checkins_mood_rating ON daily_checkins(mood_rating);
CREATE INDEX idx_daily_checkins_mood_category ON daily_checkins(mood_category);
CREATE UNIQUE INDEX idx_daily_checkins_user_date ON daily_checkins(user_id, DATE(timestamp));

-- Passive data points table
CREATE TABLE passive_data_points (
    data_point_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    value JSONB NOT NULL,
    source VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    quality_score DECIMAL(3,2) DEFAULT 1.0 CHECK (quality_score >= 0.0 AND quality_score <= 1.0),
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for passive_data_points table
CREATE INDEX idx_passive_data_user_id ON passive_data_points(user_id);
CREATE INDEX idx_passive_data_timestamp ON passive_data_points(timestamp);
CREATE INDEX idx_passive_data_type ON passive_data_points(data_type);
CREATE INDEX idx_passive_data_source ON passive_data_points(source);
CREATE INDEX idx_passive_data_processed ON passive_data_points(processed);
CREATE INDEX idx_passive_data_quality ON passive_data_points(quality_score);

-- Quiz questions table
CREATE TABLE quiz_questions (
    question_id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    options JSONB,
    min_value DECIMAL(10,2),
    max_value DECIMAL(10,2),
    category VARCHAR(50) NOT NULL,
    tags JSONB DEFAULT '[]'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    expected_response_time INTEGER DEFAULT 30 CHECK (expected_response_time >= 5 AND expected_response_time <= 300),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for quiz_questions table
CREATE INDEX idx_quiz_questions_category ON quiz_questions(category);
CREATE INDEX idx_quiz_questions_type ON quiz_questions(question_type);
CREATE INDEX idx_quiz_questions_is_active ON quiz_questions(is_active);
CREATE INDEX idx_quiz_questions_difficulty ON quiz_questions(difficulty_level);

-- Quiz sessions table
CREATE TABLE quiz_sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    quiz_type VARCHAR(50) NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    completion_rate DECIMAL(5,2) DEFAULT 0.0 CHECK (completion_rate >= 0.0 AND completion_rate <= 100.0),
    final_mood_score DECIMAL(3,2) CHECK (final_mood_score >= 1.0 AND final_mood_score <= 10.0),
    session_context JSONB DEFAULT '{}'::jsonb,
    adaptive_flow BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for quiz_sessions table
CREATE INDEX idx_quiz_sessions_user_id ON quiz_sessions(user_id);
CREATE INDEX idx_quiz_sessions_quiz_type ON quiz_sessions(quiz_type);
CREATE INDEX idx_quiz_sessions_start_time ON quiz_sessions(start_time);
CREATE INDEX idx_quiz_sessions_completion_rate ON quiz_sessions(completion_rate);

-- Quiz responses table
CREATE TABLE quiz_responses (
    response_id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES quiz_sessions(session_id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES quiz_questions(question_id) ON DELETE CASCADE,
    user_answer JSONB NOT NULL,
    response_time DECIMAL(10,2),
    confidence_score DECIMAL(3,2) CHECK (confidence_score >= 1.0 AND confidence_score <= 10.0),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for quiz_responses table
CREATE INDEX idx_quiz_responses_session_id ON quiz_responses(session_id);
CREATE INDEX idx_quiz_responses_question_id ON quiz_responses(question_id);
CREATE INDEX idx_quiz_responses_timestamp ON quiz_responses(timestamp);
CREATE INDEX idx_quiz_responses_response_time ON quiz_responses(response_time);

-- AI mood insights table
CREATE TABLE ai_mood_insights (
    insight_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    insight_type VARCHAR(50) NOT NULL,
    mood_score_prediction DECIMAL(3,2) CHECK (mood_score_prediction >= 1.0 AND mood_score_prediction <= 10.0),
    confidence_score DECIMAL(3,2) NOT NULL CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    contributing_factors JSONB DEFAULT '[]'::jsonb,
    recommendation TEXT,
    recommendation_type VARCHAR(50),
    priority_level VARCHAR(20) DEFAULT 'medium' CHECK (priority_level IN ('low', 'medium', 'high', 'urgent')),
    is_actionable BOOLEAN DEFAULT TRUE,
    feedback_score DECIMAL(3,2) CHECK (feedback_score >= 1.0 AND feedback_score <= 5.0),
    model_version VARCHAR(50),
    data_sources JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for ai_mood_insights table
CREATE INDEX idx_ai_insights_user_id ON ai_mood_insights(user_id);
CREATE INDEX idx_ai_insights_timestamp ON ai_mood_insights(timestamp);
CREATE INDEX idx_ai_insights_insight_type ON ai_mood_insights(insight_type);
CREATE INDEX idx_ai_insights_priority ON ai_mood_insights(priority_level);
CREATE INDEX idx_ai_insights_confidence ON ai_mood_insights(confidence_score);
CREATE INDEX idx_ai_insights_is_actionable ON ai_mood_insights(is_actionable);

-- Conversation logs table
CREATE TABLE conversation_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    session_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    context_data JSONB DEFAULT '{}'::jsonb,
    response_quality DECIMAL(3,2) CHECK (response_quality >= 1.0 AND response_quality <= 5.0),
    user_feedback VARCHAR(20) CHECK (user_feedback IN ('positive', 'negative', 'neutral')),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for conversation_logs table
CREATE INDEX idx_conversation_logs_user_id ON conversation_logs(user_id);
CREATE INDEX idx_conversation_logs_session_id ON conversation_logs(session_id);
CREATE INDEX idx_conversation_logs_timestamp ON conversation_logs(timestamp);
CREATE INDEX idx_conversation_logs_user_feedback ON conversation_logs(user_feedback);

-- Create triggers for updating updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_daily_checkins_updated_at BEFORE UPDATE ON daily_checkins FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_passive_data_points_updated_at BEFORE UPDATE ON passive_data_points FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_quiz_questions_updated_at BEFORE UPDATE ON quiz_questions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_quiz_sessions_updated_at BEFORE UPDATE ON quiz_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_quiz_responses_updated_at BEFORE UPDATE ON quiz_responses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ai_mood_insights_updated_at BEFORE UPDATE ON ai_mood_insights FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_conversation_logs_updated_at BEFORE UPDATE ON conversation_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for commonly accessed data

-- User summary view
CREATE VIEW user_summary AS
SELECT 
    u.user_id,
    u.name,
    u.email,
    u.registration_date,
    u.is_active,
    u.last_login,
    COUNT(DISTINCT dc.checkin_id) as total_checkins,
    AVG(dc.mood_rating) as avg_mood_rating,
    COUNT(DISTINCT qs.session_id) as total_quiz_sessions,
    COUNT(DISTINCT ai.insight_id) as total_insights
FROM users u
LEFT JOIN daily_checkins dc ON u.user_id = dc.user_id
LEFT JOIN quiz_sessions qs ON u.user_id = qs.user_id
LEFT JOIN ai_mood_insights ai ON u.user_id = ai.user_id
GROUP BY u.user_id, u.name, u.email, u.registration_date, u.is_active, u.last_login;

-- Daily mood summary view
CREATE VIEW daily_mood_summary AS
SELECT 
    user_id,
    DATE(timestamp) as date,
    AVG(mood_rating) as avg_mood,
    MIN(mood_rating) as min_mood,
    MAX(mood_rating) as max_mood,
    COUNT(*) as checkin_count,
    AVG(energy_level) as avg_energy,
    AVG(stress_level) as avg_stress,
    AVG(sleep_quality) as avg_sleep_quality
FROM daily_checkins
GROUP BY user_id, DATE(timestamp);

-- Passive data summary view
CREATE VIEW passive_data_summary AS
SELECT 
    user_id,
    data_type,
    source,
    DATE(timestamp) as date,
    COUNT(*) as data_point_count,
    AVG(quality_score) as avg_quality,
    COUNT(CASE WHEN processed = true THEN 1 END) as processed_count
FROM passive_data_points
GROUP BY user_id, data_type, source, DATE(timestamp);

-- Quiz performance view
CREATE VIEW quiz_performance AS
SELECT 
    qs.user_id,
    qs.quiz_type,
    COUNT(DISTINCT qs.session_id) as session_count,
    AVG(qs.completion_rate) as avg_completion_rate,
    AVG(qs.final_mood_score) as avg_final_mood,
    AVG(qr.response_time) as avg_response_time,
    COUNT(qr.response_id) as total_responses
FROM quiz_sessions qs
LEFT JOIN quiz_responses qr ON qs.session_id = qr.session_id
GROUP BY qs.user_id, qs.quiz_type;

-- Insert sample quiz questions
INSERT INTO quiz_questions (question_text, question_type, category, tags, difficulty_level) VALUES
('How are you feeling right now?', 'slider', 'mood', '["general", "current"]', 1),
('What''s your energy level today?', 'slider', 'energy', '["daily", "physical"]', 1),
('How stressed do you feel?', 'slider', 'stress', '["mental", "current"]', 1),
('Rate your sleep quality last night', 'slider', 'sleep', '["rest", "quality"]', 1),
('How was your social interaction today?', 'slider', 'social', '["connection", "daily"]', 1),
('What activities did you enjoy today?', 'checkbox', 'activities', '["enjoyment", "daily"]', 2),
('How would you describe your mood in one word?', 'open_text', 'mood', '["descriptive", "current"]', 2),
('Are you feeling overwhelmed right now?', 'yes_no', 'stress', '["overwhelm", "current"]', 1),
('What''s causing you the most stress today?', 'multiple_choice', 'stress', '["causes", "daily"]', 2),
('How motivated do you feel to complete tasks?', 'likert_scale', 'motivation', '["productivity", "current"]', 2);

-- Update quiz questions with options for appropriate question types
UPDATE quiz_questions 
SET options = '["Exercise", "Reading", "Music", "Social time", "Cooking", "Gaming", "Art/Creativity", "Nature/Outdoors"]'::jsonb
WHERE question_text = 'What activities did you enjoy today?';

UPDATE quiz_questions 
SET options = '["Work/Career", "Relationships", "Health", "Finances", "Family", "School/Education", "Future plans", "Current events"]'::jsonb
WHERE question_text = 'What''s causing you the most stress today?';

UPDATE quiz_questions 
SET min_value = 1.0, max_value = 10.0
WHERE question_type = 'slider';

UPDATE quiz_questions 
SET min_value = 1.0, max_value = 5.0
WHERE question_type = 'likert_scale';

-- Grant permissions (adjust as needed for your environment)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mindbridge_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mindbridge_user; 