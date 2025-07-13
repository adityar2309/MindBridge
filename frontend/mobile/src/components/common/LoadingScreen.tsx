import React from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { useTheme } from '@/utils/hooks';

interface LoadingScreenProps {
  message?: string;
}

/**
 * Loading screen component displayed during app initialization or async operations.
 */
const LoadingScreen: React.FC<LoadingScreenProps> = ({ 
  message = 'Loading...' 
}) => {
  const { isDarkMode } = useTheme();
  
  const styles = createStyles(isDarkMode);

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <ActivityIndicator 
          size="large" 
          color={isDarkMode ? '#818CF8' : '#6366F1'} 
        />
        <Text style={styles.message}>{message}</Text>
      </View>
    </View>
  );
};

const createStyles = (isDarkMode: boolean) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: isDarkMode ? '#0F172A' : '#FFFFFF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
    gap: 16,
  },
  message: {
    fontSize: 16,
    color: isDarkMode ? '#F1F5F9' : '#1E293B',
    fontWeight: '500',
  },
});

export default LoadingScreen; 