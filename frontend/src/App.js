/**
 * MindBridge - Main React Application Component
 * 
 * This component serves as the central hub for the MindBridge mood and mental health tracker.
 * It includes all core features: daily check-ins, mood quiz, AI copilot, and chat interface.
 * 
 * Features:
 * - User authentication with JWT tokens
 * - Daily mood and stress level check-ins
 * - AI-generated mood quiz with insights
 * - Contextual AI copilot for grounding exercises
 * - Conversational chat assistant
 * - Adaptive UI based on mood state
 * - Responsive design with Tailwind CSS
 */

import React, { useState, useEffect } from 'react';
import { 
  Home, 
  Heart, 
  Brain, 
  MessageCircle, 
  Plus,
  Send,
  RefreshCw,
  Calendar,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Loader2,
  User,
  LogOut,
  LogIn,
  UserPlus,
  Eye,
  EyeOff
} from 'lucide-react';

// API base URL - adjust for your backend
const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [dassQuestions] = useState([
  { id: 1, text: "I found it hard to wind down", tag: "s" },
  { id: 2, text: "I was aware of dryness of my mouth", tag: "a" },
  { id: 3, text: "I couldn’t seem to experience any positive feeling at all", tag: "d" },
  { id: 4, text: "I experienced breathing difficulty", tag: "a" },
  { id: 5, text: "I found it difficult to work up the initiative to do things", tag: "d" },
  { id: 6, text: "I tended to over-react to situations", tag: "s" },
  { id: 7, text: "I experienced trembling", tag: "a" },
  { id: 8, text: "I felt that I was using a lot of nervous energy", tag: "s" },
  { id: 9, text: "I was worried about situations in which I might panic", tag: "a" },
  { id: 10, text: "I felt that I had nothing to look forward to", tag: "d" },
  { id: 11, text: "I found myself getting agitated", tag: "s" },
  { id: 12, text: "I found it difficult to relax", tag: "s" },
  { id: 13, text: "I felt down-hearted and blue", tag: "d" },
  { id: 14, text: "I was intolerant of anything that kept me from getting on", tag: "s" },
  { id: 15, text: "I felt I was close to panic", tag: "a" },
  { id: 16, text: "I was unable to become enthusiastic about anything", tag: "d" },
  { id: 17, text: "I felt I wasn’t worth much as a person", tag: "d" },
  { id: 18, text: "I felt that I was rather touchy", tag: "s" },
  { id: 19, text: "I was aware of the action of my heart", tag: "a" },
  { id: 20, text: "I felt scared without any good reason", tag: "a" },
  { id: 21, text: "I felt that life was meaningless", tag: "d" },
]);
  const [currentDassIndex, setCurrentDassIndex] = useState(0);
  const [dassAnswers, setDassAnswers] = useState({});

  // Authentication state
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('mindbridge_token'));
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
  const [authData, setAuthData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);

  // Main application state
  const [currentPage, setCurrentPage] = useState('home');
  const [currentMood, setCurrentMood] = useState('neutral');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Check-in state
  const [checkinData, setCheckinData] = useState({
    mood: '',
    stress_level: 5,
    notes: ''
  });
  const [recentCheckins, setRecentCheckins] = useState([]);

  // Quiz state
  const [quizQuestion, setQuizQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [quizInsight, setQuizInsight] = useState('');
  const [quizStarted, setQuizStarted] = useState(false);
  const [quizType, setQuizType] = useState(null); // 'mood' or 'dass21'


  // Copilot state
  const [copilotPrompt, setCopilotPrompt] = useState('');
  const [copilotResponse, setCopilotResponse] = useState('');

  // Chat state
  const [chatMessages, setChatMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');

  // Check authentication on component mount
  useEffect(() => {
    checkAuth();
  }, []);

  // Load recent check-ins when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadRecentCheckins();
    }
  }, [isAuthenticated]);

  // Check if user is authenticated
  const checkAuth = async () => {
    const storedToken = localStorage.getItem('mindbridge_token');
    if (storedToken) {
      setToken(storedToken);
      try {
        const response = await apiCall('/auth/profile', {
          headers: { Authorization: `Bearer ${storedToken}` }
        });
        if (response.success) {
          setUser(response.user);
          setIsAuthenticated(true);
        } else {
          // Token is invalid, remove it
          localStorage.removeItem('mindbridge_token');
          setToken(null);
        }
      } catch (error) {
        // Token is invalid, remove it
        localStorage.removeItem('mindbridge_token');
        setToken(null);
      }
    }
  };

  // Login function
  const login = async () => {
    if (!authData.username || !authData.password) {
      setError('Username and password are required');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          username: authData.username,
          password: authData.password
        })
      });

      if (response.success) {
        setToken(response.access_token);
        setUser(response.user);
        setIsAuthenticated(true);
        localStorage.setItem('mindbridge_token', response.access_token);
        setAuthData({ username: '', email: '', password: '', confirmPassword: '' });
        setSuccess('Login successful!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(response.error || 'Login failed');
      }
    } catch (error) {
      setError('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (quizType === 'dass' && Object.keys(dassAnswers).length === 21) {
      handleDassSubmit();
    }
  }, [dassAnswers]);

  

  // Register function
  const register = async () => {
    if (!authData.username || !authData.email || !authData.password) {
      setError('All fields are required');
      return;
    }

    if (authData.password !== authData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (authData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          username: authData.username,
          email: authData.email,
          password: authData.password
        })
      });

      if (response.success) {
        setToken(response.access_token);
        setUser(response.user);
        setIsAuthenticated(true);
        localStorage.setItem('mindbridge_token', response.access_token);
        setAuthData({ username: '', email: '', password: '', confirmPassword: '' });
        setSuccess('Registration successful! Welcome to MindBridge!');
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(response.error || 'Registration failed');
      }
    } catch (error) {
      setError('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('mindbridge_token');
    setCurrentPage('home');
    setSuccess('Logged out successfully!');
    setTimeout(() => setSuccess(''), 3000);
  };

  // Determine adaptive UI colors based on current mood
  const getMoodColors = () => {
    switch (currentMood) {
      case 'happy':
        return {
          background: 'bg-gradient-to-br from-green-50 to-emerald-100',
          primary: 'bg-mood-happy',
          text: 'text-green-800',
          border: 'border-green-300'
        };
      case 'sad':
        return {
          background: 'bg-gradient-to-br from-gray-50 to-slate-100',
          primary: 'bg-mood-sad',
          text: 'text-gray-800',
          border: 'border-gray-300'
        };
      case 'stressed':
        return {
          background: 'bg-gradient-to-br from-red-50 to-rose-100',
          primary: 'bg-mood-stressed',
          text: 'text-red-800',
          border: 'border-red-300'
        };
      case 'calm':
        return {
          background: 'bg-gradient-to-br from-blue-50 to-sky-100',
          primary: 'bg-mood-calm',
          text: 'text-blue-800',
          border: 'border-blue-300'
        };
      default:
        return {
          background: 'bg-gradient-to-br from-gray-50 to-neutral-100',
          primary: 'bg-mood-neutral',
          text: 'text-gray-800',
          border: 'border-gray-300'
        };
    }
  };

  const colors = getMoodColors();

  // API helper functions with JWT support
  const apiCall = async (endpoint, options = {}) => {
  try {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    // Add JWT token if available and not already provided
    if (token && !headers.Authorization) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: options.method || 'GET',
      headers: headers, // ✅ Use the constructed headers here
      body: options.body || null
    });

    if (!response.ok) {
      if (response.status === 401) {
        logout(); // logout() should be defined in this scope
        throw new Error('Session expired. Please login again.');
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};


  // Load recent check-ins from backend
  const loadRecentCheckins = async () => {
    try {
      const response = await apiCall('/checkin');
      if (response.success) {
        setRecentCheckins(response.checkins);
        
        // Update current mood based on most recent check-in
        if (response.checkins.length > 0) {
          const latestCheckin = response.checkins[0];
          updateMoodFromCheckin(latestCheckin);
        }
      }
    } catch (error) {
      console.error('Failed to load check-ins:', error);
    }
  };

  // Update UI mood based on check-in data
  const updateMoodFromCheckin = (checkin) => {
    const mood = checkin.mood.toLowerCase();
    const stress = checkin.stress_level;

    if (stress >= 8) {
      setCurrentMood('stressed');
    } else if (mood.includes('happy') || mood.includes('great') || mood.includes('good')) {
      setCurrentMood('happy');
    } else if (mood.includes('sad') || mood.includes('down') || mood.includes('bad')) {
      setCurrentMood('sad');
    } else if (stress <= 3) {
      setCurrentMood('calm');
    } else {
      setCurrentMood('neutral');
    }
  };

  // Submit daily check-in
  const submitCheckin = async () => {
    if (!checkinData.mood) {
      setError('Please enter your mood');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall('/checkin', {
        method: 'POST',
        body: JSON.stringify(checkinData)
      });

      if (response.success) {
        setSuccess('Check-in submitted successfully!');
        setCheckinData({ mood: '', stress_level: 5, notes: '' });
        loadRecentCheckins();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(response.error || 'Failed to submit check-in');
      }
    } catch (error) {
      setError('Failed to submit check-in. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const startQuiz = async (type) => {
  setQuizType(type);
  setQuizInsight('');
  setSelectedAnswer('');
  setQuizQuestion(null);
  setDassAnswers({});
  setCurrentDassIndex(0);
  setError('');
  setSuccess('');
  setQuizStarted(true);

  if (type === 'mood') {
    try {
      const response = await apiCall('/mood_quiz/generate');
      if (response.success) {
        setQuizQuestion(response.question);
      } else {
        setError(response.error || 'Failed to start quiz');
      }
    } catch (error) {
      setError('Failed to start quiz. Please try again.');
    }
  }
};


  // Submit quiz answer
  const submitQuizAnswer = async () => {
    if (!selectedAnswer) {
      setError('Please select an answer');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall('/mood_quiz/submit', {
        method: 'POST',
        body: JSON.stringify({
          question_id: quizQuestion.id,
          answer: selectedAnswer
        })
      });

      if (response.success) {
        setQuizInsight(response.insight);
        setSelectedAnswer('');
      } else {
        setError(response.error || 'Failed to submit answer');
      }
    } catch (error) {
      setError('Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

const handleDassSubmit = async () => {
  console.log('Submitting DASS-21 answers:', dassAnswers); // ✅ Debug log
  try {
    const response = await apiCall('/dass21/submit', {
      method: 'POST',
      body: JSON.stringify({ answers: dassAnswers })  // ✅ Wrap in { answers: ... }
    });

    if (response.success) {
  const scores = response.scores;

  // Determine the mood with the highest score
  const highest = Object.entries(scores).reduce((max, entry) =>
    entry[1] > max[1] ? entry : max
  ); // highest = [key, value]

  const predictedMood = highest[0];
  const predictedScore = highest[1];

  const summary = `
Predicted Mood: ${predictedMood}

Depression: ${response.severity.Depression} (${scores.Depression})
Anxiety: ${response.severity.Anxiety} (${scores.Anxiety})
Stress: ${response.severity.Stress} (${scores.Stress})
Based on your overall responses, it seems that ${predictedMood} is currently the most prominent challenge you're facing.
Don't worry - you're not alone, and we're here to help you through it ☺️.
  `.trim();

  setQuizInsight(summary);
  setCurrentDassIndex(dassQuestions.length); // ✅ Force show summary screen
}
 else {
      setError(response.error || 'Failed to evaluate DASS-21');
    }
  } catch (err) {
    setError('Something went wrong submitting DASS-21');
  }
  
};



  // Get grounding exercise from copilot
  const getGroundingExercise = async () => {
    if (!copilotPrompt.trim()) {
      setError('Please enter a request');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await apiCall('/copilot/grounding', {
        method: 'POST',
        body: JSON.stringify({ prompt: copilotPrompt })
      });

      if (response.success) {
        setCopilotResponse(response.exercise);
      } else {
        setError(response.error || 'Failed to get exercise');
      }
    } catch (error) {
      setError('Failed to get exercise. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Send chat message
  const sendChatMessage = async () => {
    if (!currentMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: currentMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setChatMessages(prev => [...prev, userMessage]);
    const messageToSend = currentMessage;
    setCurrentMessage('');
    setLoading(true);
    
    try {
      const response = await apiCall('/chat', {
        method: 'POST',
        body: JSON.stringify({ message: messageToSend })
      });

      if (response.success) {
        const assistantMessage = {
          id: Date.now() + 1,
          text: response.response,
          sender: 'assistant',
          timestamp: new Date().toLocaleTimeString()
        };
        setChatMessages(prev => [...prev, assistantMessage]);
      } else {
        setError(response.error || 'Failed to send message');
      }
    } catch (error) {
      setError('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Clear messages
  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  // Navigation items
  const navItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'checkin', label: 'Check-in', icon: Heart },
    { id: 'quiz', label: 'Quiz', icon: Brain },
    { id: 'copilot', label: 'Copilot', icon: TrendingUp },
    { id: 'chat', label: 'Chat', icon: MessageCircle }
  ];

  // Render authentication page
  const renderAuth = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">MindBridge</h1>
        <p className="text-gray-600">Your personal mood and mental health companion</p>
      </div>

      {renderMessages()}

      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex justify-center mb-6">
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setAuthMode('login')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                authMode === 'login'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Login
            </button>
            <button
              onClick={() => setAuthMode('register')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                authMode === 'register'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Register
            </button>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              type="text"
              value={authData.username}
              onChange={(e) => setAuthData({...authData, username: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your username"
            />
          </div>

          {authMode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={authData.email}
                onChange={(e) => setAuthData({...authData, email: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your email"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={authData.password}
                onChange={(e) => setAuthData({...authData, password: e.target.value})}
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {authMode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                type={showPassword ? 'text' : 'password'}
                value={authData.confirmPassword}
                onChange={(e) => setAuthData({...authData, confirmPassword: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Confirm your password"
              />
            </div>
          )}

          <button
            onClick={authMode === 'login' ? login : register}
            disabled={loading}
            className={`w-full ${colors.primary} text-white py-3 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center`}
          >
            {loading ? (
              <Loader2 className="animate-spin mr-2" size={20} />
            ) : authMode === 'login' ? (
              <LogIn className="mr-2" size={20} />
            ) : (
              <UserPlus className="mr-2" size={20} />
            )}
            {loading ? 'Please wait...' : authMode === 'login' ? 'Login' : 'Register'}
          </button>
        </div>
      </div>
    </div>
  );

  // Render navigation
  const renderNavigation = () => (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 z-50">
      <div className="max-w-md mx-auto flex justify-around">
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => {
                setCurrentPage(item.id);
                clearMessages();
              }}
              className={`flex flex-col items-center px-2 py-1 rounded-lg transition-colors
                ${isActive 
                  ? `${colors.primary} text-white` 
                  : 'text-gray-600 hover:text-gray-800'
                }`}
            >
              <Icon size={20} />
              <span className="text-xs mt-1">{item.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );

  // Render header with user info and logout
  const renderHeader = () => (
    <div className="flex justify-between items-center mb-6">
      <div className="flex items-center space-x-2">
        <User size={20} className="text-gray-600" />
        <span className="text-gray-700 font-medium">Welcome, {user?.username}!</span>
      </div>
      <button
        onClick={logout}
        className="flex items-center space-x-1 text-gray-600 hover:text-gray-800 transition-colors"
      >
        <LogOut size={16} />
        <span className="text-sm">Logout</span>
      </button>
    </div>
  );

  // Render message displays
  const renderMessages = () => (
    <div className="mb-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 flex items-center">
          <AlertTriangle size={16} className="mr-2" />
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4 flex items-center">
          <CheckCircle size={16} className="mr-2" />
          {success}
        </div>
      )}
    </div>
  );

  // Render home page
  const renderHome = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to MindBridge</h1>
        <p className="text-gray-600">Your personal mood and mental health companion</p>
      </div>

      <div className="grid gap-4">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Heart className="mr-2 text-red-500" size={20} />
            Daily Check-in
          </h2>
          <p className="text-gray-600 mb-4">Track your mood and stress levels</p>
          <button
            onClick={() => setCurrentPage('checkin')}
            className={`${colors.primary} text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity`}
          >
            Start Check-in
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Brain className="mr-2 text-purple-500" size={20} />
            Mood Quiz
          </h2>
          <p className="text-gray-600 mb-4">Get personalized insights about your mood</p>
          <button
            onClick={() => setCurrentPage('quiz')}
            className={`${colors.primary} text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity`}
          >
            Take Quiz
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <TrendingUp className="mr-2 text-blue-500" size={20} />
            AI Copilot
          </h2>
          <p className="text-gray-600 mb-4">Get grounding exercises and micro-lessons</p>
          <button
            onClick={() => setCurrentPage('copilot')}
            className={`${colors.primary} text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity`}
          >
            Get Support
          </button>
        </div>
      </div>

      {/* Passive Data Placeholder */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold mb-2">Passive Data Analysis</h3>
        <div className="text-gray-600 space-y-2">
          <p>📊 Passive data analysis coming soon!</p>
          <p>💓 Heart Rate: 72 bpm</p>
          <p>😴 Sleep: 7.5 hours</p>
          <p className="text-sm text-gray-500">* Placeholder data for demonstration</p>
        </div>
      </div>

      {/* Early Warning Placeholder */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold mb-2">Early Warning System</h3>
        <div className="text-gray-600">
          {currentMood === 'stressed' ? (
            <p className="text-orange-600">⚠️ Looks like you're feeling stressed today. Remember to take a break!</p>
          ) : currentMood === 'happy' ? (
            <p className="text-green-600">😊 Great mood today! Keep up the positive energy!</p>
          ) : (
            <p>🤖 AI monitoring your patterns for early insights...</p>
          )}
        </div>
      </div>
    </div>
  );

  // Render check-in page
  const renderCheckin = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Daily Check-in</h1>
        <p className="text-gray-600">How are you feeling today?</p>
      </div>

      {renderMessages()}

      <div className="bg-white rounded-lg shadow-sm border p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Overall Mood
          </label>
          <select
            value={checkinData.mood}
            onChange={(e) => setCheckinData({...checkinData, mood: e.target.value})}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select your mood</option>
            <option value="Very Happy">😄 Very Happy</option>
            <option value="Happy">😊 Happy</option>
            <option value="Neutral">😐 Neutral</option>
            <option value="Sad">😢 Sad</option>
            <option value="Very Sad">😭 Very Sad</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Stress Level: {checkinData.stress_level}/10
          </label>
          <input
            type="range"
            min="1"
            max="10"
            value={checkinData.stress_level}
            onChange={(e) => setCheckinData({...checkinData, stress_level: parseInt(e.target.value)})}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Low</span>
            <span>High</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Notes/Reflections
          </label>
          <textarea
            value={checkinData.notes}
            onChange={(e) => setCheckinData({...checkinData, notes: e.target.value})}
            placeholder="How are you feeling? What's on your mind?"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 h-24 resize-none"
          />
        </div>

        <button
          onClick={submitCheckin}
          disabled={loading}
          className={`w-full ${colors.primary} text-white py-3 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center`}
        >
          {loading ? (
            <Loader2 className="animate-spin mr-2" size={20} />
          ) : (
            <Plus className="mr-2" size={20} />
          )}
          {loading ? 'Submitting...' : 'Submit Check-in'}
        </button>
      </div>

      {/* Recent Check-ins */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Calendar className="mr-2" size={20} />
          Recent Check-ins
        </h3>
        
        {recentCheckins.length === 0 ? (
          <p className="text-gray-500">No check-ins yet. Start your first check-in above!</p>
        ) : (
          <div className="space-y-3">
            {recentCheckins.map(checkin => (
              <div key={checkin.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium">Mood: {checkin.mood}</p>
                    <p className="text-sm text-gray-600">Stress: {checkin.stress_level}/10</p>
                    {checkin.notes && (
                      <p className="text-sm text-gray-700 mt-1">{checkin.notes}</p>
                    )}
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(checkin.timestamp).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderQuiz = () => (
    
  <div className="space-y-6">
    <div className="text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">
        {quizType === 'dass' ? 'DASS-21 Mental Health Quiz' : 'Mood Quiz'}
      </h1>
      <p className="text-gray-600">
        {quizType === 'dass'
          ? 'This questionnaire helps assess depression, anxiety, and stress levels over the past week.'
          : 'Discover insights about your current mood'}
      </p>
    </div>

    {renderMessages()}

    <div className="bg-white rounded-lg shadow-sm border p-6">
      {!quizStarted ? (
        <div className="text-center space-y-4">
          <Brain className="mx-auto text-purple-500" size={48} />
          <h2 className="text-xl font-semibold">Ready to explore your mental state?</h2>
          <p className="text-gray-600">
            Choose a quiz type to get personalized insights about your mind.
          </p>
          <div className="flex flex-col gap-4 items-center">
            <button
              onClick={() => startQuiz('mood')}
              className={`${colors.primary} text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 flex items-center justify-center`}
            >
              <Brain className="mr-2" size={20} />
              Mood Quiz
            </button>
            <button
              onClick={() => startQuiz('dass')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:opacity-90 flex items-center justify-center"
            >
              <Brain className="mr-2" size={20} />
              DASS-21 Quiz
            </button>
          </div>
        </div>
      ) : quizType === 'mood' ? (
        <div className="space-y-4">
          {quizQuestion && (
            <div>
              <h3 className="text-lg font-semibold mb-4">{quizQuestion.question}</h3>
              <div className="space-y-2">
                {quizQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedAnswer(option)}
                    className={`w-full p-3 text-left rounded-lg border transition-colors
                      ${selectedAnswer === option 
                        ? `${colors.primary} text-white border-transparent` 
                        : 'bg-gray-50 hover:bg-gray-100 border-gray-200'
                      }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
              <button
                onClick={submitQuizAnswer}
                disabled={!selectedAnswer || loading}
                className={`w-full mt-4 ${colors.primary} text-white py-3 rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center`}
              >
                {loading ? (
                  <Loader2 className="animate-spin mr-2" size={20} />
                ) : (
                  <Send className="mr-2" size={20} />
                )}
                {loading ? 'Analyzing...' : 'Submit Answer'}
              </button>
            </div>
          )}
          {quizInsight && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">Your Mood Insight:</h4>
              <p className="text-blue-800">{quizInsight}</p>
              <button
                onClick={() => {
                  setQuizStarted(false);
                  setQuizInsight('');
                  setSelectedAnswer('');
                  setQuizQuestion(null);
                  setQuizType(null);
                }}
                className="mt-3 text-blue-600 hover:text-blue-800 font-medium"
              >
                Take Another Quiz
              </button>
            </div>
          )}
        </div>
      ) : currentDassIndex < dassQuestions.length ? (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold mb-4">
              Question {currentDassIndex + 1} of 21
            </h3>
            <p className="text-gray-700 mb-4">
              {dassQuestions[currentDassIndex].text}
            </p>
            <div className="grid gap-3">
              {[0, 1, 2, 3].map(score => (
                <button
                  key={score}
                  onClick={() => {
                    setDassAnswers(prev => ({
                      ...prev,
                      [dassQuestions[currentDassIndex].id]: score
                    }));
                    if (currentDassIndex < dassQuestions.length - 1) {
                      setCurrentDassIndex(prev => prev + 1);
                    }
                  }}
                  className="w-full py-2 rounded-lg border border-gray-300 hover:bg-gray-100"
                >
                  {score} – {[
                    "Did not apply at all",
                    "Applied to some degree",
                    "Applied to a good part of time",
                    "Applied very much or most of the time"
                  ][score]}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-semibold text-blue-900 mb-2">DASS-21 Summary:</h4>
            <pre className="text-blue-800 whitespace-pre-wrap">{quizInsight}</pre>
            <button
              onClick={() => {
                setQuizStarted(false);
                setQuizInsight('');
                setDassAnswers({});
                setCurrentDassIndex(0);
                setQuizType(null);
              }}
              className="mt-3 text-blue-600 hover:text-blue-800 font-medium"
            >
              Take Another Quiz
          </button>
        </div>
      )}
    </div>
  </div>
);


  // Render copilot page
  const renderCopilot = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">AI Copilot</h1>
        <p className="text-gray-600">Get personalized grounding exercises and support</p>
      </div>

      {renderMessages()}

      <div className="bg-white rounded-lg shadow-sm border p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            What kind of support do you need?
          </label>
          <input
            type="text"
            value={copilotPrompt}
            onChange={(e) => setCopilotPrompt(e.target.value)}
            placeholder="e.g., 'I need a grounding exercise', 'breathing techniques', 'mindfulness'"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          onClick={getGroundingExercise}
          disabled={loading}
          className={`w-full ${colors.primary} text-white py-3 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center`}
        >
          {loading ? (
            <Loader2 className="animate-spin mr-2" size={20} />
          ) : (
            <TrendingUp className="mr-2" size={20} />
          )}
          {loading ? 'Getting Support...' : 'Get Support'}
        </button>
      </div>

      {copilotResponse && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold mb-4">Your Personalized Exercise:</h3>
          <div className="bg-gray-50 p-4 rounded-lg">
            <pre className="whitespace-pre-wrap text-gray-700 font-medium leading-relaxed">
              {copilotResponse}
            </pre>
          </div>
          <button
            onClick={() => setCopilotResponse('')}
            className="mt-4 text-blue-600 hover:text-blue-800 font-medium"
          >
            Clear Exercise
          </button>
        </div>
      )}
    </div>
  );

  // Render chat page
  const renderChat = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Chat Assistant</h1>
        <p className="text-gray-600">Talk to your supportive AI companion</p>
        <p className="text-sm text-gray-500 mt-1">Assistant is learning to understand tone</p>
      </div>

      {renderMessages()}

      {/* Chat Messages */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="h-64 overflow-y-auto scrollbar-hide space-y-3 mb-4">
          {chatMessages.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <MessageCircle className="mx-auto mb-2" size={32} />
              <p>Start a conversation with your AI assistant</p>
            </div>
          ) : (
            chatMessages.map(message => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-lg ${
                    message.sender === 'user'
                      ? `${colors.primary} text-white`
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <p className="text-sm">{message.text}</p>
                  <p className="text-xs mt-1 opacity-75">{message.timestamp}</p>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Chat Input */}
        <div className="flex space-x-2">
          <input
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
            placeholder="Type your message..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendChatMessage}
            disabled={loading || !currentMessage.trim()}
            className={`${colors.primary} text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center`}
          >
            {loading ? (
              <Loader2 className="animate-spin" size={20} />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
      </div>
    </div>
  );

  // Main render
  return (
    <div className={`min-h-screen ${colors.background} mood-transition pb-20`}>
      <div className="max-w-md mx-auto p-4">
        {isAuthenticated ? (
          <>
            {renderHeader()}
            {currentPage === 'home' && renderHome()}
            {currentPage === 'checkin' && renderCheckin()}
            {currentPage === 'quiz' && renderQuiz()}
            {currentPage === 'copilot' && renderCopilot()}
            {currentPage === 'chat' && renderChat()}
          </>
        ) : (
          renderAuth()
        )}
      </div>
      
      {isAuthenticated && renderNavigation()}
    </div>
  );
}

export default App; 