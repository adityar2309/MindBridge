// Check-in related types matching backend schemas

export interface DailyCheckinCreate {
  mood_rating: number; // 1-10
  mood_category?: string;
  keywords?: string[];
  notes?: string;
  location?: string;
  weather?: string;
  energy_level?: number; // 1-10
  stress_level?: number; // 1-10
  sleep_quality?: number; // 1-10
  social_interaction?: number; // 1-10
}

export interface DailyCheckinResponse {
  checkin_id: number;
  user_id: number;
  timestamp: string; // ISO datetime string
  mood_rating: number;
  mood_category?: string;
  keywords: string[];
  notes?: string;
  location?: string;
  weather?: string;
  energy_level?: number;
  stress_level?: number;
  sleep_quality?: number;
  social_interaction?: number;
}

export interface DailyCheckinUpdate {
  mood_rating?: number;
  mood_category?: string;
  keywords?: string[];
  notes?: string;
  location?: string;
  weather?: string;
  energy_level?: number;
  stress_level?: number;
  sleep_quality?: number;
  social_interaction?: number;
}

export interface MoodTrend {
  date: string;
  mood_rating: number;
  energy_level?: number;
  stress_level?: number;
  sleep_quality?: number;
}

export interface MoodAnalytics {
  period: string; // daily, weekly, monthly
  average_mood: number;
  mood_range: { [key: string]: number }; // min, max
  most_common_category?: string;
  trend_direction: string; // improving, declining, stable
  trend_data: MoodTrend[];
  keyword_frequency: { [key: string]: number };
  correlation_insights: { [key: string]: any };
}

export interface CheckinStreak {
  current_streak: number;
  longest_streak: number;
  total_checkins: number;
  streak_start_date?: string;
  days_since_last_checkin: number;
}

export interface QuickMoodEntry {
  mood_rating: number;
  mood_category?: string;
  keywords?: string[];
}

// Valid mood categories from backend
export const VALID_MOOD_CATEGORIES = [
  'happy', 'content', 'calm', 'excited', 'optimistic',
  'sad', 'anxious', 'stressed', 'angry', 'frustrated',
  'tired', 'energetic', 'focused', 'confused', 'lonely',
  'grateful', 'hopeful', 'overwhelmed', 'peaceful', 'neutral'
] as const;

export type MoodCategory = typeof VALID_MOOD_CATEGORIES[number];

// Legacy types for backward compatibility (to be removed)
export interface CheckinCreate extends DailyCheckinCreate {}
export interface DailyCheckin extends DailyCheckinResponse {} 