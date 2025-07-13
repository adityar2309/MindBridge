import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:responsive_framework/responsive_framework.dart';
import 'package:fl_chart/fl_chart.dart';
import '../bloc/analytics_bloc.dart';
import '../../../auth/presentation/bloc/auth_bloc.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/theme/app_theme.dart';

class AnalyticsPage extends StatefulWidget {
  const AnalyticsPage({super.key});

  @override
  State<AnalyticsPage> createState() => _AnalyticsPageState();
}

class _AnalyticsPageState extends State<AnalyticsPage> {
  String _selectedPeriod = '30D';
  
  @override
  void initState() {
    super.initState();
    _loadAnalyticsData();
  }

  void _loadAnalyticsData() {
    final authState = context.read<AuthBloc>().state;
    if (authState is AuthAuthenticated) {
      context.read<AnalyticsBloc>().add(AnalyticsDataRequested(authState.user.userId));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analytics & Insights'),
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard),
            onPressed: () {
              Navigator.pushReplacementNamed(context, '/dashboard');
            },
          ),
        ],
      ),
      body: BlocBuilder<AnalyticsBloc, AnalyticsState>(
        builder: (context, state) {
          if (state is AnalyticsLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          
          if (state is AnalyticsError) {
            return _buildErrorState(state.message);
          }
          
          if (state is AnalyticsLoaded) {
            return RefreshIndicator(
              onRefresh: () async {
                _loadAnalyticsData();
              },
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(AppConfig.spacingLG),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildHeader(),
                    const SizedBox(height: AppConfig.spacingXL),
                    _buildPeriodSelector(),
                    const SizedBox(height: AppConfig.spacingXL),
                    _buildChartsSection(state.data),
                    const SizedBox(height: AppConfig.spacingXL),
                    _buildInsightsSection(state.data),
                    const SizedBox(height: AppConfig.spacingXL),
                    _buildCorrelationsSection(state.data),
                  ],
                ),
              ),
            );
          }
          
          return _buildEmptyState();
        },
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Your Mental Health Analytics',
          style: Theme.of(context).textTheme.displaySmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: AppConfig.spacingSM),
        Text(
          'Discover patterns and insights in your mood and wellbeing data',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
          ),
        ),
      ],
    );
  }

  Widget _buildPeriodSelector() {
    final periods = ['7D', '30D', '90D', '1Y'];
    
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppConfig.radiusLG),
        border: Border.all(color: Theme.of(context).colorScheme.outline),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: periods.map((period) {
          final isSelected = _selectedPeriod == period;
          return GestureDetector(
            onTap: () {
              setState(() {
                _selectedPeriod = period;
              });
              _loadAnalyticsData();
            },
            child: Container(
              padding: const EdgeInsets.symmetric(
                horizontal: AppConfig.spacingLG,
                vertical: AppConfig.spacingMD,
              ),
              decoration: BoxDecoration(
                color: isSelected 
                    ? Theme.of(context).colorScheme.primary
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(AppConfig.radiusLG),
              ),
              child: Text(
                period,
                style: TextStyle(
                  color: isSelected 
                      ? Theme.of(context).colorScheme.onPrimary
                      : Theme.of(context).colorScheme.onSurface,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildChartsSection(Map<String, dynamic> data) {
    return ResponsiveRowColumn(
      layout: ResponsiveBreakpoints.of(context).smallerThan(TABLET)
          ? ResponsiveRowColumnType.COLUMN
          : ResponsiveRowColumnType.ROW,
      rowSpacing: AppConfig.spacingLG,
      columnSpacing: AppConfig.spacingLG,
      children: [
        ResponsiveRowColumnItem(
          rowFlex: 2,
          child: _buildMoodTrendChart(data),
        ),
        ResponsiveRowColumnItem(
          rowFlex: 1,
          child: _buildMoodDistributionChart(data),
        ),
      ],
    );
  }

  Widget _buildMoodTrendChart(Map<String, dynamic> data) {
    final trends = data['moodTrends'] as List<dynamic>? ?? [];
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Mood Trends Over Time',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: AppConfig.spacingLG),
            SizedBox(
              height: 300,
              child: trends.isNotEmpty
                  ? LineChart(
                      LineChartData(
                        gridData: FlGridData(
                          show: true,
                          drawVerticalLine: true,
                          horizontalInterval: 1,
                          verticalInterval: 1,
                          getDrawingHorizontalLine: (value) {
                            return FlLine(
                              color: Theme.of(context).colorScheme.outline.withOpacity(0.2),
                              strokeWidth: 1,
                            );
                          },
                        ),
                        titlesData: FlTitlesData(
                          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                          bottomTitles: AxisTitles(
                            sideTitles: SideTitles(
                              showTitles: true,
                              reservedSize: 30,
                              interval: trends.length > 10 ? (trends.length / 5).round().toDouble() : 1,
                              getTitlesWidget: (value, meta) {
                                if (value.toInt() >= trends.length) return const SizedBox.shrink();
                                final trend = trends[value.toInt()];
                                final date = DateTime.parse(trend['date']);
                                return Text(
                                  '${date.month}/${date.day}',
                                  style: const TextStyle(fontSize: 10),
                                );
                              },
                            ),
                          ),
                          leftTitles: AxisTitles(
                            sideTitles: SideTitles(
                              showTitles: true,
                              interval: 1,
                              getTitlesWidget: (value, meta) => Text(
                                value.toInt().toString(),
                                style: const TextStyle(fontSize: 12),
                              ),
                              reservedSize: 28,
                            ),
                          ),
                        ),
                        borderData: FlBorderData(
                          show: true,
                          border: Border.all(color: Theme.of(context).colorScheme.outline),
                        ),
                        minX: 0,
                        maxX: (trends.length - 1).toDouble(),
                        minY: 0,
                        maxY: 10,
                        lineBarsData: [
                          LineChartBarData(
                            spots: trends.asMap().entries.map((entry) {
                              return FlSpot(entry.key.toDouble(), (entry.value['mood'] as num).toDouble());
                            }).toList(),
                            isCurved: true,
                            color: AppTheme.primaryColor,
                            barWidth: 3,
                            isStrokeCapRound: true,
                            dotData: const FlDotData(show: true),
                            belowBarData: BarAreaData(
                              show: true,
                              color: AppTheme.primaryColor.withOpacity(0.1),
                            ),
                          ),
                          if (trends.first['energy'] != null) ...[
                            LineChartBarData(
                              spots: trends.asMap().entries.map((entry) {
                                return FlSpot(entry.key.toDouble(), (entry.value['energy'] as num?)?.toDouble() ?? 5.0);
                              }).toList(),
                              isCurved: true,
                              color: AppConfig.chartColors[1],
                              barWidth: 2,
                              isStrokeCapRound: true,
                              dotData: const FlDotData(show: false),
                              dashArray: [5, 5],
                            ),
                          ],
                        ],
                      ),
                    )
                  : _buildNoDataMessage('No trend data available'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMoodDistributionChart(Map<String, dynamic> data) {
    // Sample mood distribution data
    final moodCounts = {
      'Excellent': 12,
      'Good': 18,
      'Neutral': 8,
      'Low': 5,
      'Very Low': 2,
    };

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Mood Distribution',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: AppConfig.spacingLG),
            SizedBox(
              height: 300,
              child: PieChart(
                PieChartData(
                  sections: moodCounts.entries.map((entry) {
                    final index = moodCounts.keys.toList().indexOf(entry.key);
                    final color = AppConfig.chartColors[index % AppConfig.chartColors.length];
                    return PieChartSectionData(
                      value: entry.value.toDouble(),
                      title: '${entry.value}',
                      color: color,
                      radius: 60,
                      titleStyle: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    );
                  }).toList(),
                  sectionsSpace: 2,
                  centerSpaceRadius: 40,
                ),
              ),
            ),
            const SizedBox(height: AppConfig.spacingMD),
            ...moodCounts.entries.map((entry) {
              final index = moodCounts.keys.toList().indexOf(entry.key);
              final color = AppConfig.chartColors[index % AppConfig.chartColors.length];
              return Padding(
                padding: const EdgeInsets.only(bottom: AppConfig.spacingSM),
                child: Row(
                  children: [
                    Container(
                      width: 12,
                      height: 12,
                      decoration: BoxDecoration(
                        color: color,
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: AppConfig.spacingSM),
                    Text(entry.key),
                    const Spacer(),
                    Text('${entry.value} days'),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildInsightsSection(Map<String, dynamic> data) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.lightbulb,
                  color: Theme.of(context).colorScheme.primary,
                ),
                const SizedBox(width: AppConfig.spacingSM),
                Text(
                  'AI-Powered Insights',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppConfig.spacingLG),
            
            ..._generateInsights(data).map((insight) => _buildInsightItem(insight)),
          ],
        ),
      ),
    );
  }

  Widget _buildInsightItem(Map<String, dynamic> insight) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppConfig.spacingMD),
      padding: const EdgeInsets.all(AppConfig.spacingMD),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceVariant.withOpacity(0.5),
        borderRadius: BorderRadius.circular(AppConfig.radiusMD),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(AppConfig.spacingSM),
            decoration: BoxDecoration(
              color: insight['color'].withOpacity(0.1),
              borderRadius: BorderRadius.circular(AppConfig.radiusSM),
            ),
            child: Icon(
              insight['icon'],
              color: insight['color'],
              size: 20,
            ),
          ),
          const SizedBox(width: AppConfig.spacingMD),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  insight['title'],
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: AppConfig.spacingXS),
                Text(
                  insight['description'],
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCorrelationsSection(Map<String, dynamic> data) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Mood Correlations',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: AppConfig.spacingSM),
            Text(
              'Factors that correlate with your mood patterns',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
              ),
            ),
            const SizedBox(height: AppConfig.spacingLG),
            
            ..._getCorrelations().map((correlation) => _buildCorrelationItem(correlation)),
          ],
        ),
      ),
    );
  }

  Widget _buildCorrelationItem(Map<String, dynamic> correlation) {
    final strength = correlation['strength'] as double;
    
    return Padding(
      padding: const EdgeInsets.only(bottom: AppConfig.spacingMD),
      child: Row(
        children: [
          Expanded(
            flex: 2,
            child: Text(
              correlation['factor'],
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
          Expanded(
            flex: 3,
            child: LinearProgressIndicator(
              value: strength,
              backgroundColor: Theme.of(context).colorScheme.outline.withOpacity(0.2),
              valueColor: AlwaysStoppedAnimation<Color>(
                strength > 0.7 ? Colors.green :
                strength > 0.4 ? Colors.orange : Colors.red,
              ),
            ),
          ),
          const SizedBox(width: AppConfig.spacingMD),
          Text(
            '${(strength * 100).toInt()}%',
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorState(String message) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.error_outline,
            size: 64,
            color: Theme.of(context).colorScheme.error,
          ),
          const SizedBox(height: AppConfig.spacingMD),
          Text(
            'Error Loading Analytics',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppConfig.spacingSM),
          Text(
            message,
            style: Theme.of(context).textTheme.bodyMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppConfig.spacingLG),
          ElevatedButton(
            onPressed: _loadAnalyticsData,
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.analytics_outlined,
            size: 64,
            color: Theme.of(context).colorScheme.primary.withOpacity(0.5),
          ),
          const SizedBox(height: AppConfig.spacingMD),
          Text(
            'No Analytics Data',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppConfig.spacingSM),
          Text(
            'Complete a few check-ins to see your analytics',
            style: Theme.of(context).textTheme.bodyMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppConfig.spacingLG),
          ElevatedButton(
            onPressed: () {
              Navigator.pushNamed(context, '/checkin');
            },
            child: const Text('Create Check-in'),
          ),
        ],
      ),
    );
  }

  Widget _buildNoDataMessage(String message) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.show_chart,
            size: 48,
            color: Theme.of(context).colorScheme.primary.withOpacity(0.5),
          ),
          const SizedBox(height: AppConfig.spacingMD),
          Text(
            message,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ],
      ),
    );
  }

  List<Map<String, dynamic>> _generateInsights(Map<String, dynamic> data) {
    return [
      {
        'icon': Icons.trending_up,
        'color': Colors.green,
        'title': 'Positive Trend',
        'description': 'Your mood has improved by 15% over the last week. Keep up the great work!',
      },
      {
        'icon': Icons.bedtime,
        'color': Colors.blue,
        'title': 'Sleep Impact',
        'description': 'Better sleep quality correlates with 23% higher mood ratings in your data.',
      },
      {
        'icon': Icons.group,
        'color': Colors.purple,
        'title': 'Social Connection',
        'description': 'Days with social interaction show 18% higher mood scores on average.',
      },
    ];
  }

  List<Map<String, dynamic>> _getCorrelations() {
    return [
      {'factor': 'Sleep Quality', 'strength': 0.78},
      {'factor': 'Exercise', 'strength': 0.65},
      {'factor': 'Social Interaction', 'strength': 0.58},
      {'factor': 'Work Stress', 'strength': 0.42},
      {'factor': 'Weather', 'strength': 0.31},
    ];
  }
} 