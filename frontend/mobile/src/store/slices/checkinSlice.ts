import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { CheckinState, CheckinCreate, DailyCheckin, MoodCategory } from '@/types';
import { checkinService } from '@/services/checkinService';
import { STORAGE_KEYS } from '@/constants';
import AsyncStorage from '@react-native-async-storage/async-storage';

const initialState: CheckinState = {
  currentCheckin: {
    overallMood: 5,
    energyLevel: 5,
    stressLevel: 5,
    sleepQuality: 5,
    socialInteraction: 5,
    moodCategories: [],
    moodKeywords: [],
    notes: '',
  },
  recentCheckins: [],
  isLoading: false,
  error: null,
  lastCheckinDate: null,
};

// Async thunks
export const createCheckin = createAsyncThunk(
  'checkin/createCheckin',
  async (checkinData: CheckinCreate, { rejectWithValue }) => {
    try {
      const checkin = await checkinService.createCheckin(checkinData);
      
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
  async (limit: number = 7, { rejectWithValue }) => {
    try {
      const checkins = await checkinService.getRecentCheckins(limit);
      return checkins;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch check-ins');
    }
  }
);

export const updateCheckin = createAsyncThunk(
  'checkin/updateCheckin',
  async ({ id, data }: { id: string; data: Partial<CheckinCreate> }, { rejectWithValue }) => {
    try {
      const updatedCheckin = await checkinService.updateCheckin(id, data);
      return updatedCheckin;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update check-in');
    }
  }
);

export const checkTodaysCheckin = createAsyncThunk(
  'checkin/checkTodaysCheckin',
  async (_, { rejectWithValue }) => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const todaysCheckin = await checkinService.getCheckinByDate(today);
      return { date: today, checkin: todaysCheckin };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to check today\'s check-in');
    }
  }
);

export const loadLastCheckinDate = createAsyncThunk(
  'checkin/loadLastCheckinDate',
  async () => {
    try {
      const lastDate = await AsyncStorage.getItem(STORAGE_KEYS.LAST_CHECKIN_DATE);
      return lastDate;
    } catch (error) {
      return null;
    }
  }
);

const checkinSlice = createSlice({
  name: 'checkin',
  initialState,
  reducers: {
    updateCurrentCheckin: (state, action: PayloadAction<Partial<CheckinCreate>>) => {
      state.currentCheckin = { ...state.currentCheckin, ...action.payload };
    },
    
    updateMoodRating: (state, action: PayloadAction<{ field: keyof CheckinCreate; value: number }>) => {
      const { field, value } = action.payload;
      if (typeof state.currentCheckin[field] === 'number') {
        (state.currentCheckin as any)[field] = value;
      }
    },
    
    addMoodCategory: (state, action: PayloadAction<MoodCategory>) => {
      const existingIndex = state.currentCheckin.moodCategories?.findIndex(
        cat => cat.category === action.payload.category
      );
      
      if (existingIndex !== undefined && existingIndex >= 0) {
        // Update existing category
        state.currentCheckin.moodCategories![existingIndex] = action.payload;
      } else {
        // Add new category
        state.currentCheckin.moodCategories = [
          ...(state.currentCheckin.moodCategories || []),
          action.payload
        ];
      }
    },
    
    removeMoodCategory: (state, action: PayloadAction<string>) => {
      state.currentCheckin.moodCategories = state.currentCheckin.moodCategories?.filter(
        cat => cat.category !== action.payload
      ) || [];
    },
    
    addMoodKeyword: (state, action: PayloadAction<string>) => {
      if (!state.currentCheckin.moodKeywords?.includes(action.payload)) {
        state.currentCheckin.moodKeywords = [
          ...(state.currentCheckin.moodKeywords || []),
          action.payload
        ];
      }
    },
    
    removeMoodKeyword: (state, action: PayloadAction<string>) => {
      state.currentCheckin.moodKeywords = state.currentCheckin.moodKeywords?.filter(
        keyword => keyword !== action.payload
      ) || [];
    },
    
    updateNotes: (state, action: PayloadAction<string>) => {
      state.currentCheckin.notes = action.payload;
    },
    
    resetCurrentCheckin: (state) => {
      state.currentCheckin = {
        overallMood: 5,
        energyLevel: 5,
        stressLevel: 5,
        sleepQuality: 5,
        socialInteraction: 5,
        moodCategories: [],
        moodKeywords: [],
        notes: '',
      };
    },
    
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create check-in
      .addCase(createCheckin.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createCheckin.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recentCheckins = [action.payload, ...state.recentCheckins];
        state.lastCheckinDate = action.payload.checkinDate;
        // Reset current check-in after successful submission
        state.currentCheckin = initialState.currentCheckin;
        state.error = null;
      })
      .addCase(createCheckin.rejected, (state, action) => {
        state.isLoading = false;
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
        state.error = null;
      })
      .addCase(fetchRecentCheckins.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Update check-in
      .addCase(updateCheckin.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateCheckin.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.recentCheckins.findIndex(c => c.id === action.payload.id);
        if (index >= 0) {
          state.recentCheckins[index] = action.payload;
        }
        state.error = null;
      })
      .addCase(updateCheckin.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Check today's check-in
      .addCase(checkTodaysCheckin.fulfilled, (state, action) => {
        if (action.payload.checkin) {
          state.lastCheckinDate = action.payload.date;
          // Update recent checkins if today's checkin exists
          const existingIndex = state.recentCheckins.findIndex(
            c => c.checkinDate === action.payload.date
          );
          if (existingIndex >= 0) {
            state.recentCheckins[existingIndex] = action.payload.checkin;
          } else {
            state.recentCheckins = [action.payload.checkin, ...state.recentCheckins];
          }
        }
      })
      
      // Load last check-in date
      .addCase(loadLastCheckinDate.fulfilled, (state, action) => {
        state.lastCheckinDate = action.payload;
      });
  },
});

export const {
  updateCurrentCheckin,
  updateMoodRating,
  addMoodCategory,
  removeMoodCategory,
  addMoodKeyword,
  removeMoodKeyword,
  updateNotes,
  resetCurrentCheckin,
  clearError,
} = checkinSlice.actions;

export default checkinSlice.reducer; 