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
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import { useTheme } from '@/utils/hooks';
import { CHART_CONFIG, MOOD_CATEGORIES } from '@/constants';
import { 
  MoodAnalytics, 
  MoodTrend,
  CheckinStreak 
} from '@/types/checkin';
import { checkinService } from '@/services';

interface AnalyticsScreenProps {
  navigation: any;
}

const { width: screenWidth } = Dimensions.get('window');
const chartWidth = screenWidth - 40;

const AnalyticsScreen: React.FC<AnalyticsScreenProps> = ({ navigation }) => {
  const { isDarkMode } = useTheme();
  const [selectedPeriod, setSelectedPeriod] = useState<'weekly' | 'monthly' | 'quarterly'>('monthly');
  const [analytics, setAnalytics] = useState<MoodAnalytics | null>(null);
  const [streak, setStreak] = useState<CheckinStreak | null>(null);
  const [trends, setTrends] = useState<MoodTrend[]>([]);
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

  const periodOptions = [
    { key: 'weekly', label: 'Week', days: 7 },
    { key: 'monthly', label: 'Month', days: 30 },
    { key: 'quarterly', label: '3 Months', days: 90 },
  ];

  const loadAnalyticsData = useCallback(async () => {
    try {
      // TODO: Get actual user ID from auth context
      const userId = 1;

      const periodMapping = {
        weekly: 'weekly',
        monthly: 'monthly',
        quarterly: 'monthly', // Backend doesn't have quarterly, use monthly
      };

      const [analyticsData, streakData, trendsData] = await Promise.all([
        checkinService.getMoodAnalytics(userId, periodMapping[selectedPeriod] as 'weekly' | 'monthly'),
        checkinService.getCheckinStreak(userId),
        checkinService.getMoodTrends(userId, periodOptions.find(p => p.key === selectedPeriod)?.days || 30),
      ]);

      setAnalytics(analyticsData);
      setStreak(streakData);
      setTrends(trendsData);
    } catch (error) {
      console.error('Failed to load analytics data:', error);
      Alert.alert(
        'Error',
        'Failed to load analytics data. Please try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, [selectedPeriod]);

  useEffect(() => {
    loadAnalyticsData();
  }, [loadAnalyticsData]);

  const onRefresh = useCallback(() => {
    setIsRefreshing(true);
    loadAnalyticsData();
  }, [loadAnalyticsData]);

  const renderPeriodSelector = () => (
    <View style={styles.periodSelector}>
      {periodOptions.map((option) => (
        <TouchableOpacity
          key={option.key}
          style={[
            styles.periodButton,
            {
              backgroundColor: selectedPeriod === option.key ? theme.primary : theme.surface,
              borderColor: theme.border,
            }
          ]}
          onPress={() => setSelectedPeriod(option.key as 'weekly' | 'monthly' | 'quarterly')}
        >
          <Text
            style={[
              styles.periodButtonText,
              {
                color: selectedPeriod === option.key ? '#FFFFFF' : theme.text,
              }
            ]}
          >
            {option.label}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderMoodTrendChart = () => {
    if (!trends || trends.length === 0) {
      return (
        <View style={[styles.chartCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.cardTitle, { color: theme.text }]}>Mood Trend</Text>
          <Text style={[styles.noDataText, { color: theme.textSecondary }]}>
            No data available for this period
          </Text>
        </View>
      );
    }

    const chartData = {
      labels: trends.slice(-7).map(trend => {
        const date = new Date(trend.date);
        return date.toLocaleDateString('en-US', { 
          month: 'short', 
          day: 'numeric' 
        });
      }),
      datasets: [
        {
          data: trends.slice(-7).map(trend => trend.mood_rating),
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
        r: '5',
        strokeWidth: '2',
        stroke: CHART_CONFIG.colors.mood,
      },
    };

    return (
      <View style={[styles.chartCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <Text style={[styles.cardTitle, { color: theme.text }]}>
          Mood Trend - {periodOptions.find(p => p.key === selectedPeriod)?.label}
        </Text>
        <LineChart
          data={chartData}
          width={chartWidth - 40}
          height={220}
          chartConfig={chartConfig}
          bezier
          style={styles.chart}
        />
      </View>
    );
  };

  const renderMetricsComparison = () => {
    if (!trends || trends.length === 0) return null;

    const validTrends = trends.filter(t => 
      t.energy_level !== undefined && 
      t.stress_level !== undefined && 
      t.sleep_quality !== undefined
    );

    if (validTrends.length === 0) return null;

    const avgMood = validTrends.reduce((sum, t) => sum + t.mood_rating, 0) / validTrends.length;
    const avgEnergy = validTrends.reduce((sum, t) => sum + (t.energy_level || 0), 0) / validTrends.length;
    const avgStress = validTrends.reduce((sum, t) => sum + (t.stress_level || 0), 0) / validTrends.length;
    const avgSleep = validTrends.reduce((sum, t) => sum + (t.sleep_quality || 0), 0) / validTrends.length;

    const chartData = {
      labels: ['Mood', 'Energy', 'Sleep', 'Stress'],
      datasets: [
        {
          data: [avgMood, avgEnergy, avgSleep, 10 - avgStress], // Invert stress for better visualization
        },
      ],
    };

    const chartConfig = {
      backgroundColor: theme.card,
      backgroundGradientFrom: theme.card,
      backgroundGradientTo: theme.card,
      decimalPlaces: 1,
      color: (opacity = 1) => {
        const colors = [
          CHART_CONFIG.colors.mood,
          CHART_CONFIG.colors.energy,
          CHART_CONFIG.colors.sleep,
          CHART_CONFIG.colors.stress,
        ];
        return colors[Math.floor(Math.random() * colors.length)];
      },
      labelColor: (opacity = 1) => isDarkMode ? `rgba(241, 245, 249, ${opacity})` : `rgba(30, 41, 59, ${opacity})`,
      style: {
        borderRadius: 16,
      },
    };

    return (
      <View style={[styles.chartCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <Text style={[styles.cardTitle, { color: theme.text }]}>
          Average Metrics
        </Text>
        <BarChart
          data={chartData}
          width={chartWidth - 40}
          height={220}
          chartConfig={chartConfig}
          style={styles.chart}
          showBarTops={false}
          fromZero
        />
        <View style={styles.metricsLegend}>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: CHART_CONFIG.colors.mood }]} />
            <Text style={[styles.legendText, { color: theme.textSecondary }]}>
              Mood ({avgMood.toFixed(1)})
            </Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: CHART_CONFIG.colors.energy }]} />
            <Text style={[styles.legendText, { color: theme.textSecondary }]}>
              Energy ({avgEnergy.toFixed(1)})
            </Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: CHART_CONFIG.colors.sleep }]} />
            <Text style={[styles.legendText, { color: theme.textSecondary }]}>
              Sleep ({avgSleep.toFixed(1)})
            </Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendColor, { backgroundColor: CHART_CONFIG.colors.stress }]} />
            <Text style={[styles.legendText, { color: theme.textSecondary }]}>
              Stress ({avgStress.toFixed(1)})
            </Text>
          </View>
        </View>
      </View>
    );
  };

  const renderMoodCategories = () => {
    if (!analytics?.keyword_frequency) return null;

    const topCategories = Object.entries(analytics.keyword_frequency)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5);

    if (topCategories.length === 0) return null;

    const colors = [
      CHART_CONFIG.colors.mood,
      CHART_CONFIG.colors.energy,
      CHART_CONFIG.colors.sleep,
      CHART_CONFIG.colors.stress,
      theme.warning,
    ];

    const pieData = topCategories.map(([keyword, count], index) => ({
      name: keyword,
      count: count,
      color: colors[index % colors.length],
      legendFontColor: theme.textSecondary,
      legendFontSize: 12,
    }));

    return (
      <View style={[styles.chartCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <Text style={[styles.cardTitle, { color: theme.text }]}>
          Top Mood Keywords
        </Text>
        <PieChart
          data={pieData}
          width={chartWidth - 40}
          height={200}
          chartConfig={{
            color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
          }}
          accessor="count"
          backgroundColor="transparent"
          paddingLeft="15"
          style={styles.chart}
        />
      </View>
    );
  };

  const renderInsights = () => {
    if (!analytics) return null;

    const insights = [];

    // Trend direction insight
    if (analytics.trend_direction) {
      const trendEmoji = {
        improving: '📈',
        declining: '📉',
        stable: '➡️',
      }[analytics.trend_direction] || '➡️';

      insights.push({
        icon: trendEmoji,
        title: 'Mood Trend',
        description: `Your mood is ${analytics.trend_direction} over this period`,
        color: analytics.trend_direction === 'improving' ? theme.success : 
               analytics.trend_direction === 'declining' ? theme.error : theme.warning,
      });
    }

    // Average mood insight
    if (analytics.average_mood) {
      const moodLevel = analytics.average_mood >= 7 ? 'great' : 
                       analytics.average_mood >= 5 ? 'good' : 'challenging';
      const moodEmoji = analytics.average_mood >= 7 ? '😊' : 
                        analytics.average_mood >= 5 ? '🙂' : '😔';

      insights.push({
        icon: moodEmoji,
        title: 'Average Mood',
        description: `You've been feeling ${moodLevel} with an average of ${analytics.average_mood.toFixed(1)}/10`,
        color: analytics.average_mood >= 7 ? theme.success : 
               analytics.average_mood >= 5 ? theme.warning : theme.error,
      });
    }

    // Most common category
    if (analytics.most_common_category) {
      const categoryInfo = MOOD_CATEGORIES.find(cat => cat.id === analytics.most_common_category);
      
      insights.push({
        icon: categoryInfo?.icon || '💭',
        title: 'Common Mood',
        description: `You've felt "${analytics.most_common_category}" most often`,
        color: theme.primary,
      });
    }

    // Streak insight
    if (streak) {
      insights.push({
        icon: '🔥',
        title: 'Check-in Streak',
        description: `${streak.current_streak} day current streak (longest: ${streak.longest_streak})`,
        color: streak.current_streak >= 7 ? theme.success : theme.warning,
      });
    }

    if (insights.length === 0) return null;

    return (
      <View style={[styles.insightsCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
        <Text style={[styles.cardTitle, { color: theme.text }]}>
          Insights & Patterns
        </Text>
        {insights.map((insight, index) => (
          <View key={index} style={[styles.insightItem, { borderBottomColor: theme.border }]}>
            <Text style={styles.insightIcon}>{insight.icon}</Text>
            <View style={styles.insightContent}>
              <Text style={[styles.insightTitle, { color: insight.color }]}>
                {insight.title}
              </Text>
              <Text style={[styles.insightDescription, { color: theme.textSecondary }]}>
                {insight.description}
              </Text>
            </View>
          </View>
        ))}
      </View>
    );
  };

  const renderStats = () => {
    if (!analytics || !streak) return null;

    return (
      <View style={styles.statsGrid}>
        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statValue, { color: theme.primary }]}>
            {analytics.average_mood.toFixed(1)}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Average Mood
          </Text>
        </View>

        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statValue, { color: theme.success }]}>
            {analytics.mood_range.max?.toFixed(1) || 'N/A'}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Best Day
          </Text>
        </View>

        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statValue, { color: theme.error }]}>
            {analytics.mood_range.min?.toFixed(1) || 'N/A'}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Lowest Day
          </Text>
        </View>

        <View style={[styles.statCard, { backgroundColor: theme.card, borderColor: theme.border }]}>
          <Text style={[styles.statValue, { color: theme.warning }]}>
            {streak.total_checkins}
          </Text>
          <Text style={[styles.statLabel, { color: theme.textSecondary }]}>
            Total Check-ins
          </Text>
        </View>
      </View>
    );
  };

  if (isLoading) {
    return (
      <View style={[styles.container, styles.centered, { backgroundColor: theme.background }]}>
        <Text style={[styles.loadingText, { color: theme.text }]}>
          Loading analytics...
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
            Analytics
          </Text>
          <Text style={[styles.subtitle, { color: theme.textSecondary }]}>
            Explore your mood patterns and insights
          </Text>
        </View>

        {renderPeriodSelector()}
        {renderStats()}
        {renderMoodTrendChart()}
        {renderMetricsComparison()}
        {renderMoodCategories()}
        {renderInsights()}
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
  periodSelector: {
    flexDirection: 'row',
    marginBottom: 20,
    backgroundColor: 'transparent',
    borderRadius: 12,
    padding: 4,
  },
  periodButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 2,
    borderWidth: 1,
  },
  periodButtonText: {
    fontSize: 14,
    fontWeight: '500',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  statCard: {
    width: '48%',
    alignItems: 'center',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    marginBottom: 12,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    textAlign: 'center',
  },
  chartCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginBottom: 20,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 16,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  noDataText: {
    fontSize: 14,
    textAlign: 'center',
    marginTop: 20,
  },
  metricsLegend: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    marginTop: 12,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 4,
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 6,
  },
  legendText: {
    fontSize: 12,
  },
  insightsCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginBottom: 20,
  },
  insightItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  insightIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  insightContent: {
    flex: 1,
  },
  insightTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 2,
  },
  insightDescription: {
    fontSize: 14,
    lineHeight: 20,
  },
});

export default AnalyticsScreen; 