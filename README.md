# MindBridge - Mood & Mental Health Tracker

MindBridge is a comprehensive mood and mental health tracking application built with React and Flask. It provides daily check-ins, AI-powered mood quizzes, grounding exercises, and conversational support to help users manage their mental wellness.

## Features

- **Daily Check-ins**: Track your mood, stress levels, and personal reflections
- **AI-Generated Mood Quiz**: Get personalized insights about your mental state
- **Contextual AI Copilot**: Access grounding exercises and micro-lessons
- **Conversational Assistant**: Chat with an AI companion for support
- **Adaptive UI**: Interface changes based on your current mood state
- **Responsive Design**: Works seamlessly on mobile and desktop

## Technology Stack

### Frontend
- React 18.2.0
- Tailwind CSS for styling
- Lucide React for icons
- Responsive design with mobile-first approach

### Backend
- Flask 2.3.3
- SQLite database
- RESTful API architecture
- CORS enabled for cross-origin requests

### Database
- SQLite with automatic initialization
- Simple schema for mood tracking data

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- Python 3.7 or higher
- pip (Python package manager)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd MindBridge/backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask backend:**
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd MindBridge/frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:3000`

## Usage

### Daily Check-ins
1. Navigate to the "Check-in" tab
2. Select your current mood from the dropdown
3. Adjust the stress level slider (1-10)
4. Add optional notes about your day
5. Submit your check-in

### Mood Quiz
1. Go to the "Quiz" tab
2. Click "Start Quiz" to begin
3. Answer the presented questions
4. Receive personalized insights about your mood

### AI Copilot
1. Visit the "Copilot" tab
2. Enter a request (e.g., "I need a grounding exercise")
3. Click "Get Support" to receive tailored exercises
4. Follow the provided instructions

### Chat Assistant
1. Open the "Chat" tab
2. Type your message in the input field
3. Press Enter or click Send
4. Receive supportive responses from the AI

## API Endpoints

### Check-ins
- `GET /api/checkin` - Retrieve last 5 check-ins
- `POST /api/checkin` - Submit new check-in

### Mood Quiz
- `GET /api/mood_quiz/generate` - Get quiz question
- `POST /api/mood_quiz/submit` - Submit answer and get insight

### AI Copilot
- `POST /api/copilot/grounding` - Get grounding exercise

### Chat
- `POST /api/chat` - Send message and get response

### Health Check
- `GET /api/health` - Check API status

## Database Schema

### checkins Table
```sql
CREATE TABLE checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT NOT NULL,
    stress_level INTEGER NOT NULL,
    notes TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Project Structure

```
MindBridge/
├── docs/
│   ├── PLANNING.md          # Project architecture and guidelines
│   └── TASK.md              # Development tasks and progress
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Tailwind CSS imports
│   ├── package.json         # Node.js dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   └── postcss.config.js    # PostCSS configuration
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── mindbridge.db       # SQLite database (auto-generated)
└── README.md              # This file
```

## Development

### Running Tests
```bash
# Frontend tests
cd frontend
npm test

# Backend tests (when implemented)
cd backend
python -m pytest
```

### Building for Production
```bash
# Build frontend
cd frontend
npm run build

# The built files will be in the 'build' directory
```

## Features in Detail

### Adaptive UI
The interface dynamically changes colors based on your mood:
- **Happy**: Green gradient background
- **Sad**: Gray gradient background
- **Stressed**: Red gradient background
- **Calm**: Blue gradient background
- **Neutral**: Default gray gradient

### AI Components
All AI features use rule-based logic for the MVP:
- **Mood Quiz**: Pre-defined questions with keyword-based insights
- **Copilot**: Keyword matching for grounding exercises
- **Chat**: Pattern-based conversational responses

### Responsive Design
- Mobile-first approach with Tailwind CSS
- Fixed bottom navigation for mobile
- Responsive grid layouts
- Touch-friendly interface elements

## Troubleshooting

### Common Issues

1. **Backend not starting:**
   - Check Python version compatibility
   - Ensure all dependencies are installed
   - Verify port 5000 is available

2. **Frontend not connecting to backend:**
   - Check that both servers are running
   - Verify API_BASE_URL in App.js
   - Check browser console for CORS errors

3. **Database issues:**
   - Database is created automatically on first run
   - Check file permissions in backend directory
   - Restart backend server if database seems corrupted

### Development Tips

1. **Hot Reload**: Both frontend and backend support hot reloading during development
2. **Debugging**: Use browser developer tools and Flask debug mode
3. **API Testing**: Use tools like Postman or curl to test API endpoints
4. **State Management**: All state is managed locally in React components

## Security Considerations

- No user authentication (MVP limitation)
- All data stored locally in SQLite
- Input validation on backend
- CORS enabled for development

## Future Enhancements

- User authentication and accounts
- Data export/import functionality
- Advanced AI integration with external APIs
- Real sensor data integration
- Progressive Web App (PWA) features
- Advanced analytics and insights

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Support

For issues or questions about setup and usage, please check the troubleshooting section or create an issue in the repository. 