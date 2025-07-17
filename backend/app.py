"""
MindBridge Backend - Flask API for mood and mental health tracking
Provides RESTful API endpoints for check-ins, mood quizzes, AI copilot, and chat functionality.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import json
import os
import bcrypt
from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequest
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyANOdww8r2kz76R1IqDAahAGxHDxxNbZvs")

from sentence_transformers import SentenceTransformer
import chromadb

# Load at startup
model = SentenceTransformer("all-MiniLM-L6-v2")


client = chromadb.PersistentClient(path="vector_store")
collection = client.get_or_create_collection(name="mental_health_docs")
DB_PATH = r'C:\Users\DELL\MindBridge\backend\mindbridge.db'

def retrieve_relevant_knowledge(query, k=3):
    embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=k)
    docs = results["documents"][0]
    return "\n".join(docs)


import sqlite3
from datetime import datetime, timedelta
import datetime

def fetch_user_context(user_id):
    conn = sqlite3.connect("mindbridge.db")
    cursor = conn.cursor()

    # If your table has `timestamp`, filter by last 3 days
    three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=3)).isoformat()

    try:
        cursor.execute("""
            SELECT role, message FROM chat_logs 
            WHERE user_id = ? AND timestamp >= ? 
            ORDER BY timestamp ASC
        """, (user_id, three_days_ago))
    except sqlite3.OperationalError:
        # fallback if no timestamp column
        cursor.execute("""
            SELECT role, message FROM chat_logs 
            WHERE user_id = ? 
            ORDER BY id ASC
        """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    # Reconstruct the full conversation
    context = ""
    for role, msg in rows:
        context += f"{role.capitalize()}: {msg}\n"
    return context

def gemini_chat(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini API error:", e)
        return "Sorry, something went wrong while getting a response."


app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for all routes
@app.route("/")
def home():
    return "Welcome to MindBridge API!"


# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

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
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create checkins table with user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mood TEXT NOT NULL,
                stress_level INTEGER NOT NULL,
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        # Add below checkins table creation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dass_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                scores TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
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

def hash_password(password):
    """Hash a password for storing in the database."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    """
    Register a new user.
    
    Expected JSON payload:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        JSON response with success status and user info
    """

    if request.method == 'OPTIONS':
        return '', 204  # CORS preflight response

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({
                'success': False,
                'error': 'Username, email, and password are required'
            }), 400

        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters long'
            }), 400

        password_hash = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash) 
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))

            user_id = cursor.lastrowid
            conn.commit()

            access_token = create_access_token(identity=str(user_id))

            conn.close()

            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': {
                    'id': user_id,
                    'username': username,
                    'email': email
                }
            })

        except sqlite3.IntegrityError as e:
            conn.close()
            if 'username' in str(e):
                return jsonify({
                    'success': False,
                    'error': 'Username already exists'
                }), 409
            elif 'email' in str(e):
                return jsonify({
                    'success': False,
                    'error': 'Email already exists'
                }), 409
            else:
                return jsonify({
                    'success': False,
                    'error': 'User already exists'
                }), 409

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to register user: {str(e)}'
        }), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """
    Login user and return access token.
    
    Expected JSON payload:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        JSON response with access token and user info
    """
    if request.method == 'OPTIONS':
        # ✅ Preflight request — send empty OK response
        return '', 204
        
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        # Get user from database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash 
            FROM users 
            WHERE username = ?
        ''', (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user or not verify_password(password, user['password_hash']):
            return jsonify({
                'success': False,
                'error': 'Invalid username or password'
            }), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['id']))
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to login: {str(e)}'
        }), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile.
    
    Returns:
        JSON response with user profile information
    """
    try:
        user_id = int(get_jwt_identity())
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, created_at 
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get profile: {str(e)}'
        }), 500

@app.route('/api/checkin', methods=['GET'])
@jwt_required()
def get_checkins():
    """
    Retrieve the last 5 mood check-ins from the database for the current user.
    
    Returns:
        JSON response with checkins data or error message
    """
    try:
        user_id = int(get_jwt_identity())
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, mood, stress_level, notes, timestamp 
            FROM checkins 
            WHERE user_id = ?
            ORDER BY timestamp DESC 
            LIMIT 5
        ''', (user_id,))
        
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
@jwt_required()
def submit_checkin():
    """
    Submit a new mood check-in to the database for the current user.
    
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
        user_id = int(get_jwt_identity())
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
            INSERT INTO checkins (user_id, mood, stress_level, notes) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, mood, stress_level, notes))
        
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
@jwt_required()
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
@jwt_required()
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
@app.route('/api/dass21/submit', methods=['POST'])
@jwt_required()
def submit_dass21():
    """
    Submit a completed DASS-21 quiz and calculate severity scores.
    Expected JSON:
    {
        "answers": {
            "1": 2, "2": 0, ..., "21": 3
        }
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        data = request.get_json()
        print("Received DASS-21 submission:", data)  # 👈 Add this line

        answers = data.get('answers')
        if not answers or len(answers) != 21:
            return jsonify({
                'success': False,
                'error': 'Invalid or incomplete answers'
            }), 400


        answers = data.get('answers')

        if not answers or len(answers) != 21:
            return jsonify({
                'success': False,
                'error': 'Invalid or incomplete answers'
            }), 400

        # Initialize scores
        scores = {'d': 0, 'a': 0, 's': 0}
        tags = {
            1: 's', 2: 'a', 3: 'd', 4: 'a', 5: 'd', 6: 's', 7: 'a',
            8: 's', 9: 'a', 10: 'd', 11: 's', 12: 's', 13: 'd',
            14: 's', 15: 'a', 16: 'd', 17: 'd', 18: 's', 19: 'a',
            20: 'a', 21: 'd'
        }

        for qid, value in answers.items():
            tag = tags.get(int(qid))
            if tag:
                scores[tag] += int(value)

        # Multiply by 2 as per DASS-21 scoring
        for k in scores:
            scores[k] *= 2

        # Save in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dass_assessments (user_id, scores)
            VALUES (?, ?)
        ''', (user_id, json.dumps(scores)))
        conn.commit()
        conn.close()

        # Return scores
        return jsonify({
    'success': True,
    'scores': {
        'Depression': scores['d'],
        'Anxiety': scores['a'],
        'Stress': scores['s']
    },
    'severity': classify_dass_scores(scores)
})


    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to submit DASS-21: {str(e)}'
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
def classify_dass_scores(scores):
    """
    Map raw scores to severity levels.
    """
    def get_level(scale, score):
        if scale == 'd':
            return ("Normal" if score < 10 else
                    "Mild" if score < 14 else
                    "Moderate" if score < 21 else
                    "Severe" if score < 28 else "Extremely Severe")
        elif scale == 'a':
            return ("Normal" if score < 8 else
                    "Mild" if score < 10 else
                    "Moderate" if score < 15 else
                    "Severe" if score < 20 else "Extremely Severe")
        elif scale == 's':
            return ("Normal" if score < 15 else
                    "Mild" if score < 19 else
                    "Moderate" if score < 26 else
                    "Severe" if score < 34 else "Extremely Severe")

    return {
        "Depression": get_level('d', scores['d']),
        "Anxiety": get_level('a', scores['a']),
        "Stress": get_level('s', scores['s'])
    }

@app.route('/api/copilot/grounding', methods=['POST'])
@jwt_required()
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
@jwt_required()
def chat():
    try:
        user_id = get_jwt_identity()
        print(f"Received message from user_id: {user_id}")

        data = request.get_json()
        message = data.get("message")
        print(f"User message: {message}")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Connect to DB
        conn = sqlite3.connect("mindbridge.db")
        cursor = conn.cursor()

        # Log user message
        cursor.execute(
            "INSERT INTO chat_logs (user_id, role, message) VALUES (?, ?, ?)",
            (user_id, "user", message)
        )
        conn.commit()

        # Step 1: Fetch last 3 days' context
        print("Fetching user context...")
        user_context = fetch_user_context(user_id)

        # Step 2: Retrieve relevant docs from Chroma
        print("Retrieving relevant docs...")
        relevant_docs = retrieve_relevant_knowledge(message)
        doc_text = "\n".join([doc.page_content for doc in relevant_docs]) if relevant_docs else ""

        # Step 3: Build prompt
        prompt = f"""
        You are a compassionate mental health assistant.

        User's recent emotional history:
        {user_context}

        Helpful background information:
        {doc_text}

        Now respond to their message:
        "{message}"
        """
        print("Calling Gemini API...")
        gemini_response = gemini_chat(prompt)

        if not gemini_response:
            gemini_response = "Sorry, I'm having trouble understanding. Please try again."

        # Step 4: Log assistant response
        cursor.execute(
            "INSERT INTO chat_logs (user_id, role, message) VALUES (?, ?, ?)",
            (user_id, "assistant", gemini_response)
        )
        conn.commit()
        conn.close()

        print("Returning response to frontend.")
        return jsonify({"success": True, "response": gemini_response})


    except Exception as e:
        print(f"❌ Error in /api/chat: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


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