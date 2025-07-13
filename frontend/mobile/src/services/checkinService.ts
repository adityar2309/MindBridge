import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';
import { CheckinCreate, DailyCheckin, MoodAnalytics } from '@/types';

class CheckinService {
  /**
   * Create a new daily check-in.
   */
  async createCheckin(checkinData: CheckinCreate): Promise<DailyCheckin> {
    try {
      const checkin = await apiClient.post<DailyCheckin>(
        API_ENDPOINTS.checkins.create,
        checkinData
      );
      return checkin;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get recent check-ins.
   */
  async getRecentCheckins(limit: number = 7): Promise<DailyCheckin[]> {
    try {
      const checkins = await apiClient.get<DailyCheckin[]>(
        `${API_ENDPOINTS.checkins.list}?limit=${limit}`
      );
      return checkins;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get check-ins within a date range.
   */
  async getCheckinsByDateRange(startDate: string, endDate: string): Promise<DailyCheckin[]> {
    try {
      const checkins = await apiClient.get<DailyCheckin[]>(
        `${API_ENDPOINTS.checkins.list}?start_date=${startDate}&end_date=${endDate}`
      );
      return checkins;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get a specific check-in by date.
   */
  async getCheckinByDate(date: string): Promise<DailyCheckin | null> {
    try {
      const checkin = await apiClient.get<DailyCheckin>(
        `${API_ENDPOINTS.checkins.list}/${date}`
      );
      return checkin;
    } catch (error) {
      // Return null if no check-in found for the date
      if (error instanceof Error && (error.message?.includes('404') || error.message?.includes('not found'))) {
        return null;
      }
      throw error;
    }
  }

  /**
   * Update an existing check-in.
   */
  async updateCheckin(id: string, data: Partial<CheckinCreate>): Promise<DailyCheckin> {
    try {
      const updatedCheckin = await apiClient.patch<DailyCheckin>(
        `${API_ENDPOINTS.checkins.list}/${id}`,
        data
      );
      return updatedCheckin;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Delete a check-in.
   */
  async deleteCheckin(id: string): Promise<void> {
    try {
      await apiClient.delete(`${API_ENDPOINTS.checkins.list}/${id}`);
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get streak information.
   */
  async getStreak(): Promise<{ currentStreak: number; longestStreak: number; totalCheckins: number }> {
    try {
      const streakData = await apiClient.get<{
        currentStreak: number;
        longestStreak: number;
        totalCheckins: number;
      }>(API_ENDPOINTS.checkins.streak);
      return streakData;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get mood analytics for a specific time period.
   */
  async getAnalytics(timeRange: 'week' | 'month' | 'quarter' | 'year'): Promise<MoodAnalytics> {
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
   * Get mood patterns and correlations.
   */
  async getMoodCorrelations(timeRange: string): Promise<{
    sleepMoodCorrelation: number;
    energyMoodCorrelation: number;
    stressMoodCorrelation: number;
  }> {
    try {
      const correlations = await apiClient.get<{
        sleepMoodCorrelation: number;
        energyMoodCorrelation: number;
        stressMoodCorrelation: number;
      }>(`${API_ENDPOINTS.checkins.analytics}/correlations?range=${timeRange}`);
      return correlations;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get mood trends over time.
   */
  async getMoodTrends(timeRange: string): Promise<any[]> {
    try {
      const trends = await apiClient.get<any[]>(
        `${API_ENDPOINTS.checkins.analytics}/trends?range=${timeRange}`
      );
      return trends;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Export check-in data.
   */
  async exportData(format: 'csv' | 'json', dateRange?: { start: string; end: string }): Promise<string> {
    try {
      const params = new URLSearchParams({ format });
      if (dateRange) {
        params.append('start_date', dateRange.start);
        params.append('end_date', dateRange.end);
      }

      const exportData = await apiClient.get<string>(
        `${API_ENDPOINTS.checkins.list}/export?${params.toString()}`
      );
      return exportData;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get suggested mood keywords based on recent patterns.
   */
  async getSuggestedKeywords(): Promise<string[]> {
    try {
      const keywords = await apiClient.get<string[]>(
        `${API_ENDPOINTS.checkins.analytics}/suggested-keywords`
      );
      return keywords;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get mood insights and recommendations.
   */
  async getMoodInsights(): Promise<{
    insights: string[];
    recommendations: string[];
    patterns: any[];
  }> {
    try {
      const insights = await apiClient.get<{
        insights: string[];
        recommendations: string[];
        patterns: any[];
      }>(`${API_ENDPOINTS.checkins.analytics}/insights`);
      return insights;
    } catch (error) {
      throw error;
    }
  }
}

export const checkinService = new CheckinService(); 