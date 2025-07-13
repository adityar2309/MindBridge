import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { 
  DailyCheckinCreate, 
  DailyCheckinResponse, 
  MoodAnalytics, 
  CheckinStreak,
  MoodTrend
} from '@/types/checkin';
import { checkinService } from '@/services';
import { STORAGE_KEYS } from '@/constants';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface CheckinState {
  // Current form data
  currentCheckin: DailyCheckinCreate;
  
  // Data from API
  recentCheckins: DailyCheckinResponse[];
  todaysCheckin: DailyCheckinResponse | null;
  analytics: MoodAnalytics | null;
  streak: CheckinStreak | null;
  trends: MoodTrend[];
  
  // Loading states
  isLoading: boolean;
  isSubmitting: boolean;
  isRefreshing: boolean;
  
  // Error states
  error: string | null;
  
  // Cache info
  lastFetchTime: number | null;
}

const initialState: CheckinState = {
  currentCheckin: {
    mood_rating: 5,
    mood_category: undefined,
    keywords: [],
    notes: '',
    location: '',
    weather: '',
    energy_level: 5,
    stress_level: 5,
    sleep_quality: 5,
    social_interaction: 5,
  },
  recentCheckins: [],
  todaysCheckin: null,
  analytics: null,
  streak: null,
  trends: [],
  isLoading: false,
  isSubmitting: false,
  isRefreshing: false,
  error: null,
  lastFetchTime: null,
};

// Async thunks
export const createCheckin = createAsyncThunk(
  'checkin/createCheckin',
  async (checkinData: DailyCheckinCreate, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const checkin = await checkinService.createCheckin(checkinData, userId);
      
      // Store last checkin date locally
      const today = new Date().toISOString().split('T')[0];
      await AsyncStorage.setItem(STORAGE_KEYS.LAST_CHECKIN_DATE, today);
      
      return checkin;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create check-in');
    }
  }
);

export const fetchRecentCheckins = createAsyncThunk(
  'checkin/fetchRecentCheckins',
  async (options: { limit?: number; offset?: number } = {}, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const checkins = await checkinService.getUserCheckins(userId, options);
      return checkins;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch check-ins');
    }
  }
);

export const fetchTodaysCheckin = createAsyncThunk(
  'checkin/fetchTodaysCheckin',
  async (_, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const todaysCheckin = await checkinService.getTodaysCheckin(userId);
      return todaysCheckin;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch today\'s check-in');
    }
  }
);

export const updateCheckin = createAsyncThunk(
  'checkin/updateCheckin',
  async ({ 
    checkinId, 
    updateData 
  }: { 
    checkinId: number; 
    updateData: Partial<DailyCheckinCreate> 
  }, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const updatedCheckin = await checkinService.updateCheckin(checkinId, userId, updateData);
      return updatedCheckin;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update check-in');
    }
  }
);

export const fetchAnalytics = createAsyncThunk(
  'checkin/fetchAnalytics',
  async (period: 'daily' | 'weekly' | 'monthly' = 'monthly', { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const analytics = await checkinService.getMoodAnalytics(userId, period);
      return analytics;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch analytics');
    }
  }
);

export const fetchStreak = createAsyncThunk(
  'checkin/fetchStreak',
  async (_, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const streak = await checkinService.getCheckinStreak(userId);
      return streak;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch streak');
    }
  }
);

export const fetchTrends = createAsyncThunk(
  'checkin/fetchTrends',
  async (days: number = 30, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const trends = await checkinService.getMoodTrends(userId, days);
      return trends;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch trends');
    }
  }
);

export const fetchDashboardData = createAsyncThunk(
  'checkin/fetchDashboardData',
  async (_, { rejectWithValue }) => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;
      
      const dashboardData = await checkinService.getDashboardData(userId);
      return dashboardData;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch dashboard data');
    }
  }
);

const checkinSlice = createSlice({
  name: 'checkin',
  initialState,
  reducers: {
    // Update current form data
    updateCurrentCheckin: (state, action: PayloadAction<Partial<DailyCheckinCreate>>) => {
      state.currentCheckin = { ...state.currentCheckin, ...action.payload };
    },
    
    updateMoodRating: (state, action: PayloadAction<number>) => {
      state.currentCheckin.mood_rating = action.payload;
    },
    
    updateMoodCategory: (state, action: PayloadAction<string | undefined>) => {
      state.currentCheckin.mood_category = action.payload;
    },
    
    updateKeywords: (state, action: PayloadAction<string[]>) => {
      state.currentCheckin.keywords = action.payload;
    },
    
    addKeyword: (state, action: PayloadAction<string>) => {
      if (!state.currentCheckin.keywords?.includes(action.payload)) {
        state.currentCheckin.keywords = [
          ...(state.currentCheckin.keywords || []),
          action.payload
        ];
      }
    },
    
    removeKeyword: (state, action: PayloadAction<string>) => {
      state.currentCheckin.keywords = state.currentCheckin.keywords?.filter(
        keyword => keyword !== action.payload
      ) || [];
    },
    
    updateNotes: (state, action: PayloadAction<string>) => {
      state.currentCheckin.notes = action.payload;
    },
    
    updateEnergyLevel: (state, action: PayloadAction<number>) => {
      state.currentCheckin.energy_level = action.payload;
    },
    
    updateStressLevel: (state, action: PayloadAction<number>) => {
      state.currentCheckin.stress_level = action.payload;
    },
    
    updateSleepQuality: (state, action: PayloadAction<number>) => {
      state.currentCheckin.sleep_quality = action.payload;
    },
    
    updateSocialInteraction: (state, action: PayloadAction<number>) => {
      state.currentCheckin.social_interaction = action.payload;
    },
    
    updateLocation: (state, action: PayloadAction<string>) => {
      state.currentCheckin.location = action.payload;
    },
    
    updateWeather: (state, action: PayloadAction<string>) => {
      state.currentCheckin.weather = action.payload;
    },
    
    resetCurrentCheckin: (state) => {
      state.currentCheckin = initialState.currentCheckin;
    },
    
    clearError: (state) => {
      state.error = null;
    },
    
    setRefreshing: (state, action: PayloadAction<boolean>) => {
      state.isRefreshing = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create check-in
      .addCase(createCheckin.pending, (state) => {
        state.isSubmitting = true;
        state.error = null;
      })
      .addCase(createCheckin.fulfilled, (state, action) => {
        state.isSubmitting = false;
        state.recentCheckins = [action.payload, ...state.recentCheckins.slice(0, 9)]; // Keep last 10
        state.todaysCheckin = action.payload;
        state.currentCheckin = initialState.currentCheckin; // Reset form
        state.lastFetchTime = Date.now();
        state.error = null;
      })
      .addCase(createCheckin.rejected, (state, action) => {
        state.isSubmitting = false;
        state.error = action.payload as string;
      })
      
      // Fetch recent check-ins
      .addCase(fetchRecentCheckins.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRecentCheckins.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recentCheckins = action.payload;
        state.lastFetchTime = Date.now();
        state.error = null;
      })
      .addCase(fetchRecentCheckins.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch today's check-in
      .addCase(fetchTodaysCheckin.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchTodaysCheckin.fulfilled, (state, action) => {
        state.isLoading = false;
        state.todaysCheckin = action.payload;
        state.error = null;
      })
      .addCase(fetchTodaysCheckin.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Update check-in
      .addCase(updateCheckin.pending, (state) => {
        state.isSubmitting = true;
        state.error = null;
      })
      .addCase(updateCheckin.fulfilled, (state, action) => {
        state.isSubmitting = false;
        
        // Update in recent checkins
        const index = state.recentCheckins.findIndex(c => c.checkin_id === action.payload.checkin_id);
        if (index >= 0) {
          state.recentCheckins[index] = action.payload;
        }
        
        // Update today's checkin if it's the same
        if (state.todaysCheckin?.checkin_id === action.payload.checkin_id) {
          state.todaysCheckin = action.payload;
        }
        
        state.error = null;
      })
      .addCase(updateCheckin.rejected, (state, action) => {
        state.isSubmitting = false;
        state.error = action.payload as string;
      })
      
      // Fetch analytics
      .addCase(fetchAnalytics.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchAnalytics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.analytics = action.payload;
        state.error = null;
      })
      .addCase(fetchAnalytics.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch streak
      .addCase(fetchStreak.fulfilled, (state, action) => {
        state.streak = action.payload;
      })
      
      // Fetch trends
      .addCase(fetchTrends.fulfilled, (state, action) => {
        state.trends = action.payload;
      })
      
      // Fetch dashboard data
      .addCase(fetchDashboardData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recentCheckins = action.payload.recentCheckins;
        state.analytics = action.payload.analytics;
        state.streak = action.payload.streak;
        state.todaysCheckin = action.payload.todaysCheckin;
        state.lastFetchTime = Date.now();
        state.error = null;
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const {
  updateCurrentCheckin,
  updateMoodRating,
  updateMoodCategory,
  updateKeywords,
  addKeyword,
  removeKeyword,
  updateNotes,
  updateEnergyLevel,
  updateStressLevel,
  updateSleepQuality,
  updateSocialInteraction,
  updateLocation,
  updateWeather,
  resetCurrentCheckin,
  clearError,
  setRefreshing,
} = checkinSlice.actions;

export default checkinSlice.reducer;

// Selectors
export const selectCurrentCheckin = (state: { checkin: CheckinState }) => state.checkin.currentCheckin;
export const selectRecentCheckins = (state: { checkin: CheckinState }) => state.checkin.recentCheckins;
export const selectTodaysCheckin = (state: { checkin: CheckinState }) => state.checkin.todaysCheckin;
export const selectAnalytics = (state: { checkin: CheckinState }) => state.checkin.analytics;
export const selectStreak = (state: { checkin: CheckinState }) => state.checkin.streak;
export const selectTrends = (state: { checkin: CheckinState }) => state.checkin.trends;
export const selectIsLoading = (state: { checkin: CheckinState }) => state.checkin.isLoading;
export const selectIsSubmitting = (state: { checkin: CheckinState }) => state.checkin.isSubmitting;
export const selectError = (state: { checkin: CheckinState }) => state.checkin.error;
export const selectHasCheckedInToday = (state: { checkin: CheckinState }) => 
  state.checkin.todaysCheckin !== null; 