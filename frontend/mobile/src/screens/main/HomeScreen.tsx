import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Alert,
  Dimensions,
} from 'react-native';
import { LineChart, BarChart } from 'react-native-chart-kit';
import { useTheme } from '@/utils/hooks';
import { CHART_CONFIG, MOOD_CATEGORIES } from '@/constants';
import { 
  DailyCheckinResponse, 
  MoodAnalytics, 
  CheckinStreak, 
  MoodTrend 
} from '@/types/checkin';
import { HealthMetrics } from '@/services/passiveDataService';
import { checkinService, passiveDataService } from '@/services';

interface HomeScreenProps {
  navigation: any;
}

interface DashboardData {
  recentCheckins: DailyCheckinResponse[];
  analytics: MoodAnalytics;
  streak: CheckinStreak;
  todaysCheckin: DailyCheckinResponse | null;
  healthMetrics: HealthMetrics[];
}

const { width: screenWidth } = Dimensions.get('window');
const chartWidth = screenWidth - 40;

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const { isDarkMode } = useTheme();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const theme = {
    background: isDarkMode ? '#0F172A' : '#FFFFFF',
    surface: isDarkMode ? '#1E293B' : '#F8FAFC',
    card: isDarkMode ? '#334155' : '#FFFFFF',
    primary: '#6366F1',
    text: isDarkMode ? '#F1F5F9' : '#1E293B',
    textSecondary: isDarkMode ? '#94A3B8' : '#64748B',
    border: isDarkMode ? '#475569' : '#E2E8F0',
    success: '#22C55E',
    warning: '#F59E0B',
    error: '#EF4444',
  };

  const loadDashboardData = useCallback(async () => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;

      const [dashboardResponse, healthSummary] = await Promise.all([
        checkinService.getDashboardData(userId),
        passiveDataService.getRecentHealthSummary(userId, 7),
      ]);

      setDashboardData({
        ...dashboardResponse,
        healthMetrics: healthSummary.daily_metrics,
      });
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      Alert.alert(
        'Error',
        'Failed to load dashboard data. Please try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const onRefresh = useCallback(() => {
    setIsRefreshing(true);
    loadDashboardData();
  }, [loadDashboardData]);

  const navigateToCheckin = () => {
    navigation.navigate('CheckinFlow');
  };

  const navigateToAnalytics = () => {
    navigation.navigate('Analytics');
  };

  const navigateToHistory = () => {
    navigation.navigate('History');
  };

  const renderQuickStats = () => {
    if (!dashboardData) return null;

    const { streak, analytics, todaysCheckin } = dashboardData;
    
    return (
      <View style={styles.quickStatsContainer}>
        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statNumber, { color: theme.primary }]}>
            {streak.current_streak}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Day Streak
          </Text>
        </View>
        
        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statNumber, { color: CHART_CONFIG.colors.mood }]}>
            {analytics.average_mood.toFixed(1)}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Avg Mood
          </Text>
        </View>
        
        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statNumber, { color: theme.success }]}>
            {streak.total_checkins}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Total Check-ins
          </Text>
        </View>
      </View>
    );
  };

  const renderTodaysStatus = () => {
    if (!dashboardData) return null;

    const { todaysCheckin } = dashboardData;
    const hasCheckedInToday = todaysCheckin !== null;

    return (
      <View style={[styles.todaysStatusCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <View style={styles.todaysStatusHeader}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            Today's Check-in
          </Text>
          <Text style={[styles.dateText, { color: theme.textSecondary }]}>
            {new Date().toLocaleDateString('en-US', { 
              weekday: 'long', 
              month: 'short', 
              day: 'numeric' 
            })}
          </Text>
        </View>

        {hasCheckedInToday ? (
          <View style={styles.checkinComplete}>
            <View style={styles.moodDisplay}>
              <Text style={[styles.moodEmoji, { fontSize: 48 }]}>
                {MOOD_CATEGORIES.find(cat => cat.id === todaysCheckin.mood_category)?.icon || '😊'}
              </Text>
              <Text style={[styles.moodRating, { color: theme.text }]}>
                {todaysCheckin.mood_rating}/10
              </Text>
            </View>
            <Text style={[styles.moodCategory, { color: theme.textSecondary }]}>
              Feeling {todaysCheckin.mood_category || 'good'}
            </Text>
            <TouchableOpacity
              style={[styles.editButton, { borderColor: theme.primary }]}
              onPress={() => navigation.navigate('CheckinFlow', { editMode: true, checkinId: todaysCheckin.checkin_id })}
            >
              <Text style={[styles.editButtonText, { color: theme.primary }]}>
                Edit Check-in
              </Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.checkinPending}>
            <Text style={[styles.checkinMessage, { color: theme.textSecondary }]}>
              You haven't checked in today yet
            </Text>
            <TouchableOpacity
              style={[styles.checkinButton, { backgroundColor: theme.primary }]}
              onPress={navigateToCheckin}
            >
              <Text style={styles.checkinButtonText}>
                Daily Check-in
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    );
  };

  const renderMoodTrend = () => {
    if (!dashboardData?.analytics.trend_data || dashboardData.analytics.trend_data.length === 0) {
      return null;
    }

    const trendData = dashboardData.analytics.trend_data.slice(-7); // Last 7 days
    
    const chartData = {
      labels: trendData.map(trend => {
        const date = new Date(trend.date);
        return date.toLocaleDateString('en-US', { weekday: 'short' });
      }),
      datasets: [
        {
          data: trendData.map(trend => trend.mood_rating),
          color: (opacity = 1) => `rgba(99, 102, 241, ${opacity})`,
          strokeWidth: 3,
        },
      ],
    };

    const chartConfig = {
      backgroundColor: theme.card,
      backgroundGradientFrom: theme.card,
      backgroundGradientTo: theme.card,
      decimalPlaces: 1,
      color: (opacity = 1) => `rgba(99, 102, 241, ${opacity})`,
      labelColor: (opacity = 1) => isDarkMode ? `rgba(241, 245, 249, ${opacity})` : `rgba(30, 41, 59, ${opacity})`,
      style: {
        borderRadius: 16,
      },
      propsForDots: {
        r: '4',
        strokeWidth: '2',
        stroke: CHART_CONFIG.colors.mood,
      },
    };

    return (
      <View style={[styles.chartCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <View style={styles.chartHeader}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            7-Day Mood Trend
          </Text>
          <TouchableOpacity onPress={navigateToAnalytics}>
            <Text style={[styles.viewAllText, { color: theme.primary }]}>
              View All
            </Text>
          </TouchableOpacity>
        </View>
        
        <LineChart
          data={chartData}
          width={chartWidth - 40}
          height={180}
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />
      </View>
    );
  };

  const renderRecentCheckins = () => {
    if (!dashboardData?.recentCheckins || dashboardData.recentCheckins.length === 0) {
      return null;
    }

    const recentCheckins = dashboardData.recentCheckins.slice(0, 3);

    return (
      <View style={[styles.recentCheckinsCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <View style={styles.cardHeader}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>
            Recent Check-ins
          </Text>
          <TouchableOpacity onPress={navigateToHistory}>
            <Text style={[styles.viewAllText, { color: theme.primary }]}>
              View All
            </Text>
          </TouchableOpacity>
        </View>

        {recentCheckins.map((checkin) => {
          const date = new Date(checkin.timestamp);
          const categoryInfo = MOOD_CATEGORIES.find(cat => cat.id === checkin.mood_category);
          
          return (
            <View key={checkin.checkin_id} style={[styles.checkinItem, { borderBottomColor: theme.border }]}>
              <View style={styles.checkinDate}>
                <Text style={[styles.checkinDay, { color: theme.text }]}>
                  {date.toLocaleDateString('en-US', { weekday: 'short' })}
                </Text>
                <Text style={[styles.checkinDateText, { color: theme.textSecondary }]}>
                  {date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </Text>
              </View>
              
              <View style={styles.checkinMood}>
                <Text style={styles.checkinEmoji}>
                  {categoryInfo?.icon || '😊'}
                </Text>
                <Text style={[styles.checkinRating, { color: theme.text }]}>
                  {checkin.mood_rating}
                </Text>
              </View>
              
              <View style={styles.checkinDetails}>
                <Text style={[styles.checkinCategory, { color: theme.text }]}>
                  {checkin.mood_category || 'Good'}
                </Text>
                {checkin.keywords && checkin.keywords.length > 0 && (
                  <Text style={[styles.checkinKeywords, { color: theme.textSecondary }]}>
                    {checkin.keywords.slice(0, 2).join(', ')}
                  </Text>
                )}
              </View>
            </View>
          );
        })}
      </View>
    );
  };

  const renderHealthMetrics = () => {
    if (!dashboardData?.healthMetrics || dashboardData.healthMetrics.length === 0) {
      return null;
    }

    const latestMetrics = dashboardData.healthMetrics[dashboardData.healthMetrics.length - 1];

    return (
      <View style={[styles.healthCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <Text style={[styles.cardTitle, { color: theme.text }]}>
          Health Overview
        </Text>
        
        <View style={styles.healthMetricsGrid}>
          {latestMetrics.sleep_duration && (
            <View style={styles.healthMetric}>
              <Text style={[styles.healthMetricValue, { color: CHART_CONFIG.colors.sleep }]}>
                {latestMetrics.sleep_duration.toFixed(1)}h
              </Text>
              <Text style={[styles.healthMetricLabel, { color: theme.textSecondary }]}>
                Sleep
              </Text>
            </View>
          )}
          
          {latestMetrics.step_count && (
            <View style={styles.healthMetric}>
              <Text style={[styles.healthMetricValue, { color: CHART_CONFIG.colors.energy }]}>
                {(latestMetrics.step_count / 1000).toFixed(1)}k
              </Text>
              <Text style={[styles.healthMetricLabel, { color: theme.textSecondary }]}>
                Steps
              </Text>
            </View>
          )}
          
          {latestMetrics.screen_time && (
            <View style={styles.healthMetric}>
              <Text style={[styles.healthMetricValue, { color: theme.warning }]}>
                {latestMetrics.screen_time.toFixed(1)}h
              </Text>
              <Text style={[styles.healthMetricLabel, { color: theme.textSecondary }]}>
                Screen
              </Text>
            </View>
          )}
        </View>
      </View>
    );
  };

  if (isLoading) {
    return (
      <View style={[styles.container, styles.centered, { backgroundColor: theme.background }]}>
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading your dashboard...
        </Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: theme.background }]}>
      <ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        refreshControl={
          <RefreshControl
            refreshing={isRefreshing}
            onRefresh={onRefresh}
            tintColor={theme.primary}
            colors={[theme.primary]}
          />
        }
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.header}>
          <Text style={[styles.title, { color: theme.text }]}>
            Welcome back!
          </Text>
          <Text style={[styles.subtitle, { color: theme.textSecondary }]}>
            Here's how you're doing
          </Text>
        </View>

        {renderQuickStats()}
        {renderTodaysStatus()}
        {renderMoodTrend()}
        {renderRecentCheckins()}
        {renderHealthMetrics()}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    lineHeight: 24,
  },
  loadingText: {
    fontSize: 16,
  },
  quickStatsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    marginHorizontal: 4,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    textAlign: 'center',
  },
  todaysStatusCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginBottom: 20,
  },
  todaysStatusHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
  },
  dateText: {
    fontSize: 14,
  },
  checkinComplete: {
    alignItems: 'center',
  },
  moodDisplay: {
    alignItems: 'center',
    marginBottom: 8,
  },
  moodEmoji: {
    marginBottom: 8,
  },
  moodRating: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  moodCategory: {
    fontSize: 16,
    marginBottom: 16,
    textTransform: 'capitalize',
  },
  editButton: {
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  editButtonText: {
    fontSize: 14,
    fontWeight: '500',
  },
  checkinPending: {
    alignItems: 'center',
  },
  checkinMessage: {
    fontSize: 16,
    marginBottom: 16,
    textAlign: 'center',
  },
  checkinButton: {
    borderRadius: 12,
    paddingHorizontal: 24,
    paddingVertical: 12,
  },
  checkinButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  chartCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginBottom: 20,
  },
  chartHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  viewAllText: {
    fontSize: 14,
    fontWeight: '500',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  recentCheckinsCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginBottom: 20,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  checkinItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  checkinDate: {
    width: 60,
    alignItems: 'center',
  },
  checkinDay: {
    fontSize: 12,
    fontWeight: '500',
  },
  checkinDateText: {
    fontSize: 11,
  },
  checkinMood: {
    width: 60,
    alignItems: 'center',
  },
  checkinEmoji: {
    fontSize: 24,
    marginBottom: 2,
  },
  checkinRating: {
    fontSize: 12,
    fontWeight: '500',
  },
  checkinDetails: {
    flex: 1,
    marginLeft: 12,
  },
  checkinCategory: {
    fontSize: 14,
    fontWeight: '500',
    textTransform: 'capitalize',
    marginBottom: 2,
  },
  checkinKeywords: {
    fontSize: 12,
    textTransform: 'lowercase',
  },
  healthCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginBottom: 20,
  },
  healthMetricsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  healthMetric: {
    alignItems: 'center',
  },
  healthMetricValue: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  healthMetricLabel: {
    fontSize: 12,
  },
});

export default HomeScreen; 