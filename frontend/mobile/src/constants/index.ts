// API Configuration
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000/api/v1' 
  : 'https://api.mindbridge.app/v1';

export const API_ENDPOINTS = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    refresh: '/auth/refresh',
    logout: '/auth/logout',
    profile: '/auth/profile',
  },
  checkins: {
    create: '/checkins',
    list: '/checkins',
    analytics: '/checkins/analytics',
    streak: '/checkins/streak',
  },
  passiveData: {
    upload: '/passive-data',
    list: '/passive-data',
  },
  ai: {
    insights: '/ai/insights',
    chat: '/ai/chat',
  },
} as const;

// App Configuration
export const APP_CONFIG = {
  name: 'MindBridge',
  version: '1.0.0',
  defaultLanguage: 'en',
  defaultTheme: 'system' as const,
  maxRetries: 3,
  requestTimeout: 10000,
  tokenRefreshThreshold: 300000, // 5 minutes
} as const;

// Validation Constants
export const VALIDATION = {
  password: {
    minLength: 8,
    maxLength: 128,
    requireUppercase: true,
    requireLowercase: true,
    requireNumbers: true,
    requireSpecialChars: true,
  },
  username: {
    minLength: 3,
    maxLength: 30,
    allowedPattern: /^[a-zA-Z0-9_]+$/,
  },
  email: {
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  },
} as const;

// Mood Categories with descriptions
export const MOOD_CATEGORIES = [
  { id: 'happy', label: 'Happy', icon: '😊', description: 'Feeling joyful and positive' },
  { id: 'sad', label: 'Sad', icon: '😢', description: 'Feeling down or melancholy' },
  { id: 'anxious', label: 'Anxious', icon: '😰', description: 'Feeling worried or nervous' },
  { id: 'stressed', label: 'Stressed', icon: '😤', description: 'Feeling overwhelmed or pressured' },
  { id: 'calm', label: 'Calm', icon: '😌', description: 'Feeling peaceful and relaxed' },
  { id: 'energetic', label: 'Energetic', icon: '⚡', description: 'Feeling full of energy' },
  { id: 'tired', label: 'Tired', icon: '😴', description: 'Feeling fatigued or sleepy' },
  { id: 'focused', label: 'Focused', icon: '🎯', description: 'Feeling concentrated and alert' },
  { id: 'creative', label: 'Creative', icon: '🎨', description: 'Feeling inspired and imaginative' },
  { id: 'social', label: 'Social', icon: '👥', description: 'Feeling connected with others' },
  { id: 'motivated', label: 'Motivated', icon: '🔥', description: 'Feeling driven to achieve goals' },
  { id: 'grateful', label: 'Grateful', icon: '🙏', description: 'Feeling thankful and appreciative' },
] as const;

// Common mood keywords
export const MOOD_KEYWORDS = [
  'peaceful', 'excited', 'overwhelmed', 'content', 'frustrated', 'hopeful',
  'lonely', 'confident', 'worried', 'inspired', 'angry', 'serene',
  'restless', 'optimistic', 'disappointed', 'proud', 'jealous', 'compassionate',
  'fearful', 'euphoric', 'bored', 'determined', 'melancholic', 'ecstatic',
] as const;

// Scale labels for sliders
export const SCALE_LABELS = {
  mood: ['Terrible', 'Poor', 'Fair', 'Good', 'Great'],
  energy: ['Exhausted', 'Low', 'Moderate', 'High', 'Energized'],
  stress: ['None', 'Mild', 'Moderate', 'High', 'Extreme'],
  sleep: ['Terrible', 'Poor', 'Fair', 'Good', 'Excellent'],
  social: ['Isolated', 'Limited', 'Some', 'Good', 'Very Social'],
} as const;

// Chart configurations
export const CHART_CONFIG = {
  colors: {
    mood: '#6366F1',
    energy: '#22C55E',
    stress: '#EF4444',
    sleep: '#8B5CF6',
  },
  gradients: {
    mood: ['#6366F1', '#8B5CF6'],
    energy: ['#22C55E', '#84CC16'],
    stress: ['#EF4444', '#F97316'],
    sleep: ['#8B5CF6', '#A78BFA'],
  },
} as const;

// Notification categories
export const NOTIFICATION_TYPES = {
  CHECKIN_REMINDER: 'checkin_reminder',
  STREAK_MILESTONE: 'streak_milestone',
  INSIGHT_AVAILABLE: 'insight_available',
  WEEKLY_SUMMARY: 'weekly_summary',
} as const;

// Feature flags (can be used for A/B testing or gradual rollouts)
export const FEATURE_FLAGS = {
  ENABLE_PASSIVE_DATA: true,
  ENABLE_AI_INSIGHTS: true,
  ENABLE_SOCIAL_FEATURES: false,
  ENABLE_ANALYTICS_EXPORT: true,
  ENABLE_DARK_MODE: true,
} as const;

// Storage keys for AsyncStorage
export const STORAGE_KEYS = {
  AUTH_TOKEN: '@mindbridge/auth_token',
  REFRESH_TOKEN: '@mindbridge/refresh_token',
  USER_SETTINGS: '@mindbridge/user_settings',
  THEME_PREFERENCE: '@mindbridge/theme_preference',
  ONBOARDING_COMPLETED: '@mindbridge/onboarding_completed',
  LAST_CHECKIN_DATE: '@mindbridge/last_checkin_date',
} as const; 