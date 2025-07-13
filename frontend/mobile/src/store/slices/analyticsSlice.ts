import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { AnalyticsState, MoodAnalytics } from '@/types';
import { analyticsService } from '@/services/analyticsService';

const initialState: AnalyticsState = {
  moodAnalytics: null,
  isLoading: false,
  error: null,
  timeRange: 'month',
};

// Async thunks
export const fetchMoodAnalytics = createAsyncThunk(
  'analytics/fetchMoodAnalytics',
  async (timeRange: 'week' | 'month' | 'quarter' | 'year', { rejectWithValue }) => {
    try {
      const analytics = await analyticsService.getMoodAnalytics(timeRange);
      return { analytics, timeRange };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch mood analytics');
    }
  }
);

export const fetchStreakData = createAsyncThunk(
  'analytics/fetchStreakData',
  async (_, { rejectWithValue }) => {
    try {
      const streakData = await analyticsService.getStreakData();
      return streakData;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch streak data');
    }
  }
);

export const fetchMoodCorrelations = createAsyncThunk(
  'analytics/fetchMoodCorrelations',
  async (timeRange: 'week' | 'month' | 'quarter' | 'year', { rejectWithValue }) => {
    try {
      const correlations = await analyticsService.getMoodCorrelations(timeRange);
      return correlations;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch mood correlations');
    }
  }
);

export const exportAnalyticsData = createAsyncThunk(
  'analytics/exportAnalyticsData',
  async (format: 'csv' | 'json', { rejectWithValue }) => {
    try {
      const exportData = await analyticsService.exportData(format);
      return exportData;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to export analytics data');
    }
  }
);

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    setTimeRange: (state, action: PayloadAction<'week' | 'month' | 'quarter' | 'year'>) => {
      state.timeRange = action.payload;
    },
    
    clearError: (state) => {
      state.error = null;
    },
    
    resetAnalytics: (state) => {
      state.moodAnalytics = null;
      state.error = null;
      state.isLoading = false;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch mood analytics
      .addCase(fetchMoodAnalytics.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchMoodAnalytics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.moodAnalytics = action.payload.analytics;
        state.timeRange = action.payload.timeRange;
        state.error = null;
      })
      .addCase(fetchMoodAnalytics.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch streak data
      .addCase(fetchStreakData.fulfilled, (state, action) => {
        if (state.moodAnalytics) {
          state.moodAnalytics.streakDays = action.payload.currentStreak;
          state.moodAnalytics.totalCheckins = action.payload.totalCheckins;
        }
      })
      
      // Fetch mood correlations
      .addCase(fetchMoodCorrelations.fulfilled, (state, action) => {
        if (state.moodAnalytics) {
          state.moodAnalytics.correlations = action.payload;
        }
      })
      
      // Export analytics data
      .addCase(exportAnalyticsData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(exportAnalyticsData.fulfilled, (state) => {
        state.isLoading = false;
        state.error = null;
      })
      .addCase(exportAnalyticsData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setTimeRange, clearError, resetAnalytics } = analyticsSlice.actions;
export default analyticsSlice.reducer; 