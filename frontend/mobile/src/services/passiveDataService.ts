import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';

// Types for passive data (matches backend schemas)
export interface PassiveDataCreate {
  data_type: string;
  value: number | string | object;
  source: string;
  timestamp?: string;
  meta_data?: { [key: string]: any };
  quality_score?: number;
}

export interface PassiveDataResponse {
  data_point_id: number;
  user_id: number;
  timestamp: string;
  data_type: string;
  value: number | string | object;
  source: string;
  meta_data: { [key: string]: any };
  quality_score: number;
  processed: boolean;
}

export interface PassiveDataBulkCreate {
  data_points: PassiveDataCreate[];
  process_async?: boolean;
}

export interface BulkIngestResponse {
  success_count: number;
  error_count: number;
  total_count: number;
  created_ids: number[];
  processing_async: boolean;
}

export interface DataAggregation {
  data_type: string;
  period: string;
  start_date: string;
  end_date: string;
  aggregated_value: number | object;
  count: number;
  source_breakdown: { [key: string]: number };
}

export interface HealthMetrics {
  date: string;
  sleep_duration?: number;
  sleep_quality?: number;
  step_count?: number;
  exercise_duration?: number;
  heart_rate_avg?: number;
  screen_time?: number;
}

// Data type enums matching backend
export enum DataType {
  SLEEP_DURATION = 'sleep_duration',
  SLEEP_QUALITY = 'sleep_quality',
  STEP_COUNT = 'step_count',
  EXERCISE_DURATION = 'exercise_duration',
  HEART_RATE = 'heart_rate',
  SCREEN_TIME = 'screen_time',
  LOCATION_SUMMARY = 'location_summary',
  SOCIAL_INTERACTION = 'social_interaction',
  NOTIFICATION_COUNT = 'notification_count',
}

export enum DataSource {
  HEALTH_KIT = 'HealthKit',
  GOOGLE_FIT = 'GoogleFit',
  DEVICE_SENSORS = 'device_sensors',
  INTERNAL_TRACKING = 'internal_tracking',
  SMARTPHONE = 'smartphone',
}

class PassiveDataService {
  /**
   * Create a single passive data point.
   */
  async createDataPoint(dataPoint: PassiveDataCreate, userId: number): Promise<PassiveDataResponse> {
    try {
      const response = await apiClient.post<PassiveDataResponse>(
        `${API_ENDPOINTS.passiveData.create}?user_id=${userId}`,
        dataPoint
      );
      return response;
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Bulk create multiple passive data points.
   */
  async bulkCreateDataPoints(
    bulkData: PassiveDataBulkCreate, 
    userId: number
  ): Promise<BulkIngestResponse> {
    try {
      const response = await apiClient.post<BulkIngestResponse>(
        `${API_ENDPOINTS.passiveData.bulk}?user_id=${userId}`,
        bulkData
      );
      return response;
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Get passive data points with filtering and pagination.
   */
  async getDataPoints(
    userId: number,
    options: {
      data_type?: string;
      source?: string;
      start_date?: string;
      end_date?: string;
      limit?: number;
      offset?: number;
    } = {}
  ): Promise<PassiveDataResponse[]> {
    try {
      const params = new URLSearchParams({ user_id: userId.toString() });
      
      Object.entries(options).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value.toString());
        }
      });

      const response = await apiClient.get<PassiveDataResponse[]>(
        `${API_ENDPOINTS.passiveData.list}?${params.toString()}`
      );
      return response;
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Get aggregated data by time period.
   */
  async getAggregatedData(
    userId: number,
    dataType: string,
    period: 'hourly' | 'daily' | 'weekly' | 'monthly',
    options: {
      start_date?: string;
      end_date?: string;
    } = {}
  ): Promise<DataAggregation[]> {
    try {
      const params = new URLSearchParams({
        user_id: userId.toString(),
        data_type: dataType,
        period: period,
      });

      Object.entries(options).forEach(([key, value]) => {
        if (value !== undefined) {
          params.append(key, value);
        }
      });

      const response = await apiClient.get<DataAggregation[]>(
        `${API_ENDPOINTS.passiveData.aggregate}?${params.toString()}`
      );
      return response;
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Get health metrics summary for a specific date.
   */
  async getHealthMetrics(
    userId: number,
    date?: string
  ): Promise<HealthMetrics> {
    try {
      const params = new URLSearchParams({ user_id: userId.toString() });
      if (date) {
        params.append('date', date);
      }

      const response = await apiClient.get<HealthMetrics>(
        `${API_ENDPOINTS.passiveData.healthMetrics}?${params.toString()}`
      );
      return response;
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Record sleep data.
   */
  async recordSleepData(
    userId: number,
    sleepData: {
      duration: number; // hours
      quality: number; // 1-10
      efficiency?: number; // percentage
      bedtime?: string;
      wake_time?: string;
    },
    source: DataSource = DataSource.INTERNAL_TRACKING
  ): Promise<PassiveDataResponse[]> {
    try {
      const dataPoints: PassiveDataCreate[] = [
        {
          data_type: DataType.SLEEP_DURATION,
          value: sleepData.duration,
          source: source,
          meta_data: {
            bedtime: sleepData.bedtime,
            wake_time: sleepData.wake_time,
          },
        },
        {
          data_type: DataType.SLEEP_QUALITY,
          value: sleepData.quality,
          source: source,
        },
      ];

      const bulkResponse = await this.bulkCreateDataPoints(
        { data_points: dataPoints },
        userId
      );

      // Return created data points
      return await this.getDataPoints(userId, {
        data_type: DataType.SLEEP_DURATION,
        limit: dataPoints.length,
      });
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Record activity data.
   */
  async recordActivityData(
    userId: number,
    activityData: {
      steps?: number;
      exercise_duration?: number; // minutes
      calories_burned?: number;
    },
    source: DataSource = DataSource.DEVICE_SENSORS
  ): Promise<PassiveDataResponse[]> {
    try {
      const dataPoints: PassiveDataCreate[] = [];

      if (activityData.steps !== undefined) {
        dataPoints.push({
          data_type: DataType.STEP_COUNT,
          value: activityData.steps,
          source: source,
        });
      }

      if (activityData.exercise_duration !== undefined) {
        dataPoints.push({
          data_type: DataType.EXERCISE_DURATION,
          value: activityData.exercise_duration,
          source: source,
        });
      }

      if (dataPoints.length === 0) {
        return [];
      }

      await this.bulkCreateDataPoints({ data_points: dataPoints }, userId);
      
      // Return recent activity data
      return await this.getDataPoints(userId, {
        limit: dataPoints.length,
      });
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Record screen time data.
   */
  async recordScreenTime(
    userId: number,
    screenTimeHours: number,
    appUsageData?: { [appName: string]: number },
    source: DataSource = DataSource.SMARTPHONE
  ): Promise<PassiveDataResponse> {
    try {
      const dataPoint: PassiveDataCreate = {
        data_type: DataType.SCREEN_TIME,
        value: screenTimeHours,
        source: source,
        meta_data: {
          app_usage: appUsageData || {},
        },
      };

      return await this.createDataPoint(dataPoint, userId);
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Get recent health metrics summary.
   */
  async getRecentHealthSummary(
    userId: number,
    days: number = 7
  ): Promise<{
    daily_metrics: HealthMetrics[];
    averages: {
      sleep_duration: number;
      sleep_quality: number;
      step_count: number;
      screen_time: number;
    };
  }> {
    try {
      const endDate = new Date();
      const startDate = new Date(endDate);
      startDate.setDate(startDate.getDate() - days);

      const dailyMetrics: HealthMetrics[] = [];
      
      // Get daily metrics for each day
      for (let i = 0; i < days; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);
        const dateStr = date.toISOString().split('T')[0];
        
        try {
          const metrics = await this.getHealthMetrics(userId, dateStr);
          dailyMetrics.push(metrics);
        } catch (error) {
          // If no data for this day, add empty metrics
          dailyMetrics.push({ date: dateStr });
        }
      }

      // Calculate averages
      const averages = {
        sleep_duration: this.calculateAverage(dailyMetrics, 'sleep_duration'),
        sleep_quality: this.calculateAverage(dailyMetrics, 'sleep_quality'),
        step_count: this.calculateAverage(dailyMetrics, 'step_count'),
        screen_time: this.calculateAverage(dailyMetrics, 'screen_time'),
      };

      return {
        daily_metrics: dailyMetrics,
        averages,
      };
    } catch (error) {
      throw this.handlePassiveDataError(error);
    }
  }

  /**
   * Helper to calculate average of a metric across multiple days.
   */
  private calculateAverage(metrics: HealthMetrics[], field: keyof HealthMetrics): number {
    const values = metrics
      .map(m => m[field])
      .filter(v => v !== undefined && v !== null) as number[];
    
    if (values.length === 0) return 0;
    return values.reduce((sum, val) => sum + val, 0) / values.length;
  }

  /**
   * Handle passive data service errors.
   */
  private handlePassiveDataError(error: any): Error {
    if (error.response?.data?.message) {
      return new Error(error.response.data.message);
    }
    if (error.message) {
      return new Error(error.message);
    }
    return new Error('Passive data operation failed');
  }
}

const passiveDataService = new PassiveDataService();
export { passiveDataService };
export default passiveDataService; 