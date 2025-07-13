import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';
import { MoodAnalytics } from '@/types';

class AnalyticsService {
  /**
   * Get comprehensive mood analytics for a time period.
   */
  async getMoodAnalytics(timeRange: 'week' | 'month' | 'quarter' | 'year'): Promise<MoodAnalytics> {
    try {
      const analytics = await apiClient.get<MoodAnalytics>(
        `${API_ENDPOINTS.checkins.analytics}?range=${timeRange}`
      );
      return analytics;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get streak data and check-in statistics.
   */
  async getStreakData(): Promise<{
    currentStreak: number;
    longestStreak: number;
    totalCheckins: number;
    streakHistory: Array<{ date: string; hasCheckin: boolean }>;
  }> {
    try {
      const streakData = await apiClient.get<{
        currentStreak: number;
        longestStreak: number;
        totalCheckins: number;
        streakHistory: Array<{ date: string; hasCheckin: boolean }>;
      }>(API_ENDPOINTS.checkins.streak);
      return streakData;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get mood correlations with various factors.
   */
  async getMoodCorrelations(timeRange: string): Promise<{
    sleepMoodCorrelation: number;
    energyMoodCorrelation: number;
    stressMoodCorrelation: number;
    socialMoodCorrelation?: number;
    weatherMoodCorrelation?: number;
  }> {
    try {
      const correlations = await apiClient.get<{
        sleepMoodCorrelation: number;
        energyMoodCorrelation: number;
        stressMoodCorrelation: number;
        socialMoodCorrelation?: number;
        weatherMoodCorrelation?: number;
      }>(`${API_ENDPOINTS.checkins.analytics}/correlations?range=${timeRange}`);
      return correlations;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get detailed trend analysis.
   */
  async getTrendAnalysis(timeRange: string): Promise<{
    moodTrend: 'improving' | 'declining' | 'stable';
    trendPercentage: number;
    significantChanges: Array<{
      date: string;
      change: 'increase' | 'decrease';
      magnitude: number;
      factor: string;
    }>;
  }> {
    try {
      const trends = await apiClient.get<{
        moodTrend: 'improving' | 'declining' | 'stable';
        trendPercentage: number;
        significantChanges: Array<{
          date: string;
          change: 'increase' | 'decrease';
          magnitude: number;
          factor: string;
        }>;
      }>(`${API_ENDPOINTS.checkins.analytics}/trends?range=${timeRange}`);
      return trends;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get mood patterns by day of week, time of day, etc.
   */
  async getMoodPatterns(timeRange: string): Promise<{
    dayOfWeekPatterns: Array<{ day: string; averageMood: number; checkinCount: number }>;
    monthlyPatterns: Array<{ month: string; averageMood: number; checkinCount: number }>;
    categoryFrequency: Array<{ category: string; frequency: number; averageIntensity: number }>;
  }> {
    try {
      const patterns = await apiClient.get<{
        dayOfWeekPatterns: Array<{ day: string; averageMood: number; checkinCount: number }>;
        monthlyPatterns: Array<{ month: string; averageMood: number; checkinCount: number }>;
        categoryFrequency: Array<{ category: string; frequency: number; averageIntensity: number }>;
      }>(`${API_ENDPOINTS.checkins.analytics}/patterns?range=${timeRange}`);
      return patterns;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get AI-generated insights and recommendations.
   */
  async getAIInsights(): Promise<{
    insights: Array<{
      type: 'trend' | 'pattern' | 'correlation' | 'recommendation';
      title: string;
      description: string;
      confidence: number;
      actionable: boolean;
    }>;
    personalizedRecommendations: string[];
  }> {
    try {
      const insights = await apiClient.get<{
        insights: Array<{
          type: 'trend' | 'pattern' | 'correlation' | 'recommendation';
          title: string;
          description: string;
          confidence: number;
          actionable: boolean;
        }>;
        personalizedRecommendations: string[];
      }>(API_ENDPOINTS.ai.insights);
      return insights;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Export analytics data in various formats.
   */
  async exportData(format: 'csv' | 'json', options?: {
    timeRange?: string;
    includeCharts?: boolean;
    includeInsights?: boolean;
  }): Promise<string | Blob> {
    try {
      const params = new URLSearchParams({ format });
      
      if (options?.timeRange) {
        params.append('range', options.timeRange);
      }
      if (options?.includeCharts) {
        params.append('include_charts', 'true');
      }
      if (options?.includeInsights) {
        params.append('include_insights', 'true');
      }

      const exportData = await apiClient.get<string>(
        `${API_ENDPOINTS.checkins.analytics}/export?${params.toString()}`
      );
      return exportData;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get comparative analytics (compare different time periods).
   */
  async getComparativeAnalytics(
    currentPeriod: string,
    previousPeriod: string
  ): Promise<{
    currentPeriodStats: MoodAnalytics;
    previousPeriodStats: MoodAnalytics;
    comparison: {
      moodChange: number;
      energyChange: number;
      stressChange: number;
      sleepChange: number;
      significantChanges: string[];
    };
  }> {
    try {
      const comparison = await apiClient.get<{
        currentPeriodStats: MoodAnalytics;
        previousPeriodStats: MoodAnalytics;
        comparison: {
          moodChange: number;
          energyChange: number;
          stressChange: number;
          sleepChange: number;
          significantChanges: string[];
        };
      }>(`${API_ENDPOINTS.checkins.analytics}/compare?current=${currentPeriod}&previous=${previousPeriod}`);
      return comparison;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get prediction model results for mood forecasting.
   */
  async getMoodPrediction(daysAhead: number = 7): Promise<{
    predictions: Array<{
      date: string;
      predictedMood: number;
      confidence: number;
      factors: string[];
    }>;
    accuracy: number;
    modelVersion: string;
  }> {
    try {
      const prediction = await apiClient.get<{
        predictions: Array<{
          date: string;
          predictedMood: number;
          confidence: number;
          factors: string[];
        }>;
        accuracy: number;
        modelVersion: string;
      }>(`${API_ENDPOINTS.ai.insights}/prediction?days=${daysAhead}`);
      return prediction;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get goal tracking and achievement data.
   */
  async getGoalProgress(): Promise<{
    activeGoals: Array<{
      id: string;
      type: 'mood' | 'checkin_streak' | 'category_frequency';
      target: number;
      current: number;
      deadline?: string;
      achieved: boolean;
    }>;
    achievements: Array<{
      id: string;
      title: string;
      description: string;
      unlockedAt: string;
      category: string;
    }>;
  }> {
    try {
      const progress = await apiClient.get<{
        activeGoals: Array<{
          id: string;
          type: 'mood' | 'checkin_streak' | 'category_frequency';
          target: number;
          current: number;
          deadline?: string;
          achieved: boolean;
        }>;
        achievements: Array<{
          id: string;
          title: string;
          description: string;
          unlockedAt: string;
          category: string;
        }>;
      }>(`${API_ENDPOINTS.checkins.analytics}/goals`);
      return progress;
    } catch (error) {
      throw error;
    }
  }
}

export const analyticsService = new AnalyticsService(); 