#!/usr/bin/env python3
"""
Test script for JWT authentication endpoints
"""

import requests
import json

API_BASE_URL = 'http://localhost:5000/api'

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{API_BASE_URL}/auth/register', json=user_data)
    print(f"Registration Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{API_BASE_URL}/auth/login', json=login_data)
    print(f"Login Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['access_token']
    return None

def test_protected_endpoint(token):
    """Test protected endpoint with token"""
    print("\nTesting protected endpoint...")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = requests.get(f'{API_BASE_URL}/auth/profile', headers=headers)
    print(f"Profile Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_checkin_with_auth(token):
    """Test check-in with authentication"""
    print("\nTesting check-in with authentication...")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    checkin_data = {
        'mood': 'Happy',
        'stress_level': 3,
        'notes': 'Testing with JWT auth!'
    }
    
    response = requests.post(f'{API_BASE_URL}/checkin', json=checkin_data, headers=headers)
    print(f"Check-in Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def run_auth_tests():
    """Run all authentication tests"""
    print("🔐 Testing JWT Authentication System")
    print("=" * 50)
    
    try:
        # Test registration
        token = test_register()
        if not token:
            print("❌ Registration failed, trying login...")
            token = test_login()
        
        if token:
            print("✅ Authentication successful!")
            
            # Test protected endpoints
            test_protected_endpoint(token)
            test_checkin_with_auth(token)
            
            print("\n🎉 All authentication tests completed!")
        else:
            print("❌ Authentication failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure Flask server is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    run_auth_tests() 