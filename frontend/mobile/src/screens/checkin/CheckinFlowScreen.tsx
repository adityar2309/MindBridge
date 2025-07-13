import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import Slider from 'react-native-slider';
import { useTheme } from '@/utils/hooks';
import { MOOD_CATEGORIES, MOOD_KEYWORDS, SCALE_LABELS, CHART_CONFIG } from '@/constants';
import { DailyCheckinCreate, MoodCategory } from '@/types/checkin';
import { checkinService } from '@/services';

interface CheckinFlowScreenProps {
  navigation: any;
  route: any;
}

const CheckinFlowScreen: React.FC<CheckinFlowScreenProps> = ({ navigation }) => {
  const { isDarkMode } = useTheme();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Form state
  const [formData, setFormData] = useState<DailyCheckinCreate>({
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
  });

  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);

  const theme = {
    background: isDarkMode ? '#0F172A' : '#FFFFFF',
    surface: isDarkMode ? '#1E293B' : '#F8FAFC',
    primary: '#6366F1',
    text: isDarkMode ? '#F1F5F9' : '#1E293B',
    textSecondary: isDarkMode ? '#94A3B8' : '#64748B',
    border: isDarkMode ? '#334155' : '#E2E8F0',
  };

  const updateFormData = useCallback((key: keyof DailyCheckinCreate, value: any) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  }, []);

  const toggleKeyword = useCallback((keyword: string) => {
    setSelectedKeywords(prev => {
      const newKeywords = prev.includes(keyword)
        ? prev.filter(k => k !== keyword)
        : [...prev, keyword];
      updateFormData('keywords', newKeywords);
      return newKeywords;
    });
  }, [updateFormData]);

  const selectMoodCategory = useCallback((categoryId: string) => {
    updateFormData('mood_category', categoryId);
  }, [updateFormData]);

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true);
      
      // Basic validation
      if (formData.mood_rating < 1 || formData.mood_rating > 10) {
        Alert.alert('Validation Error', 'Please select a mood rating between 1 and 10');
        return;
      }

      // TODO: Get actual user ID from auth context
      const userId = 1; // Temporary hardcoded value
      
      await checkinService.createCheckin(formData, userId);
      
      Alert.alert(
        'Check-in Complete!',
        'Your daily check-in has been saved successfully.',
        [
          {
            text: 'OK',
            onPress: () => navigation.navigate('Home'),
          },
        ]
      );
    } catch (error) {
      Alert.alert(
        'Error',
        'Failed to save your check-in. Please try again.',
        [{ text: 'OK' }]
      );
      console.error('Check-in submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderMoodRating = () => (
    <View style={styles.section}>
      <Text style={[styles.sectionTitle, { color: theme.text }]}>
        How are you feeling today?
      </Text>
      <View style={styles.sliderContainer}>
        <Slider
          style={styles.slider}
          minimumValue={1}
          maximumValue={10}
          step={0.5}
          value={formData.mood_rating}
          onValueChange={(value) => updateFormData('mood_rating', value)}
          minimumTrackTintColor={CHART_CONFIG.colors.mood}
          maximumTrackTintColor={theme.border}
          thumbStyle={{ backgroundColor: CHART_CONFIG.colors.mood }}
        />
        <View style={styles.sliderLabels}>
          <Text style={[styles.sliderLabel, { color: theme.textSecondary }]}>1</Text>
          <Text style={[styles.moodValue, { color: theme.text }]}>
            {formData.mood_rating.toFixed(1)}
          </Text>
          <Text style={[styles.sliderLabel, { color: theme.textSecondary }]}>10</Text>
        </View>
      </View>
    </View>
  );

  const renderMoodCategories = () => (
    <View style={styles.section}>
      <Text style={[styles.sectionTitle, { color: theme.text }]}>
        What best describes your mood?
      </Text>
      <View style={styles.categoriesGrid}>
        {MOOD_CATEGORIES.map((category) => (
          <TouchableOpacity
            key={category.id}
            style={[
              styles.categoryButton,
              { 
                backgroundColor: formData.mood_category === category.id 
                  ? theme.primary 
                  : theme.surface,
                borderColor: theme.border,
              }
            ]}
            onPress={() => selectMoodCategory(category.id)}
          >
            <Text style={styles.categoryIcon}>{category.icon}</Text>
            <Text
              style={[
                styles.categoryLabel,
                {
                  color: formData.mood_category === category.id 
                    ? '#FFFFFF' 
                    : theme.text,
                }
              ]}
            >
              {category.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderKeywords = () => (
    <View style={styles.section}>
      <Text style={[styles.sectionTitle, { color: theme.text }]}>
        Add some keywords (optional)
      </Text>
      <View style={styles.keywordsContainer}>
        {MOOD_KEYWORDS.map((keyword) => (
          <TouchableOpacity
            key={keyword}
            style={[
              styles.keywordChip,
              {
                backgroundColor: selectedKeywords.includes(keyword)
                  ? theme.primary
                  : theme.surface,
                borderColor: theme.border,
              }
            ]}
            onPress={() => toggleKeyword(keyword)}
          >
            <Text
              style={[
                styles.keywordText,
                {
                  color: selectedKeywords.includes(keyword)
                    ? '#FFFFFF'
                    : theme.text,
                }
              ]}
            >
              {keyword}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderMetricSlider = (
    label: string,
    value: number,
    key: keyof DailyCheckinCreate,
    color: string,
    scaleLabels: readonly string[]
  ) => (
    <View style={styles.metricContainer}>
      <Text style={[styles.metricLabel, { color: theme.text }]}>{label}</Text>
      <Slider
        style={styles.slider}
        minimumValue={1}
        maximumValue={10}
        step={1}
        value={value}
        onValueChange={(val) => updateFormData(key, val)}
        minimumTrackTintColor={color}
        maximumTrackTintColor={theme.border}
        thumbStyle={{ backgroundColor: color }}
      />
      <View style={styles.metricLabels}>
        <Text style={[styles.metricValue, { color: theme.textSecondary }]}>
          {scaleLabels[Math.min(Math.floor(value / 2), scaleLabels.length - 1)]}
        </Text>
        <Text style={[styles.metricValue, { color: theme.text }]}>
          {value}/10
        </Text>
      </View>
    </View>
  );

  const renderAdditionalMetrics = () => (
    <View style={styles.section}>
      <Text style={[styles.sectionTitle, { color: theme.text }]}>
        Additional Metrics
      </Text>
      {renderMetricSlider(
        'Energy Level',
        formData.energy_level || 5,
        'energy_level',
        CHART_CONFIG.colors.energy,
        SCALE_LABELS.energy
      )}
      {renderMetricSlider(
        'Stress Level',
        formData.stress_level || 5,
        'stress_level',
        CHART_CONFIG.colors.stress,
        SCALE_LABELS.stress
      )}
      {renderMetricSlider(
        'Sleep Quality',
        formData.sleep_quality || 5,
        'sleep_quality',
        CHART_CONFIG.colors.sleep,
        SCALE_LABELS.sleep
      )}
      {renderMetricSlider(
        'Social Interaction',
        formData.social_interaction || 5,
        'social_interaction',
        theme.primary,
        SCALE_LABELS.social
      )}
    </View>
  );

  const renderNotes = () => (
    <View style={styles.section}>
      <Text style={[styles.sectionTitle, { color: theme.text }]}>
        Notes (optional)
      </Text>
      <TextInput
        style={[
          styles.notesInput,
          {
            backgroundColor: theme.surface,
            borderColor: theme.border,
            color: theme.text,
          }
        ]}
        placeholder="How was your day? Any specific thoughts or events?"
        placeholderTextColor={theme.textSecondary}
        value={formData.notes}
        onChangeText={(text) => updateFormData('notes', text)}
        multiline
        numberOfLines={4}
        textAlignVertical="top"
      />
    </View>
  );

  return (
    <KeyboardAvoidingView 
      style={[styles.container, { backgroundColor: theme.background }]}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={[styles.title, { color: theme.text }]}>
            Daily Check-in
          </Text>
          <Text style={[styles.subtitle, { color: theme.textSecondary }]}>
            Take a moment to reflect on your day
          </Text>
        </View>

        {renderMoodRating()}
        {renderMoodCategories()}
        {renderKeywords()}
        {renderAdditionalMetrics()}
        {renderNotes()}

        <TouchableOpacity
          style={[
            styles.submitButton,
            { 
              backgroundColor: theme.primary,
              opacity: isSubmitting ? 0.6 : 1,
            }
          ]}
          onPress={handleSubmit}
          disabled={isSubmitting}
        >
          <Text style={styles.submitButtonText}>
            {isSubmitting ? 'Saving...' : 'Complete Check-in'}
          </Text>
        </TouchableOpacity>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    lineHeight: 24,
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 16,
  },
  sliderContainer: {
    paddingHorizontal: 10,
  },
  slider: {
    width: '100%',
    height: 40,
  },
  sliderLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  sliderLabel: {
    fontSize: 14,
  },
  moodValue: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  categoryButton: {
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    width: 80,
    height: 80,
    borderRadius: 12,
    borderWidth: 1,
  },
  categoryIcon: {
    fontSize: 24,
    marginBottom: 4,
  },
  categoryLabel: {
    fontSize: 12,
    fontWeight: '500',
    textAlign: 'center',
  },
  keywordsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  keywordChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    borderWidth: 1,
  },
  keywordText: {
    fontSize: 14,
    fontWeight: '500',
  },
  metricContainer: {
    marginBottom: 24,
  },
  metricLabel: {
    fontSize: 16,
    fontWeight: '500',
    marginBottom: 8,
  },
  metricLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  metricValue: {
    fontSize: 14,
  },
  notesInput: {
    borderWidth: 1,
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    height: 120,
  },
  submitButton: {
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 20,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
});

export default CheckinFlowScreen; 