import React, { useEffect } from 'react';
import { StatusBar, Platform, Alert } from 'react-native';
import { Provider as ReduxProvider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { enableScreens } from 'react-native-screens';

import { store, persistor } from '@/store';
import AppNavigator from '@/navigation/AppNavigator';
import { useTheme } from '@/utils/hooks';
import ErrorBoundary from '@/components/common/ErrorBoundary';
import LoadingScreen from '@/components/common/LoadingScreen';

// Enable react-native-screens for better performance
enableScreens();

/**
 * Theme provider wrapper that applies StatusBar styling based on theme.
 */
const ThemedStatusBar: React.FC = () => {
  const { isDarkMode } = useTheme();

  useEffect(() => {
    if (Platform.OS === 'android') {
      StatusBar.setBackgroundColor(isDarkMode ? '#0F172A' : '#FFFFFF', true);
    }
    StatusBar.setBarStyle(isDarkMode ? 'light-content' : 'dark-content', true);
  }, [isDarkMode]);

  return (
    <StatusBar
      barStyle={isDarkMode ? 'light-content' : 'dark-content'}
      backgroundColor={isDarkMode ? '#0F172A' : '#FFFFFF'}
      translucent={false}
    />
  );
};

/**
 * App content component that needs Redux state.
 */
const AppContent: React.FC = () => {
  return (
    <>
      <ThemedStatusBar />
      <AppNavigator />
    </>
  );
};

/**
 * Main App component with all providers and error handling.
 */
const App: React.FC = () => {
  useEffect(() => {
    // Global error handler for unhandled promise rejections
    const handleUnhandledRejection = (event: any) => {
      console.error('Unhandled promise rejection:', event.reason);
      
      if (__DEV__) {
        Alert.alert(
          'Development Error',
          `Unhandled promise rejection: ${event.reason?.message || event.reason}`,
          [{ text: 'OK' }]
        );
      }
    };

    // Add global error listeners
    if (global.addEventListener) {
      global.addEventListener('unhandledRejection', handleUnhandledRejection);
    }

    return () => {
      if (global.removeEventListener) {
        global.removeEventListener('unhandledRejection', handleUnhandledRejection);
      }
    };
  }, []);

  return (
    <ErrorBoundary>
      <GestureHandlerRootView style={{ flex: 1 }}>
        <SafeAreaProvider>
          <ReduxProvider store={store}>
            <PersistGate 
              loading={<LoadingScreen />} 
              persistor={persistor}
            >
              <AppContent />
            </PersistGate>
          </ReduxProvider>
        </SafeAreaProvider>
      </GestureHandlerRootView>
    </ErrorBoundary>
  );
};

export default App; 