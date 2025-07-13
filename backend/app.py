"""
MindBridge Backend - Flask API for mood and mental health tracking
Provides RESTful API endpoints for check-ins, mood quizzes, AI copilot, and chat functionality.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.before_request
def handle_json_errors():
    """Handle JSON parsing errors globally."""
    if request.content_type == 'application/json':
        try:
            if request.data:
                json.loads(request.data)
        except json.JSONDecodeError:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON format'
            }), 400

# Database configuration
DB_NAME = 'mindbridge.db'

# Pre-defined mood quiz questions
MOOD_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "How do you feel about starting your day?",
        "options": ["Energized", "Neutral", "Tired", "Anxious"]
    },
    {
        "id": 2,
        "question": "What best describes your current outlook?",
        "options": ["Optimistic", "Cautious", "Worried", "Hopeful"]
    },
    {
        "id": 3,
        "question": "How would you rate your social connections today?",
        "options": ["Strong", "Adequate", "Weak", "Isolated"]
    },
    {
        "id": 4,
        "question": "What's your current stress level?",
        "options": ["Very Low", "Low", "Moderate", "High"]
    },
    {
        "id": 5,
        "question": "How satisfied are you with your recent accomplishments?",
        "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied"]
    }
]

# Pre-defined grounding exercises and micro-lessons
GROUNDING_EXERCISES = {
    "grounding": """Try the 5-4-3-2-1 grounding technique:
• 5 things you can see around you
• 4 things you can touch
• 3 things you can hear
• 2 things you can smell
• 1 thing you can taste

This helps bring your attention to the present moment.""",
    
    "breathing": """Let's practice deep breathing:
1. Inhale slowly through your nose for 4 counts
2. Hold your breath for 4 counts
3. Exhale slowly through your mouth for 6 counts
4. Repeat 3-5 times

This activates your body's relaxation response.""",
    
    "mindfulness": """Here's a simple mindfulness exercise:
• Sit comfortably and close your eyes
• Focus on your breath without changing it
• When your mind wanders, gently bring attention back to breathing
• Start with 2-3 minutes and gradually increase

Regular practice improves emotional regulation.""",
    
    "default": """Here are some general wellness tips:
• Take regular breaks throughout your day
• Stay hydrated and eat nutritious meals
• Get adequate sleep (7-9 hours)
• Practice gratitude by noting 3 good things daily
• Connect with supportive people in your life"""
}

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Create checkins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                stress_level INTEGER NOT NULL,
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database {DB_NAME} initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def get_db_connection():
    """Get a database connection with row factory for easier data access."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/checkin', methods=['GET'])
def get_checkins():
    """
    Retrieve the last 5 mood check-ins from the database.
    
    Returns:
        JSON response with checkins data or error message
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, mood, stress_level, notes, timestamp 
            FROM checkins 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        
        checkins = cursor.fetchall()
        conn.close()
        
        # Convert rows to dictionaries
        checkins_list = []
        for checkin in checkins:
            checkins_list.append({
                'id': checkin['id'],
                'mood': checkin['mood'],
                'stress_level': checkin['stress_level'],
                'notes': checkin['notes'],
                'timestamp': checkin['timestamp']
            })
        
        return jsonify({
            'success': True,
            'checkins': checkins_list
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve check-ins: {str(e)}'
        }), 500

@app.route('/api/checkin', methods=['POST'])
def submit_checkin():
    """
    Submit a new mood check-in to the database.
    
    Expected JSON payload:
        {
            "mood": "Happy" | "Neutral" | "Sad" | "1-5",
            "stress_level": 1-10,
            "notes": "Optional notes text"
        }
    
    Returns:
        JSON response with success status and message
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        mood = data.get('mood')
        stress_level = data.get('stress_level')
        notes = data.get('notes', '')
        
        if not mood or stress_level is None:
            return jsonify({
                'success': False,
                'error': 'Mood and stress_level are required'
            }), 400
        
        # Validate stress level range
        if not isinstance(stress_level, int) or stress_level < 1 or stress_level > 10:
            return jsonify({
                'success': False,
                'error': 'Stress level must be an integer between 1 and 10'
            }), 400
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO checkins (mood, stress_level, notes) 
            VALUES (?, ?, ?)
        ''', (mood, stress_level, notes))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Check-in submitted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to submit check-in: {str(e)}'
        }), 500

@app.route('/api/mood_quiz/generate', methods=['GET'])
def generate_mood_quiz():
    """
    Generate a mood quiz question.
    
    Returns:
        JSON response with a quiz question and options
    """
    try:
        import random
        
        # Select a random question from the pre-defined list
        question = random.choice(MOOD_QUIZ_QUESTIONS)
        
        return jsonify({
            'success': True,
            'question': question
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate quiz: {str(e)}'
        }), 500

@app.route('/api/mood_quiz/submit', methods=['POST'])
def submit_mood_quiz():
    """
    Submit a mood quiz answer and get insight.
    
    Expected JSON payload:
        {
            "question_id": 1,
            "answer": "Selected option text"
        }
    
    Returns:
        JSON response with mood insight based on the answer
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        answer = data.get('answer')
        question_id = data.get('question_id')
        
        if not answer:
            return jsonify({
                'success': False,
                'error': 'Answer is required'
            }), 400
        
        # Log the answer (for debugging)
        print(f"Quiz answer received - Question ID: {question_id}, Answer: {answer}")
        
        # Generate insight based on answer
        insight = generate_mood_insight(answer)
        
        return jsonify({
            'success': True,
            'insight': insight
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to submit quiz answer: {str(e)}'
        }), 500

def generate_mood_insight(answer):
    """
    Generate a simple mood insight based on the quiz answer.
    
    Args:
        answer (str): The selected answer from the quiz
    
    Returns:
        str: A personalized insight message
    """
    answer_lower = answer.lower()
    
    # Check concerning responses first (to catch "dissatisfied" before "satisfied")
    if any(word in answer_lower for word in ['tired', 'anxious', 'worried', 'isolated', 'dissatisfied', 'high']):
        return "It sounds like you might be going through a challenging time. Remember to be kind to yourself and consider reaching out for support."
    
    # Positive responses
    elif any(word in answer_lower for word in ['energized', 'optimistic', 'strong', 'satisfied', 'hopeful']):
        return "You're showing positive energy and outlook! Keep nurturing this mindset."
    
    # Neutral responses
    elif any(word in answer_lower for word in ['neutral', 'adequate', 'cautious']):
        return "You're in a balanced state. Consider what might help you feel more energized."
    
    # Default response
    else:
        return "Thanks for sharing your thoughts. Self-reflection is an important part of mental wellness."

@app.route('/api/copilot/grounding', methods=['POST'])
def get_grounding_exercise():
    """
    Get a grounding exercise or micro-lesson based on the user's prompt.
    
    Expected JSON payload:
        {
            "prompt": "User's request text"
        }
    
    Returns:
        JSON response with a grounding exercise or helpful content
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        prompt = data.get('prompt', '').lower()
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            }), 400
        
        # Match keywords to appropriate exercises
        if 'grounding' in prompt:
            exercise = GROUNDING_EXERCISES['grounding']
        elif any(word in prompt for word in ['breathing', 'breath', 'breathe']):
            exercise = GROUNDING_EXERCISES['breathing']
        elif any(word in prompt for word in ['mindfulness', 'meditation', 'calm']):
            exercise = GROUNDING_EXERCISES['mindfulness']
        else:
            exercise = GROUNDING_EXERCISES['default']
        
        return jsonify({
            'success': True,
            'exercise': exercise
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get grounding exercise: {str(e)}'
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_response():
    """
    Generate a conversational response based on the user's message.
    
    Expected JSON payload:
        {
            "message": "User's message text"
        }
    
    Returns:
        JSON response with an appropriate conversational reply
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        message = data.get('message', '').lower()
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Generate response based on message content
        response = generate_chat_response(message)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate chat response: {str(e)}'
        }), 500

def generate_chat_response(message):
    """
    Generate a rule-based conversational response.
    
    Args:
        message (str): User's message in lowercase
    
    Returns:
        str: Appropriate response based on message content
    """
    # Sad/down responses
    if any(word in message for word in ['sad', 'down', 'depressed', 'upset', 'hurt']):
        return "I'm sorry to hear that you're feeling this way. It's completely normal to have difficult emotions. Remember to be kind to yourself during tough times. Is there anything specific that's been weighing on you?"
    
    # Stressed/anxious responses
    elif any(word in message for word in ['stressed', 'anxious', 'worried', 'overwhelmed', 'panic']):
        return "Stress and anxiety can be really tough to deal with. Try taking a few deep breaths - in through your nose for 4 counts, hold for 4, and out through your mouth for 6. Remember that this feeling will pass. What's been causing you the most stress lately?"
    
    # Happy/positive responses
    elif any(word in message for word in ['happy', 'good', 'great', 'excited', 'joy']):
        return "I'm so glad to hear you're feeling positive! It's wonderful when we can appreciate the good moments. What's been going well for you recently?"
    
    # Tired/exhausted responses
    elif any(word in message for word in ['tired', 'exhausted', 'sleepy', 'drained']):
        return "It sounds like you might need some rest. Make sure you're getting enough sleep and taking breaks when you need them. Self-care isn't selfish - it's necessary. Have you been able to get enough rest lately?"
    
    # Angry/frustrated responses
    elif any(word in message for word in ['angry', 'mad', 'frustrated', 'annoyed']):
        return "Anger and frustration are valid emotions. It's okay to feel this way. Try to take some time to process these feelings safely. Deep breathing or physical activity can sometimes help. What's been frustrating you?"
    
    # Lonely responses
    elif any(word in message for word in ['lonely', 'alone', 'isolated']):
        return "Feeling lonely can be really difficult. Remember that you're not truly alone, even when it feels that way. Consider reaching out to someone you trust or engaging in activities that connect you with others. I'm here to listen too."
    
    # Help/support requests
    elif any(word in message for word in ['help', 'support', 'advice', 'guidance']):
        return "I'm here to support you. While I can provide general wellness tips and a listening ear, remember that professional help is available if you need more support. What kind of help are you looking for today?"
    
    # Gratitude/thanks
    elif any(word in message for word in ['thank', 'grateful', 'appreciate']):
        return "You're very welcome! I'm glad I could be helpful. Practicing gratitude, like you're doing right now, is actually great for mental health. Keep being kind to yourself."
    
    # Default response
    else:
        return "Thank you for sharing that with me. I'm here to listen and provide support. How are you feeling right now? Is there anything specific I can help you with today?"

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify the API is running.
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'MindBridge API is running'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors with JSON response."""
    return jsonify({
        'success': False,
        'error': 'Bad request'
    }), 400

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with JSON response."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000) 