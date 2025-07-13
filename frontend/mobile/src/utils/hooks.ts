import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';
import { useEffect, useState } from 'react';
import { Appearance, ColorSchemeName } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { RootState, AppDispatch } from '@/store';
import { STORAGE_KEYS } from '@/constants';

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

/**
 * Hook to manage theme switching between light/dark/system.
 */
export const useTheme = () => {
  const [colorScheme, setColorScheme] = useState<ColorSchemeName>(Appearance.getColorScheme());
  const [themePreference, setThemePreference] = useState<'light' | 'dark' | 'system'>('system');

  useEffect(() => {
    // Load saved theme preference
    const loadThemePreference = async () => {
      try {
        const saved = await AsyncStorage.getItem(STORAGE_KEYS.THEME_PREFERENCE);
        if (saved) {
          setThemePreference(saved as 'light' | 'dark' | 'system');
        }
      } catch (error) {
        console.warn('Failed to load theme preference:', error);
      }
    };

    loadThemePreference();

    // Listen for system theme changes
    const subscription = Appearance.addChangeListener(({ colorScheme }) => {
      setColorScheme(colorScheme);
    });

    return () => subscription?.remove();
  }, []);

  const changeTheme = async (preference: 'light' | 'dark' | 'system') => {
    try {
      setThemePreference(preference);
      await AsyncStorage.setItem(STORAGE_KEYS.THEME_PREFERENCE, preference);
    } catch (error) {
      console.warn('Failed to save theme preference:', error);
    }
  };

  const isDarkMode = themePreference === 'system' 
    ? colorScheme === 'dark' 
    : themePreference === 'dark';

  return {
    isDarkMode,
    themePreference,
    changeTheme,
    systemColorScheme: colorScheme,
  };
};

/**
 * Hook to check if it's a new day and time for a check-in.
 */
export const useCheckinStatus = () => {
  const { lastCheckinDate } = useAppSelector(state => state.checkin);
  const [isNewDay, setIsNewDay] = useState(false);

  useEffect(() => {
    const checkNewDay = () => {
      const today = new Date().toISOString().split('T')[0];
      const hasCheckedInToday = lastCheckinDate === today;
      setIsNewDay(!hasCheckedInToday);
    };

    checkNewDay();
    
    // Check every minute for day changes
    const interval = setInterval(checkNewDay, 60000);
    
    return () => clearInterval(interval);
  }, [lastCheckinDate]);

  return {
    isNewDay,
    lastCheckinDate,
    canCheckinToday: isNewDay,
  };
};

/**
 * Hook to check network connectivity.
 */
export const useNetworkStatus = () => {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    let NetInfo: any;
    
    const loadNetInfo = async () => {
      try {
        NetInfo = await import('@react-native-community/netinfo');
        
        const unsubscribe = NetInfo.addEventListener((state: any) => {
          setIsConnected(state.isConnected);
        });

        // Check initial state
        NetInfo.fetch().then((state: any) => {
          setIsConnected(state.isConnected);
        });

        return unsubscribe;
      } catch (error) {
        console.warn('NetInfo not available:', error);
        // Fallback to assuming connection is available
        setIsConnected(true);
      }
    };

    const cleanup = loadNetInfo();
    
    return () => {
      cleanup?.then(unsubscribe => unsubscribe?.());
    };
  }, []);

  return { isConnected };
};

/**
 * Hook for debouncing values (useful for search inputs).
 */
export const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

/**
 * Hook to manage form validation state.
 */
export const useFormValidation = <T extends Record<string, any>>(
  initialValues: T,
  validationRules: Partial<Record<keyof T, (value: any) => string | null>>
) => {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const validateField = (field: keyof T, value: any): string | null => {
    const rule = validationRules[field];
    return rule ? rule(value) : null;
  };

  const setValue = (field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
    
    // Validate field if it has been touched
    if (touched[field]) {
      const error = validateField(field, value);
      setErrors(prev => ({ ...prev, [field]: error || undefined }));
    }
  };

  const setFieldTouched = (field: keyof T) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    
    // Validate field when touched
    const error = validateField(field, values[field]);
    setErrors(prev => ({ ...prev, [field]: error || undefined }));
  };

  const validateAll = (): boolean => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    let isValid = true;

    Object.keys(validationRules).forEach(key => {
      const field = key as keyof T;
      const error = validateField(field, values[field]);
      if (error) {
        newErrors[field] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };

  return {
    values,
    errors,
    touched,
    setValue,
    setFieldTouched,
    validateAll,
    reset,
    isValid: Object.keys(errors).length === 0,
  };
};

/**
 * Hook to format dates consistently across the app.
 */
export const useDateFormatter = () => {
  const formatDate = (date: string | Date, format: 'short' | 'long' | 'relative' = 'short'): string => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    if (format === 'relative') {
      const now = new Date();
      const diffMs = now.getTime() - dateObj.getTime();
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      
      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Yesterday';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
      return dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
    
    if (format === 'long') {
      return dateObj.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    }
    
    // Default 'short' format
    return dateObj.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    });
  };

  const formatTime = (date: string | Date): string => {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return dateObj.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  return { formatDate, formatTime };
};

/**
 * Hook to manage async operations with loading states.
 */
export const useAsyncOperation = <T>() => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<T | null>(null);

  const execute = async (asyncFunction: () => Promise<T>) => {
    try {
      setIsLoading(true);
      setError(null);
      const result = await asyncFunction();
      setData(result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'An error occurred';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const reset = () => {
    setIsLoading(false);
    setError(null);
    setData(null);
  };

  return {
    isLoading,
    error,
    data,
    execute,
    reset,
  };
}; 