// User Types
export interface User {
  id: string;
  email: string;
  username: string;
  firstName?: string;
  lastName?: string;
  dateOfBirth?: string;
  gender?: 'male' | 'female' | 'other' | 'prefer_not_to_say';
  timezone: string;
  isActive: boolean;
  createdAt: string;
  settings: UserSettings;
}

export interface UserSettings {
  notificationsEnabled: boolean;
  checkinReminders: boolean;
  reminderTime: string;
  dataRetentionDays: number;
  shareDataForResearch: boolean;
  theme: 'light' | 'dark' | 'system';
  language: string;
  privacyLevel: 'low' | 'medium' | 'high';
}

// Check-in Types
export interface DailyCheckin {
  id: string;
  userId: string;
  checkinDate: string;
  overallMood: number; // 1-10 scale
  energyLevel: number; // 1-10 scale
  stressLevel: number; // 1-10 scale
  sleepQuality: number; // 1-10 scale
  socialInteraction: number; // 1-10 scale
  moodCategories: MoodCategory[];
  moodKeywords: string[];
  notes?: string;
  location?: string;
  weather?: string;
  createdAt: string;
  updatedAt: string;
}

export interface MoodCategory {
  category: string;
  intensity: number; // 1-5 scale
}

export interface CheckinCreate {
  overallMood: number;
  energyLevel: number;
  stressLevel: number;
  sleepQuality: number;
  socialInteraction: number;
  moodCategories: MoodCategory[];
  moodKeywords: string[];
  notes?: string;
  location?: string;
  weather?: string;
}

// Analytics Types
export interface MoodTrend {
  date: string;
  overallMood: number;
  energyLevel: number;
  stressLevel: number;
  sleepQuality: number;
}

export interface MoodAnalytics {
  averageMood: number;
  moodTrend: 'improving' | 'declining' | 'stable';
  streakDays: number;
  totalCheckins: number;
  weeklyTrends: MoodTrend[];
  monthlyTrends: MoodTrend[];
  correlations: {
    sleepMoodCorrelation: number;
    energyMoodCorrelation: number;
    stressMoodCorrelation: number;
  };
}

// Navigation Types
export type RootStackParamList = {
  Welcome: undefined;
  Login: undefined;
  Register: undefined;
  Main: undefined;
  CheckinFlow: undefined;
  Profile: undefined;
  Settings: undefined;
  Analytics: undefined;
  History: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  Checkin: undefined;
  Analytics: undefined;
  Profile: undefined;
};

// API Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: string[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
}

// Redux State Types
export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

export interface CheckinState {
  currentCheckin: Partial<CheckinCreate>;
  recentCheckins: DailyCheckin[];
  isLoading: boolean;
  error: string | null;
  lastCheckinDate: string | null;
}

export interface AnalyticsState {
  moodAnalytics: MoodAnalytics | null;
  isLoading: boolean;
  error: string | null;
  timeRange: 'week' | 'month' | 'quarter' | 'year';
}

export interface RootState {
  auth: AuthState;
  checkin: CheckinState;
  analytics: AnalyticsState;
}

// Component Props Types
export interface ThemeColors {
  primary: string;
  secondary: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  error: string;
  success: string;
  warning: string;
}

export interface Theme {
  colors: ThemeColors;
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
  };
  typography: {
    h1: {
      fontSize: number;
      fontWeight: string;
    };
    h2: {
      fontSize: number;
      fontWeight: string;
    };
    h3: {
      fontSize: number;
      fontWeight: string;
    };
    body: {
      fontSize: number;
      fontWeight: string;
    };
    caption: {
      fontSize: number;
      fontWeight: string;
    };
  };
} 