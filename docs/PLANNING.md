# MindBridge - Mood & Mental Health Tracker

## Project Overview
MindBridge is a personal mood and mental health tracking application with AI-driven interactive elements. The application helps users track their daily mood, stress levels, and provides supportive AI-powered features.

## Architecture

### Frontend (ReactJS)
- **Technology Stack**: ReactJS, Tailwind CSS, lucide-react
- **Structure**: Single-page application with component-based architecture
- **Main Component**: App.js with dynamic page rendering
- **State Management**: React hooks (useState, useEffect)

### Backend (Flask)
- **Technology Stack**: Flask, SQLite
- **Structure**: Single app.py file with RESTful API
- **Database**: SQLite (mindbridge.db)
- **CORS**: Enabled for frontend-backend communication

### Database Schema
```sql
checkins:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- mood: TEXT
- stress_level: INTEGER (1-10)
- notes: TEXT
- timestamp: DATETIME DEFAULT CURRENT_TIMESTAMP
```

## Core Features

### 1. Daily Check-ins
- Mood tracking (1-5 scale or text)
- Stress level (1-10 scale)
- Notes/reflections
- History display (last 5 entries)

### 2. AI-Generated Mood Quiz
- Pre-defined questions with multiple choice
- Simple insight generation based on answers
- Static question cycling

### 3. Contextual AI Copilot
- Keyword-based grounding exercises
- Pre-defined micro-lessons
- Simple rule-based responses

### 4. Conversational Assistant
- Chat interface
- Rule-based conversational responses
- Simple mood-based reply generation

### 5. Adaptive UI/UX
- Dynamic background colors based on mood
- Responsive design with Tailwind CSS
- Mobile-first approach

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

## File Structure
```
MindBridge/
├── docs/
│   ├── PLANNING.md
│   └── TASK.md
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── mindbridge.db (generated)
└── README.md
```

## Development Guidelines

### Code Style
- Use functional components with hooks
- Follow PEP8 for Python code
- Extensive commenting
- Error handling with try-catch/try-except

### UI/UX Principles
- Clean, modern design with Tailwind CSS
- Responsive layout
- Accessibility considerations
- No alert() dialogs - use UI elements

### Testing
- Unit tests for backend functions
- Frontend component testing
- Integration testing for API endpoints

## Security Considerations
- No authentication required for MVP
- Input validation on backend
- CORS configuration
- SQL injection prevention

## Deployment
- Frontend: Serve static files
- Backend: Flask development server
- Database: SQLite file-based storage

## Future Enhancements
- User authentication
- Data export/import
- Advanced AI integration
- Real sensor data integration
- Mobile app version 