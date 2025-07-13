import { Theme } from '@/types';

export const lightTheme: Theme = {
  colors: {
    primary: '#6366F1', // Indigo
    secondary: '#8B5CF6', // Purple
    background: '#FFFFFF',
    surface: '#F8FAFC',
    text: '#1E293B',
    textSecondary: '#64748B',
    border: '#E2E8F0',
    error: '#EF4444',
    success: '#10B981',
    warning: '#F59E0B',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 16,
  },
  typography: {
    h1: {
      fontSize: 32,
      fontWeight: 'bold',
    },
    h2: {
      fontSize: 24,
      fontWeight: 'bold',
    },
    h3: {
      fontSize: 20,
      fontWeight: '600',
    },
    body: {
      fontSize: 16,
      fontWeight: 'normal',
    },
    caption: {
      fontSize: 14,
      fontWeight: 'normal',
    },
  },
};

export const darkTheme: Theme = {
  ...lightTheme,
  colors: {
    primary: '#818CF8', // Lighter indigo for dark mode
    secondary: '#A78BFA', // Lighter purple for dark mode
    background: '#0F172A',
    surface: '#1E293B',
    text: '#F1F5F9',
    textSecondary: '#94A3B8',
    border: '#334155',
    error: '#F87171',
    success: '#34D399',
    warning: '#FBBF24',
  },
};

export const moodColors = {
  1: '#EF4444', // Very sad - Red
  2: '#F97316', // Sad - Orange
  3: '#EAB308', // Somewhat sad - Yellow
  4: '#84CC16', // Neutral - Light green
  5: '#22C55E', // Okay - Green
  6: '#06B6D4', // Good - Cyan
  7: '#3B82F6', // Happy - Blue
  8: '#8B5CF6', // Very happy - Purple
  9: '#EC4899', // Excellent - Pink
  10: '#F59E0B', // Amazing - Amber
};

export const categoryColors = {
  anxious: '#EF4444',
  stressed: '#F97316',
  tired: '#64748B',
  energetic: '#22C55E',
  focused: '#3B82F6',
  creative: '#8B5CF6',
  social: '#EC4899',
  calm: '#06B6D4',
  motivated: '#84CC16',
  grateful: '#F59E0B',
}; 