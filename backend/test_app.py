"""
Unit tests for MindBridge Flask backend API endpoints.

This test suite covers all API endpoints with expected use cases, edge cases, and failure scenarios.
Tests use an in-memory SQLite database to avoid interfering with the main database.
"""

import unittest
import json
import tempfile
import os
import sqlite3
from app import app, init_db, DB_NAME

class MindBridgeAPITestCase(unittest.TestCase):
    """Test case for MindBridge API endpoints."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary database file
        self.db_fd, self.temp_db = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['DATABASE'] = self.temp_db
        
        # Override the database name for testing
        global DB_NAME
        self.original_db_name = DB_NAME
        DB_NAME = self.temp_db
        
        # Initialize test database
        init_db()
        
        # Clear any existing data (table should exist after init_db)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM checkins')
        except sqlite3.OperationalError:
            # Table doesn't exist, create it
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
        
        # Create test client
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up after each test."""
        global DB_NAME
        DB_NAME = self.original_db_name
        os.close(self.db_fd)
        os.unlink(self.temp_db)
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'healthy')
    
    def test_submit_checkin_success(self):
        """Test successful check-in submission."""
        checkin_data = {
            'mood': 'Happy',
            'stress_level': 3,
            'notes': 'Feeling good today!'
        }
        
        response = self.client.post('/api/checkin', 
                                   data=json.dumps(checkin_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Check-in submitted successfully')
    
    def test_submit_checkin_missing_fields(self):
        """Test check-in submission with missing required fields."""
        # Missing mood
        checkin_data = {
            'stress_level': 5,
            'notes': 'Test note'
        }
        
        response = self.client.post('/api/checkin', 
                                   data=json.dumps(checkin_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('required', data['error'])
    
    def test_submit_checkin_invalid_stress_level(self):
        """Test check-in submission with invalid stress level."""
        checkin_data = {
            'mood': 'Happy',
            'stress_level': 15,  # Invalid: should be 1-10
            'notes': 'Test note'
        }
        
        response = self.client.post('/api/checkin', 
                                   data=json.dumps(checkin_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('between 1 and 10', data['error'])
    
    def test_get_checkins_empty(self):
        """Test retrieving check-ins when none exist."""
        response = self.client.get('/api/checkin')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['checkins']), 0)
    
    def test_get_checkins_with_data(self):
        """Test retrieving check-ins after submitting some."""
        # Submit a few check-ins
        checkins = [
            {'mood': 'Happy', 'stress_level': 2, 'notes': 'Good day'},
            {'mood': 'Neutral', 'stress_level': 5, 'notes': 'Average day'},
            {'mood': 'Sad', 'stress_level': 8, 'notes': 'Tough day'}
        ]
        
        for checkin in checkins:
            self.client.post('/api/checkin', 
                            data=json.dumps(checkin),
                            content_type='application/json')
        
        # Retrieve check-ins
        response = self.client.get('/api/checkin')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['checkins']), 3)
        
        # Check that most recent is first
        self.assertEqual(data['checkins'][0]['mood'], 'Sad')
    
    def test_generate_mood_quiz(self):
        """Test mood quiz generation."""
        response = self.client.get('/api/mood_quiz/generate')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('question', data)
        self.assertIn('id', data['question'])
        self.assertIn('question', data['question'])
        self.assertIn('options', data['question'])
        self.assertGreater(len(data['question']['options']), 0)
    
    def test_submit_mood_quiz_success(self):
        """Test successful mood quiz answer submission."""
        quiz_data = {
            'question_id': 1,
            'answer': 'Energized'
        }
        
        response = self.client.post('/api/mood_quiz/submit',
                                   data=json.dumps(quiz_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('insight', data)
        self.assertGreater(len(data['insight']), 0)
    
    def test_submit_mood_quiz_missing_answer(self):
        """Test mood quiz submission with missing answer."""
        quiz_data = {
            'question_id': 1
        }
        
        response = self.client.post('/api/mood_quiz/submit',
                                   data=json.dumps(quiz_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('required', data['error'])
    
    def test_copilot_grounding_exercise(self):
        """Test getting grounding exercise from copilot."""
        prompts = [
            'grounding exercise',
            'breathing techniques',
            'mindfulness meditation',
            'general wellness'
        ]
        
        for prompt in prompts:
            copilot_data = {'prompt': prompt}
            
            response = self.client.post('/api/copilot/grounding',
                                       data=json.dumps(copilot_data),
                                       content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('exercise', data)
            self.assertGreater(len(data['exercise']), 0)
    
    def test_copilot_empty_prompt(self):
        """Test copilot with empty prompt."""
        copilot_data = {'prompt': ''}
        
        response = self.client.post('/api/copilot/grounding',
                                   data=json.dumps(copilot_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('required', data['error'])
    
    def test_chat_response(self):
        """Test chat response generation."""
        test_messages = [
            'I feel sad today',
            'I am stressed',
            'I feel happy',
            'I am tired',
            'I need help',
            'Thank you',
            'Random message'
        ]
        
        for message in test_messages:
            chat_data = {'message': message}
            
            response = self.client.post('/api/chat',
                                       data=json.dumps(chat_data),
                                       content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('response', data)
            self.assertGreater(len(data['response']), 0)
    
    def test_chat_empty_message(self):
        """Test chat with empty message."""
        chat_data = {'message': ''}
        
        response = self.client.post('/api/chat',
                                   data=json.dumps(chat_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('required', data['error'])
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoint."""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('not found', data['error'])
    
    def test_invalid_json(self):
        """Test sending invalid JSON data."""
        response = self.client.post('/api/checkin',
                                   data='invalid json',
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

class MoodInsightTestCase(unittest.TestCase):
    """Test case for mood insight generation logic."""
    
    def setUp(self):
        """Set up test environment."""
        from app import generate_mood_insight
        self.generate_mood_insight = generate_mood_insight
    
    def test_positive_insights(self):
        """Test insights for positive responses."""
        positive_answers = ['Energized', 'Optimistic', 'Strong', 'Satisfied', 'Hopeful']
        
        for answer in positive_answers:
            insight = self.generate_mood_insight(answer)
            self.assertIn('positive', insight.lower())
    
    def test_neutral_insights(self):
        """Test insights for neutral responses."""
        neutral_answers = ['Neutral', 'Adequate', 'Cautious']
        
        for answer in neutral_answers:
            insight = self.generate_mood_insight(answer)
            self.assertIn('balanced', insight.lower())
    
    def test_concerning_insights(self):
        """Test insights for concerning responses."""
        concerning_answers = ['Tired', 'Anxious', 'Worried', 'Isolated', 'Dissatisfied']
        
        for answer in concerning_answers:
            insight = self.generate_mood_insight(answer)
            self.assertIn('challenging', insight.lower())
    
    def test_default_insight(self):
        """Test default insight for unknown responses."""
        insight = self.generate_mood_insight('Unknown response')
        self.assertIn('reflection', insight.lower())

class ChatResponseTestCase(unittest.TestCase):
    """Test case for chat response generation logic."""
    
    def setUp(self):
        """Set up test environment."""
        from app import generate_chat_response
        self.generate_chat_response = generate_chat_response
    
    def test_sad_responses(self):
        """Test responses for sad messages."""
        sad_messages = ['I feel sad', 'I am down', 'feeling depressed']
        
        for message in sad_messages:
            response = self.generate_chat_response(message)
            self.assertIn('sorry', response.lower())
    
    def test_stress_responses(self):
        """Test responses for stress messages."""
        stress_messages = ['I am stressed', 'feeling anxious', 'overwhelmed']
        
        for message in stress_messages:
            response = self.generate_chat_response(message)
            self.assertIn('breath', response.lower())
    
    def test_happy_responses(self):
        """Test responses for happy messages."""
        happy_messages = ['I feel happy', 'I am good', 'feeling great']
        
        for message in happy_messages:
            response = self.generate_chat_response(message)
            self.assertIn('glad', response.lower())
    
    def test_help_responses(self):
        """Test responses for help requests."""
        help_messages = ['I need help', 'can you support me', 'guidance please']
        
        for message in help_messages:
            response = self.generate_chat_response(message)
            self.assertIn('support', response.lower())
    
    def test_default_response(self):
        """Test default response for general messages."""
        response = self.generate_chat_response('random message')
        self.assertIn('sharing', response.lower())

if __name__ == '__main__':
    unittest.main() 