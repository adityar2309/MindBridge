#!/usr/bin/env python3
"""
MindBridge Demo Script with JWT Authentication

This script demonstrates the complete functionality of the MindBridge API
including authentication and all protected endpoints.

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

def test_authentication():
    """Test authentication flow and return JWT token."""
    print("\n🔐 Testing Authentication Flow...")
    
    # Try to register a new user
    auth_data = {
        'username': 'demouser',
        'email': 'demo@example.com',
        'password': 'demopass123'
    }
    
    response = requests.post(f'{API_BASE_URL}/auth/register', json=auth_data)
    print_response('Register New User', response)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print("✅ Registration successful!")
        return token
    
    # If registration fails (user exists), try login
    print("User already exists, trying login...")
    login_data = {
        'username': 'demouser',
        'password': 'demopass123'
    }
    
    response = requests.post(f'{API_BASE_URL}/auth/login', json=login_data)
    print_response('Login Existing User', response)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print("✅ Login successful!")
        return token
    
    print("❌ Authentication failed!")
    return None

def test_checkin_flow(token):
    """Test check-in submission and retrieval with authentication."""
    print("\n🔸 Testing Check-in Flow...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Submit a check-in
    checkin_data = {
        'mood': 'Happy',
        'stress_level': 3,
        'notes': 'Feeling good after demo with auth!'
    }
    
    response = requests.post(f'{API_BASE_URL}/checkin', json=checkin_data, headers=headers)
    print_response('Submit Check-in', response)
    
    # Retrieve check-ins
    response = requests.get(f'{API_BASE_URL}/checkin', headers=headers)
    print_response('Get Check-ins', response)

def test_mood_quiz(token):
    """Test mood quiz generation and submission with authentication."""
    print("\n🧠 Testing Mood Quiz...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Generate a quiz question
    response = requests.get(f'{API_BASE_URL}/mood_quiz/generate', headers=headers)
    print_response('Generate Quiz', response)
    
    if response.status_code == 200:
        quiz_data = response.json()
        question = quiz_data['question']
        
        # Submit an answer
        answer_data = {
            'question_id': question['id'],
            'answer': question['options'][0]  # Select first option
        }
        
        response = requests.post(f'{API_BASE_URL}/mood_quiz/submit', json=answer_data, headers=headers)
        print_response('Submit Quiz Answer', response)

def test_copilot(token):
    """Test AI copilot grounding exercises with authentication."""
    print("\n🤖 Testing AI Copilot...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    test_prompts = [
        'I need a grounding exercise',
        'breathing techniques',
        'mindfulness meditation',
        'general wellness tips'
    ]
    
    for prompt in test_prompts:
        prompt_data = {'prompt': prompt}
        response = requests.post(f'{API_BASE_URL}/copilot/grounding', json=prompt_data, headers=headers)
        print_response(f'Copilot: "{prompt}"', response)
        time.sleep(1)  # Small delay between requests

def test_chat(token):
    """Test chat functionality with authentication."""
    print("\n💬 Testing Chat Assistant...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    test_messages = [
        'Hello, I feel sad today',
        'I am stressed about work',
        'I feel happy and grateful',
        'I need some help',
        'Thank you for your support'
    ]
    
    for message in test_messages:
        chat_data = {'message': message}
        response = requests.post(f'{API_BASE_URL}/chat', json=chat_data, headers=headers)
        print_response(f'Chat: "{message}"', response)
        time.sleep(1)  # Small delay between requests

def test_user_profile(token):
    """Test user profile endpoint with authentication."""
    print("\n👤 Testing User Profile...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{API_BASE_URL}/auth/profile', headers=headers)
    print_response('Get User Profile', response)

def run_demo():
    """Run the complete demo with authentication."""
    print("🌟 MindBridge API Demo Starting (with JWT Authentication)...")
    print("Make sure the Flask backend is running on http://localhost:5000")
    
    try:
        # Test health check first
        if not test_health_check():
            print("❌ Health check failed. Make sure the backend is running.")
            return
        
        print("✅ Backend is healthy!")
        
        # Test authentication
        token = test_authentication()
        if not token:
            print("❌ Authentication failed. Cannot proceed with protected endpoints.")
            return
        
        # Test user profile
        test_user_profile(token)
        
        # Run all tests with authentication
        test_checkin_flow(token)
        test_mood_quiz(token)
        test_copilot(token)
        test_chat(token)
        
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("1. Start the React frontend: cd frontend && npm start")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Try all the features in the web interface")
        print("4. Use the same credentials (demouser/demopass123) to login")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the backend.")
        print("Make sure to run: cd backend && python app.py")
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == '__main__':
    run_demo() 