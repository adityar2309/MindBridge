import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '@/utils/hooks';

const HomeScreen: React.FC = () => {
  const { isDarkMode } = useTheme();

  return (
    <View style={[styles.container, { backgroundColor: isDarkMode ? '#0F172A' : '#FFFFFF' }]}>
      <Text style={[styles.title, { color: isDarkMode ? '#F1F5F9' : '#1E293B' }]}>
        Home Screen
      </Text>
      <Text style={[styles.subtitle, { color: isDarkMode ? '#94A3B8' : '#64748B' }]}>
        Dashboard and mood overview will be implemented here
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
  },
});

export default HomeScreen; 