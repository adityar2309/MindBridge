/**
 * Dashboard Widget Tests
 * Tests for Flutter web dashboard components, charts, and user interactions
 */

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:mocktail/mocktail.dart';
import '../test_config.dart';

// Mock Dashboard Widget for testing
class MockDashboardPage extends StatefulWidget {
  final DashboardBloc? bloc;
  final bool isLoading;
  final String? error;
  
  const MockDashboardPage({
    Key? key,
    this.bloc,
    this.isLoading = false,
    this.error,
  }) : super(key: key);

  @override
  State<MockDashboardPage> createState() => _MockDashboardPageState();
}

class _MockDashboardPageState extends State<MockDashboardPage> {
  @override
  Widget build(BuildContext context) {
    if (widget.error != null) {
      return Scaffold(
        key: const Key('dashboard_error'),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.error_outline,
                size: 64,
                color: Colors.red,
                key: const Key('error_icon'),
              ),
              const SizedBox(height: 16),
              Text(
                'Error: ${widget.error}',
                key: const Key('error_message'),
                style: const TextStyle(color: Colors.red),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                key: const Key('retry_button'),
                onPressed: () {
                  // Trigger retry
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }

    if (widget.isLoading) {
      return Scaffold(
        key: const Key('dashboard_loading'),
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(key: Key('loading_indicator')),
              SizedBox(height: 16),
              Text('Loading dashboard...', key: Key('loading_text')),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      key: const Key('dashboard_page'),
      appBar: AppBar(
        key: const Key('dashboard_appbar'),
        title: const Text('MindBridge Dashboard'),
        actions: [
          IconButton(
            key: const Key('notifications_button'),
            icon: const Icon(Icons.notifications),
            onPressed: () {},
          ),
          IconButton(
            key: const Key('profile_button'),
            icon: const Icon(Icons.account_circle),
            onPressed: () {},
          ),
        ],
      ),
      body: const SingleChildScrollView(
        key: Key('dashboard_scroll'),
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            WelcomeCard(),
            SizedBox(height: 16),
            QuickActionsRow(),
            SizedBox(height: 16),
            MoodChartCard(),
            SizedBox(height: 16),
            RecentCheckinsCard(),
            SizedBox(height: 16),
            InsightsCard(),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        key: const Key('quick_checkin_fab'),
        onPressed: () {},
        child: const Icon(Icons.add),
        tooltip: 'Quick Check-in',
      ),
    );
  }
}

// Mock Dashboard Components
class WelcomeCard extends StatelessWidget {
  const WelcomeCard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      key: const Key('welcome_card'),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  key: const Key('user_avatar'),
                  backgroundImage: NetworkImage('https://example.com/avatar.jpg'),
                  radius: 24,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Welcome back, Test User!',
                        key: const Key('welcome_message'),
                        style: Theme.of(context).textTheme.headlineSmall,
                      ),
                      Text(
                        'How are you feeling today?',
                        key: const Key('welcome_subtitle'),
                        style: Theme.of(context).textTheme.bodyMedium,
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            LinearProgressIndicator(
              key: const Key('mood_progress'),
              value: 0.7,
              backgroundColor: Colors.grey[300],
              valueColor: AlwaysStoppedAnimation<Color>(Colors.green),
            ),
            const SizedBox(height: 8),
            Text(
              'Weekly mood average: 7.2/10',
              key: const Key('mood_average'),
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}

class QuickActionsRow extends StatelessWidget {
  const QuickActionsRow({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      key: const Key('quick_actions'),
      children: [
        Expanded(
          child: Card(
            child: InkWell(
              key: const Key('quick_checkin_card'),
              onTap: () {},
              child: const Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Icon(Icons.favorite, size: 32, color: Colors.red),
                    SizedBox(height: 8),
                    Text('Quick Check-in'),
                  ],
                ),
              ),
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Card(
            child: InkWell(
              key: const Key('view_analytics_card'),
              onTap: () {},
              child: const Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Icon(Icons.analytics, size: 32, color: Colors.blue),
                    SizedBox(height: 8),
                    Text('View Analytics'),
                  ],
                ),
              ),
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Card(
            child: InkWell(
              key: const Key('view_history_card'),
              onTap: () {},
              child: const Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Icon(Icons.history, size: 32, color: Colors.orange),
                    SizedBox(height: 8),
                    Text('History'),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class MoodChartCard extends StatelessWidget {
  const MoodChartCard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      key: const Key('mood_chart_card'),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Mood Trend (Last 7 Days)',
              key: const Key('chart_title'),
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: LineChart(
                key: const Key('mood_line_chart'),
                LineChartData(
                  gridData: const FlGridData(show: true),
                  titlesData: const FlTitlesData(show: true),
                  borderData: FlBorderData(show: true),
                  lineBarsData: [
                    LineChartBarData(
                      spots: const [
                        FlSpot(0, 6),
                        FlSpot(1, 7),
                        FlSpot(2, 8),
                        FlSpot(3, 7),
                        FlSpot(4, 8),
                        FlSpot(5, 9),
                        FlSpot(6, 8),
                      ],
                      isCurved: true,
                      color: Colors.blue,
                      barWidth: 3,
                      dotData: const FlDotData(show: true),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Trend: Improving ↗️',
                  key: const Key('mood_trend'),
                  style: TextStyle(color: Colors.green),
                ),
                TextButton(
                  key: const Key('view_detailed_analytics'),
                  onPressed: () {},
                  child: const Text('View Details'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class RecentCheckinsCard extends StatelessWidget {
  const RecentCheckinsCard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final recentCheckins = [
      {'date': 'Today', 'mood': 8, 'notes': 'Great day!'},
      {'date': 'Yesterday', 'mood': 7, 'notes': 'Pretty good'},
      {'date': '2 days ago', 'mood': 6, 'notes': 'Average day'},
    ];

    return Card(
      key: const Key('recent_checkins_card'),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Recent Check-ins',
                  key: const Key('recent_checkins_title'),
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                TextButton(
                  key: const Key('view_all_checkins'),
                  onPressed: () {},
                  child: const Text('View All'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...recentCheckins.asMap().entries.map((entry) {
              final index = entry.key;
              final checkin = entry.value;
              return ListTile(
                key: Key('checkin_item_$index'),
                leading: CircleAvatar(
                  backgroundColor: _getMoodColor(checkin['mood'] as int),
                  child: Text(
                    '${checkin['mood']}',
                    style: const TextStyle(color: Colors.white),
                  ),
                ),
                title: Text(checkin['date'] as String),
                subtitle: Text(checkin['notes'] as String),
                trailing: Icon(Icons.chevron_right),
                onTap: () {},
              );
            }).toList(),
          ],
        ),
      ),
    );
  }

  Color _getMoodColor(int mood) {
    if (mood >= 8) return Colors.green;
    if (mood >= 6) return Colors.orange;
    return Colors.red;
  }
}

class InsightsCard extends StatelessWidget {
  const InsightsCard({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final insights = [
      'Your mood improves after exercise sessions',
      'You tend to feel better on weekends',
      'Sleep quality affects your daily mood significantly',
    ];

    return Card(
      key: const Key('insights_card'),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Personal Insights',
              key: const Key('insights_title'),
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            ...insights.asMap().entries.map((entry) {
              final index = entry.key;
              final insight = entry.value;
              return Padding(
                key: Key('insight_item_$index'),
                padding: const EdgeInsets.only(bottom: 12),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      Icons.lightbulb_outline,
                      color: Colors.amber,
                      size: 20,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(insight),
                    ),
                  ],
                ),
              );
            }).toList(),
            const SizedBox(height: 8),
            Center(
              child: TextButton.icon(
                key: const Key('generate_more_insights'),
                onPressed: () {},
                icon: const Icon(Icons.auto_awesome),
                label: const Text('Generate More Insights'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// Test Suite
void main() {
  group('Dashboard Widget Tests', () {
    setUpAll(() {
      TestConfig.setup();
    });

    tearDown(() {
      TestConfig.tearDown();
    });

    group('Dashboard Page', () => {
      testWidgets('should render dashboard page correctly', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(),
          ),
        );

        expect(find.byKey(const Key('dashboard_page')), findsOneWidget);
        expect(find.byKey(const Key('dashboard_appbar')), findsOneWidget);
        expect(find.text('MindBridge Dashboard'), findsOneWidget);
        expect(find.byKey(const Key('quick_checkin_fab')), findsOneWidget);
      });

      testWidgets('should show loading state', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(isLoading: true),
          ),
        );

        expect(find.byKey(const Key('dashboard_loading')), findsOneWidget);
        expect(find.byKey(const Key('loading_indicator')), findsOneWidget);
        expect(find.text('Loading dashboard...'), findsOneWidget);
      });

      testWidgets('should show error state', (WidgetTester tester) async {
        const errorMessage = 'Failed to load dashboard';
        
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(error: errorMessage),
          ),
        );

        expect(find.byKey(const Key('dashboard_error')), findsOneWidget);
        expect(find.byKey(const Key('error_icon')), findsOneWidget);
        expect(find.text('Error: $errorMessage'), findsOneWidget);
        expect(find.byKey(const Key('retry_button')), findsOneWidget);
      });

      testWidgets('should handle app bar actions', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(),
          ),
        );

        // Test notifications button
        final notificationsButton = find.byKey(const Key('notifications_button'));
        expect(notificationsButton, findsOneWidget);
        await tester.tap(notificationsButton);
        await tester.pump();

        // Test profile button
        final profileButton = find.byKey(const Key('profile_button'));
        expect(profileButton, findsOneWidget);
        await tester.tap(profileButton);
        await tester.pump();
      });
    });

    group('Welcome Card', () => {
      testWidgets('should display user information', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const WelcomeCard(),
          ),
        );

        expect(find.byKey(const Key('welcome_card')), findsOneWidget);
        expect(find.byKey(const Key('user_avatar')), findsOneWidget);
        expect(find.text('Welcome back, Test User!'), findsOneWidget);
        expect(find.text('How are you feeling today?'), findsOneWidget);
        expect(find.byKey(const Key('mood_progress')), findsOneWidget);
        expect(find.text('Weekly mood average: 7.2/10'), findsOneWidget);
      });

      testWidgets('should show mood progress correctly', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const WelcomeCard(),
          ),
        );

        final progressIndicator = tester.widget<LinearProgressIndicator>(
          find.byKey(const Key('mood_progress'))
        );
        expect(progressIndicator.value, equals(0.7));
        expect(progressIndicator.valueColor?.value, equals(Colors.green));
      });
    });

    group('Quick Actions', () => {
      testWidgets('should render all quick action cards', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const QuickActionsRow(),
          ),
        );

        expect(find.byKey(const Key('quick_actions')), findsOneWidget);
        expect(find.byKey(const Key('quick_checkin_card')), findsOneWidget);
        expect(find.byKey(const Key('view_analytics_card')), findsOneWidget);
        expect(find.byKey(const Key('view_history_card')), findsOneWidget);
        
        expect(find.text('Quick Check-in'), findsOneWidget);
        expect(find.text('View Analytics'), findsOneWidget);
        expect(find.text('History'), findsOneWidget);
      });

      testWidgets('should handle card taps', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const QuickActionsRow(),
          ),
        );

        await tester.tap(find.byKey(const Key('quick_checkin_card')));
        await tester.pump();

        await tester.tap(find.byKey(const Key('view_analytics_card')));
        await tester.pump();

        await tester.tap(find.byKey(const Key('view_history_card')));
        await tester.pump();

        // Verify no exceptions were thrown
      });
    });

    group('Mood Chart', () => {
      testWidgets('should display mood chart with data', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MoodChartCard(),
          ),
        );

        expect(find.byKey(const Key('mood_chart_card')), findsOneWidget);
        expect(find.text('Mood Trend (Last 7 Days)'), findsOneWidget);
        expect(find.byKey(const Key('mood_line_chart')), findsOneWidget);
        expect(find.text('Trend: Improving ↗️'), findsOneWidget);
        expect(find.byKey(const Key('view_detailed_analytics')), findsOneWidget);
      });

      testWidgets('should handle view details button', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MoodChartCard(),
          ),
        );

        final viewDetailsButton = find.byKey(const Key('view_detailed_analytics'));
        await tester.tap(viewDetailsButton);
        await tester.pump();
      });
    });

    group('Recent Check-ins', () => {
      testWidgets('should display recent check-ins list', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const RecentCheckinsCard(),
          ),
        );

        expect(find.byKey(const Key('recent_checkins_card')), findsOneWidget);
        expect(find.text('Recent Check-ins'), findsOneWidget);
        expect(find.byKey(const Key('view_all_checkins')), findsOneWidget);
        
        // Check individual checkin items
        expect(find.byKey(const Key('checkin_item_0')), findsOneWidget);
        expect(find.byKey(const Key('checkin_item_1')), findsOneWidget);
        expect(find.byKey(const Key('checkin_item_2')), findsOneWidget);
        
        expect(find.text('Today'), findsOneWidget);
        expect(find.text('Yesterday'), findsOneWidget);
        expect(find.text('2 days ago'), findsOneWidget);
      });

      testWidgets('should handle checkin item taps', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const RecentCheckinsCard(),
          ),
        );

        await tester.tap(find.byKey(const Key('checkin_item_0')));
        await tester.pump();
      });
    });

    group('Insights Card', () => {
      testWidgets('should display personal insights', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const InsightsCard(),
          ),
        );

        expect(find.byKey(const Key('insights_card')), findsOneWidget);
        expect(find.text('Personal Insights'), findsOneWidget);
        
        // Check insight items
        expect(find.byKey(const Key('insight_item_0')), findsOneWidget);
        expect(find.byKey(const Key('insight_item_1')), findsOneWidget);
        expect(find.byKey(const Key('insight_item_2')), findsOneWidget);
        
        expect(find.text('Your mood improves after exercise sessions'), findsOneWidget);
        expect(find.byKey(const Key('generate_more_insights')), findsOneWidget);
      });

      testWidgets('should handle generate insights button', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const InsightsCard(),
          ),
        );

        final generateButton = find.byKey(const Key('generate_more_insights'));
        await tester.tap(generateButton);
        await tester.pump();
      });
    });

    group('Scrolling and Layout', () => {
      testWidgets('should be scrollable', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(),
          ),
        );

        final scrollView = find.byKey(const Key('dashboard_scroll'));
        expect(scrollView, findsOneWidget);
        
        // Test scrolling
        await tester.fling(scrollView, const Offset(0, -500), 1000);
        await tester.pumpAndSettle();
      });

      testWidgets('should handle small screen sizes', (WidgetTester tester) async {
        tester.binding.window.physicalSizeTestValue = const Size(800, 600);
        tester.binding.window.devicePixelRatioTestValue = 1.0;
        
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(),
          ),
        );

        expect(find.byKey(const Key('dashboard_page')), findsOneWidget);
        
        tester.binding.window.clearPhysicalSizeTestValue();
        tester.binding.window.clearDevicePixelRatioTestValue();
      });
    });

    group('Performance', () => {
      testWidgets('should render within performance limits', (WidgetTester tester) async {
        final buildTime = await PerformanceTestHelpers.measureWidgetBuildTime(
          tester,
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(),
          ),
        );

        // Should build within 100ms
        expect(buildTime.inMilliseconds, lessThan(100));
      });

      testWidgets('should handle rapid interactions without lag', (WidgetTester tester) async {
        await tester.pumpWidget(
          TestHelpers.createTestableWidget(
            child: const MockDashboardPage(),
          ),
        );

        // Rapidly tap different elements
        for (int i = 0; i < 10; i++) {
          await tester.tap(find.byKey(const Key('quick_checkin_card')));
          await tester.pump(const Duration(milliseconds: 10));
        }

        // Should not cause any performance issues
      });
    });
  });
}

// Mock BLoC states and events for compilation
abstract class DashboardEvent {}
abstract class DashboardState {}
abstract class DashboardBloc {}
abstract class AnalyticsEvent {}
abstract class AnalyticsState {}
abstract class AnalyticsBloc {}
abstract class AuthEvent {}
abstract class AuthState {}
abstract class AuthBloc {} 