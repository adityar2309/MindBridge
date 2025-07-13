#!/usr/bin/env python3
"""
MindBridge Demo Script

This script demonstrates the basic functionality of the MindBridge API
by making sample requests to all endpoints.

Run this script after starting the Flask backend to test the API.
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = 'http://localhost:5000/api'

def print_response(endpoint, response):
    """Pretty print API response."""
    print(f"\n{'='*50}")
    print(f"Testing: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print('='*50)

def test_health_check():
    """Test health check endpoint."""
    response = requests.get(f'{API_BASE_URL}/health')
    print_response('Health Check', response)
    return response.status_code == 200

def test_checkin_flow():
    """Test check-in submission and retrieval."""
    print("\n🔸 Testing Check-in Flow...")
    
    # Submit a check-in
    checkin_data = {
        'mood': 'Happy',
        'stress_level': 3,
        'notes': 'Feeling good after demo!'
    }
    
    response = requests.post(f'{API_BASE_URL}/checkin', json=checkin_data)
    print_response('Submit Check-in', response)
    
    # Retrieve check-ins
    response = requests.get(f'{API_BASE_URL}/checkin')
    print_response('Get Check-ins', response)

def test_mood_quiz():
    """Test mood quiz generation and submission."""
    print("\n🧠 Testing Mood Quiz...")
    
    # Generate a quiz question
    response = requests.get(f'{API_BASE_URL}/mood_quiz/generate')
    print_response('Generate Quiz', response)
    
    if response.status_code == 200:
        quiz_data = response.json()
        question = quiz_data['question']
        
        # Submit an answer
        answer_data = {
            'question_id': question['id'],
            'answer': question['options'][0]  # Select first option
        }
        
        response = requests.post(f'{API_BASE_URL}/mood_quiz/submit', json=answer_data)
        print_response('Submit Quiz Answer', response)

def test_copilot():
    """Test AI copilot grounding exercises."""
    print("\n🤖 Testing AI Copilot...")
    
    test_prompts = [
        'I need a grounding exercise',
        'breathing techniques',
        'mindfulness meditation',
        'general wellness tips'
    ]
    
    for prompt in test_prompts:
        prompt_data = {'prompt': prompt}
        response = requests.post(f'{API_BASE_URL}/copilot/grounding', json=prompt_data)
        print_response(f'Copilot: "{prompt}"', response)
        time.sleep(1)  # Small delay between requests

def test_chat():
    """Test chat functionality."""
    print("\n💬 Testing Chat Assistant...")
    
    test_messages = [
        'Hello, I feel sad today',
        'I am stressed about work',
        'I feel happy and grateful',
        'I need some help',
        'Thank you for your support'
    ]
    
    for message in test_messages:
        chat_data = {'message': message}
        response = requests.post(f'{API_BASE_URL}/chat', json=chat_data)
        print_response(f'Chat: "{message}"', response)
        time.sleep(1)  # Small delay between requests

def run_demo():
    """Run the complete demo."""
    print("🌟 MindBridge API Demo Starting...")
    print("Make sure the Flask backend is running on http://localhost:5000")
    
    try:
        # Test health check first
        if not test_health_check():
            print("❌ Health check failed. Make sure the backend is running.")
            return
        
        print("✅ Backend is healthy!")
        
        # Run all tests
        test_checkin_flow()
        test_mood_quiz()
        test_copilot()
        test_chat()
        
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("1. Start the React frontend: cd frontend && npm start")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Try all the features in the web interface")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the backend.")
        print("Make sure to run: cd backend && python app.py")
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == '__main__':
    run_demo() 