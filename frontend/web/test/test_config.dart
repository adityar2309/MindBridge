/**
 * Test Configuration for Flutter Web App
 * Provides global test setup, utilities, and configurations
 */

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

// Test Configuration
class TestConfig {
  static const String testBaseUrl = 'https://test-api.mindbridge.com';
  static const Duration testTimeout = Duration(seconds: 10);
  static const Size testDeviceSize = Size(1920, 1080);
  
  static void setup() {
    // Setup fake timers for consistent testing
    TestWidgetsFlutterBinding.ensureInitialized();
    
    // Setup shared preferences for testing
    SharedPreferences.setMockInitialValues({
      'user_token': 'test_token_123',
      'user_id': 'test_user_123',
      'theme_mode': 'light',
      'language': 'en',
      'notifications_enabled': true,
    });
    
    // Register fallback values for mocktail
    registerFallbackValue(Uri.parse('https://test.com'));
    registerFallbackValue(http.Request('GET', Uri.parse('https://test.com')));
  }
  
  static void tearDown() {
    // Clean up after tests
    reset(mockApiService);
    reset(mockAnalyticsService);
    reset(mockAuthService);
  }
}

// Mock Services
class MockApiService extends Mock implements ApiService {}
class MockAnalyticsService extends Mock {}
class MockAuthService extends Mock {}
class MockDashboardBloc extends MockBloc<DashboardEvent, DashboardState> 
    implements DashboardBloc {}
class MockAnalyticsBloc extends MockBloc<AnalyticsEvent, AnalyticsState> 
    implements AnalyticsBloc {}
class MockAuthBloc extends MockBloc<AuthEvent, AuthState> 
    implements AuthBloc {}

// Global mock instances
final mockApiService = MockApiService();
final mockAnalyticsService = MockAnalyticsService();
final mockAuthService = MockAuthService();
final mockDashboardBloc = MockDashboardBloc();
final mockAnalyticsBloc = MockAnalyticsBloc();
final mockAuthBloc = MockAuthBloc();

// Test Data Generators
class TestDataGenerator {
  static Map<String, dynamic> createMockUser({
    String? id,
    String? email,
    String? name,
  }) {
    return {
      'id': id ?? 'test_user_123',
      'email': email ?? 'test@mindbridge.com',
      'name': name ?? 'Test User',
      'avatar': 'https://example.com/avatar.jpg',
      'preferences': {
        'theme': 'light',
        'notifications': true,
        'language': 'en',
      },
      'profile': {
        'age': 28,
        'timezone': 'UTC',
        'joined_date': '2024-01-01T00:00:00Z',
      },
    };
  }
  
  static Map<String, dynamic> createMockCheckin({
    String? id,
    String? userId,
    int? mood,
    DateTime? timestamp,
  }) {
    return {
      'id': id ?? 'checkin_123',
      'user_id': userId ?? 'test_user_123',
      'timestamp': (timestamp ?? DateTime.now()).toIso8601String(),
      'mood': mood ?? 7,
      'anxiety': 3,
      'stress': 4,
      'energy': 6,
      'sleep': {
        'hours': 8,
        'quality': 7,
      },
      'notes': 'Feeling good today',
      'tags': ['work', 'exercise'],
      'activities': ['meditation', 'exercise'],
    };
  }
  
  static Map<String, dynamic> createMockAnalytics({
    String? period,
    double? averageMood,
  }) {
    return {
      'period': period ?? '7d',
      'average_mood': averageMood ?? 7.2,
      'mood_trend': 'improving',
      'total_checkins': 25,
      'top_triggers': ['work stress', 'sleep'],
      'insights': [
        'Your mood improves after exercise',
        'Consider reducing caffeine intake',
      ],
      'chart_data': List.generate(7, (index) => {
        'date': DateTime.now().subtract(Duration(days: 6 - index)).toIso8601String(),
        'mood': (5 + (index * 0.5)).clamp(1, 10),
        'anxiety': (6 - (index * 0.3)).clamp(1, 10),
        'stress': (5 + (index * 0.2)).clamp(1, 10),
        'energy': (6 + (index * 0.4)).clamp(1, 10),
      }),
    };
  }
  
  static List<Map<String, dynamic>> createMockCheckinHistory({
    int count = 10,
    String? userId,
  }) {
    return List.generate(count, (index) => createMockCheckin(
      id: 'checkin_${index + 1}',
      userId: userId,
      mood: (5 + (index % 5)).clamp(1, 10),
      timestamp: DateTime.now().subtract(Duration(days: index)),
    ));
  }
}

// Test Helpers
class TestHelpers {
  // Widget Test Helpers
  static Widget createTestableWidget({
    required Widget child,
    ThemeData? theme,
    Locale? locale,
  }) {
    return MaterialApp(
      theme: theme ?? ThemeData.light(),
      locale: locale ?? const Locale('en'),
      home: child,
    );
  }
  
  static Widget createBlocTestableWidget<B extends BlocBase<S>, S>({
    required Widget child,
    required B bloc,
    ThemeData? theme,
  }) {
    return MaterialApp(
      theme: theme ?? ThemeData.light(),
      home: BlocProvider<B>(
        create: (_) => bloc,
        child: child,
      ),
    );
  }
  
  static Widget createMultiBlocTestableWidget({
    required Widget child,
    required List<BlocProvider> providers,
    ThemeData? theme,
  }) {
    return MaterialApp(
      theme: theme ?? ThemeData.light(),
      home: MultiBlocProvider(
        providers: providers,
        child: child,
      ),
    );
  }
  
  // API Response Helpers
  static Map<String, dynamic> createSuccessResponse({
    required dynamic data,
    String? message,
  }) {
    return {
      'success': true,
      'data': data,
      'message': message ?? 'Operation successful',
      'timestamp': DateTime.now().toIso8601String(),
    };
  }
  
  static Map<String, dynamic> createErrorResponse({
    required String message,
    int? code,
    String? type,
  }) {
    return {
      'success': false,
      'error': {
        'message': message,
        'code': code ?? 500,
        'type': type ?? 'INTERNAL_ERROR',
      },
      'timestamp': DateTime.now().toIso8601String(),
    };
  }
  
  // Form Testing Helpers
  static Future<void> enterText(
    WidgetTester tester,
    String testKey,
    String text,
  ) async {
    final finder = find.byKey(Key(testKey));
    await tester.enterText(finder, text);
    await tester.pump();
  }
  
  static Future<void> tapButton(
    WidgetTester tester,
    String testKey,
  ) async {
    final finder = find.byKey(Key(testKey));
    await tester.tap(finder);
    await tester.pump();
  }
  
  static Future<void> waitForCondition(
    WidgetTester tester,
    bool Function() condition, {
    Duration timeout = const Duration(seconds: 5),
  }) async {
    final stopwatch = Stopwatch()..start();
    while (!condition() && stopwatch.elapsed < timeout) {
      await tester.pump(const Duration(milliseconds: 100));
    }
    if (!condition()) {
      throw TimeoutException('Condition not met within timeout', timeout);
    }
  }
  
  // Chart Testing Helpers
  static Future<void> verifyChartData(
    WidgetTester tester,
    String chartKey,
    List<dynamic> expectedData,
  ) async {
    final chartFinder = find.byKey(Key(chartKey));
    expect(chartFinder, findsOneWidget);
    
    // Additional chart-specific verification would go here
    // This is a placeholder for chart data verification
  }
  
  // Animation Testing Helpers
  static Future<void> pumpAndSettle(
    WidgetTester tester, {
    Duration timeout = const Duration(seconds: 10),
  }) async {
    await tester.pumpAndSettle(timeout);
  }
  
  static Future<void> runAnimation(
    WidgetTester tester,
    Duration duration,
  ) async {
    await tester.pump();
    await tester.pump(duration);
  }
}

// Golden Test Configuration
class GoldenTestConfig {
  static Future<void> setupGoldenTests() async {
    await loadAppFonts();
  }
  
  static Future<void> expectGolden(
    WidgetTester tester,
    String goldenFile, {
    Size? size,
  }) async {
    await tester.binding.setSurfaceSize(size ?? TestConfig.testDeviceSize);
    await tester.pumpAndSettle();
    await expectLater(
      find.byType(MaterialApp),
      matchesGoldenFile('goldens/$goldenFile.png'),
    );
  }
}

// Performance Test Helpers
class PerformanceTestHelpers {
  static Future<Duration> measureWidgetBuildTime(
    WidgetTester tester,
    Widget widget,
  ) async {
    final stopwatch = Stopwatch()..start();
    await tester.pumpWidget(widget);
    stopwatch.stop();
    return stopwatch.elapsed;
  }
  
  static Future<void> verifyNoFrameDrops(
    WidgetTester tester,
    VoidCallback action,
  ) async {
    final timeline = await tester.binding.traceAction(action);
    final summary = TimelineSummary.summarize(timeline);
    
    // Verify no dropped frames
    expect(summary.countFrames(), greaterThan(0));
    expect(summary.averageFrameBuildTimeMillis, lessThan(16.0)); // 60 FPS
  }
}

// Custom Matchers
Matcher hasTextStyle(TextStyle expectedStyle) {
  return _HasTextStyle(expectedStyle);
}

class _HasTextStyle extends Matcher {
  final TextStyle expectedStyle;
  
  const _HasTextStyle(this.expectedStyle);
  
  @override
  bool matches(dynamic item, Map<dynamic, dynamic> matchState) {
    if (item is! Text) return false;
    return item.style == expectedStyle;
  }
  
  @override
  Description describe(Description description) {
    return description.add('has text style $expectedStyle');
  }
}

// Exception classes for testing
class TimeoutException implements Exception {
  final String message;
  final Duration timeout;
  
  const TimeoutException(this.message, this.timeout);
  
  @override
  String toString() => 'TimeoutException: $message after ${timeout.inSeconds}s';
}

// API Service Interface (for mocking)
abstract class ApiService {
  Future<Map<String, dynamic>> get(String endpoint);
  Future<Map<String, dynamic>> post(String endpoint, Map<String, dynamic> data);
  Future<Map<String, dynamic>> put(String endpoint, Map<String, dynamic> data);
  Future<void> delete(String endpoint);
} 