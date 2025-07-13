import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';
import { 
  DailyCheckinCreate,
  DailyCheckinResponse,
  DailyCheckinUpdate,
  MoodAnalytics,
  CheckinStreak,
  MoodTrend,
  QuickMoodEntry,
  // Legacy types for backward compatibility
  CheckinCreate, 
  DailyCheckin 
} from '@/types';

class CheckinService {
  /**
   * Create a new daily check-in.
   */
  async createCheckin(checkinData: DailyCheckinCreate | CheckinCreate, userId: number): Promise<DailyCheckinResponse> {
    try {
      const checkin = await apiClient.post<DailyCheckinResponse>(
        `${API_ENDPOINTS.checkins.create}?user_id=${userId}`,
        checkinData
      );
      return checkin;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Create a quick mood entry (simplified check-in).
   */
  async createQuickMood(moodData: QuickMoodEntry, userId: number): Promise<DailyCheckinResponse> {
    try {
      const checkinData: DailyCheckinCreate = {
        mood_rating: moodData.mood_rating,
        mood_category: moodData.mood_category,
        keywords: moodData.keywords,
      };
      
      return await this.createCheckin(checkinData, userId);
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Get user's check-ins with pagination.
   */
  async getUserCheckins(
    userId: number, 
    options: {
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<DailyCheckinResponse[]> {
    try {
      const { limit = 30, offset = 0 } = options;
      const checkins = await apiClient.get<DailyCheckinResponse[]>(
        `${API_ENDPOINTS.checkins.list}?user_id=${userId}&limit=${limit}&offset=${offset}`
      );
      return checkins;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Get a specific check-in by ID.
   */
  async getCheckin(checkinId: number, userId: number): Promise<DailyCheckinResponse> {
    try {
      const checkin = await apiClient.get<DailyCheckinResponse>(
        `${API_ENDPOINTS.checkins.list}/${checkinId}?user_id=${userId}`
      );
      return checkin;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Update an existing check-in.
   */
  async updateCheckin(
    checkinId: number, 
    updateData: DailyCheckinUpdate, 
    userId: number
  ): Promise<DailyCheckinResponse> {
    try {
      const checkin = await apiClient.put<DailyCheckinResponse>(
        `${API_ENDPOINTS.checkins.list}/${checkinId}?user_id=${userId}`,
        updateData
      );
      return checkin;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Delete a check-in.
   */
  async deleteCheckin(checkinId: number, userId: number): Promise<void> {
    try {
      await apiClient.delete(
        `${API_ENDPOINTS.checkins.list}/${checkinId}?user_id=${userId}`
      );
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Get mood analytics for a time period.
   */
  async getMoodAnalytics(
    userId: number, 
    period: 'daily' | 'weekly' | 'monthly' = 'monthly'
  ): Promise<MoodAnalytics> {
    try {
      const analytics = await apiClient.get<MoodAnalytics>(
        `${API_ENDPOINTS.checkins.analytics}?user_id=${userId}&period=${period}`
      );
      return analytics;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Get check-in streak information.
   */
  async getCheckinStreak(userId: number): Promise<CheckinStreak> {
    try {
      const streak = await apiClient.get<CheckinStreak>(
        `${API_ENDPOINTS.checkins.streak}?user_id=${userId}`
      );
      return streak;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Get mood trends for a specific time range.
   */
  async getMoodTrends(
    userId: number, 
    days: number = 30
  ): Promise<MoodTrend[]> {
    try {
      const trends = await apiClient.get<MoodTrend[]>(
        `${API_ENDPOINTS.checkins.list}/trends?user_id=${userId}&days=${days}`
      );
      return trends;
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Get recent check-ins (shortcut method).
   */
  async getRecentCheckins(userId: number, limit: number = 5): Promise<DailyCheckinResponse[]> {
    return await this.getUserCheckins(userId, { limit, offset: 0 });
  }

  /**
   * Check if user has checked in today.
   */
  async hasCheckedInToday(userId: number): Promise<boolean> {
    try {
      const today = new Date().toISOString().split('T')[0];
      const recentCheckins = await this.getRecentCheckins(userId, 1);
      
      if (recentCheckins.length === 0) {
        return false;
      }
      
      const latestCheckinDate = recentCheckins[0].timestamp.split('T')[0];
      return latestCheckinDate === today;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get today's check-in if it exists.
   */
  async getTodaysCheckin(userId: number): Promise<DailyCheckinResponse | null> {
    try {
      const today = new Date().toISOString().split('T')[0];
      const recentCheckins = await this.getRecentCheckins(userId, 5);
      
      const todaysCheckin = recentCheckins.find(checkin => 
        checkin.timestamp.split('T')[0] === today
      );
      
      return todaysCheckin || null;
    } catch (error) {
      return null;
    }
  }

  /**
   * Get dashboard data (combined analytics and recent check-ins).
   */
  async getDashboardData(userId: number): Promise<{
    recentCheckins: DailyCheckinResponse[];
    analytics: MoodAnalytics;
    streak: CheckinStreak;
    todaysCheckin: DailyCheckinResponse | null;
  }> {
    try {
      const [recentCheckins, analytics, streak, todaysCheckin] = await Promise.all([
        this.getRecentCheckins(userId, 5),
        this.getMoodAnalytics(userId, 'weekly'),
        this.getCheckinStreak(userId),
        this.getTodaysCheckin(userId),
      ]);

      return {
        recentCheckins,
        analytics,
        streak,
        todaysCheckin,
      };
    } catch (error) {
      throw this.handleCheckinError(error);
    }
  }

  /**
   * Handle check-in service errors with consistent formatting.
   */
  private handleCheckinError(error: any): Error {
    if (error.response?.data?.message) {
      return new Error(error.response.data.message);
    }
    if (error.message) {
      return new Error(error.message);
    }
    return new Error('Check-in operation failed');
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

const checkinService = new CheckinService();
export { checkinService };
export default checkinService; 