import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';
import '../../models/user_models.dart';
import '../../models/checkin_models.dart';

class ApiService {
  static const String _baseUrl = AppConfig.baseUrl;
  String? _authToken;
  
  // Headers for API requests
  Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    if (_authToken != null) 'Authorization': 'Bearer $_authToken',
  };
  
  // Set authentication token
  void setAuthToken(String token) {
    _authToken = token;
  }
  
  // Clear authentication token
  void clearAuthToken() {
    _authToken = null;
  }
  
  // Handle API errors
  void _handleError(http.Response response) {
    final Map<String, dynamic> errorData;
    try {
      errorData = json.decode(response.body);
    } catch (e) {
      throw Exception('Network error: ${response.statusCode}');
    }
    
    final errorMessage = errorData['message'] ?? 'Unknown error occurred';
    throw Exception(errorMessage);
  }
  
  // Authentication methods
  Future<TokenResponse> login(String email, String password) async {
    final loginData = UserLogin(email: email, password: password);
    
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/login'),
      headers: _headers,
      body: json.encode(loginData.toJson()),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final tokenResponse = TokenResponse.fromJson(data);
      setAuthToken(tokenResponse.accessToken);
      return tokenResponse;
    } else {
      _handleError(response);
      throw Exception('Login failed');
    }
  }
  
  Future<TokenResponse> register(UserCreate userData) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/auth/register'),
      headers: _headers,
      body: json.encode(userData.toJson()),
    );
    
    if (response.statusCode == 201) {
      final data = json.decode(response.body);
      final tokenResponse = TokenResponse.fromJson(data);
      setAuthToken(tokenResponse.accessToken);
      return tokenResponse;
    } else {
      _handleError(response);
      throw Exception('Registration failed');
    }
  }
  
  Future<void> logout() async {
    try {
      await http.post(
        Uri.parse('$_baseUrl/auth/logout'),
        headers: _headers,
      );
    } catch (e) {
      // Ignore logout errors, clear token anyway
    } finally {
      clearAuthToken();
    }
  }
  
  // Check-in methods
  Future<DailyCheckinResponse> createCheckin(DailyCheckinCreate checkinData, int userId) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/checkins/?user_id=$userId'),
      headers: _headers,
      body: json.encode(checkinData.toJson()),
    );
    
    if (response.statusCode == 201) {
      final data = json.decode(response.body);
      return DailyCheckinResponse.fromJson(data);
    } else {
      _handleError(response);
      throw Exception('Failed to create check-in');
    }
  }
  
    Future<List<DailyCheckinResponse>> getUserCheckins(int userId, {int limit = 30, int offset = 0}) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/checkins/?user_id=$userId&limit=$limit&offset=$offset'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => DailyCheckinResponse.fromJson(json)).toList();
    } else {
      _handleError(response);
      throw Exception('Failed to fetch check-ins');
    }
  }

  Future<MoodAnalytics> getMoodAnalytics(int userId, {String period = 'monthly'}) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/checkins/analytics/?user_id=$userId&period=$period'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return MoodAnalytics.fromJson(data);
    } else {
      _handleError(response);
      throw Exception('Failed to fetch mood analytics');
    }
  }

  Future<CheckinStreak> getCheckinStreak(int userId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/checkins/streak/?user_id=$userId'),
      headers: _headers,
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return CheckinStreak.fromJson(data);
    } else {
      _handleError(response);
      throw Exception('Failed to fetch check-in streak');
    }
  }
  
  // Dashboard data - aggregated from multiple endpoints
  Future<Map<String, dynamic>> getDashboardData(int userId) async {
    try {
      // Fetch data from multiple endpoints in parallel
      final futures = await Future.wait([
        getUserCheckins(userId, limit: 5),
        getMoodAnalytics(userId, period: 'weekly'),
        getCheckinStreak(userId),
      ]);
      
      final recentCheckins = futures[0] as List<DailyCheckinResponse>;
      final analytics = futures[1] as MoodAnalytics;
      final streak = futures[2] as CheckinStreak;
      
      // Get today's mood from recent check-ins
      final DateTime today = DateTime.now();
      final todaysCheckin = recentCheckins.firstWhere(
        (checkin) => 
          checkin.timestamp.year == today.year &&
          checkin.timestamp.month == today.month &&
          checkin.timestamp.day == today.day,
        orElse: () => recentCheckins.first,
      );
      
      return {
        'todaysMood': todaysCheckin.moodRating,
        'streak': streak.currentStreak,
        'weeklyAverage': analytics.averageMood,
        'recentCheckins': recentCheckins.map((checkin) => {
          'date': checkin.timestamp.toIso8601String().split('T')[0],
          'mood': checkin.moodRating,
          'notes': checkin.notes ?? '',
          'category': checkin.moodCategory ?? '',
        }).toList(),
        'analytics': analytics,
        'streakData': streak,
      };
    } catch (e) {
      throw Exception('Failed to fetch dashboard data: $e');
    }
  }
  
  // Analytics data - processed from mood analytics
  Future<Map<String, dynamic>> getAnalyticsData(int userId) async {
    try {
      final analytics = await getMoodAnalytics(userId, period: 'monthly');
      
      return {
        'moodTrends': analytics.trendData.map((trend) => {
          'date': trend.date,
          'mood': trend.moodRating,
          'energy': trend.energyLevel,
          'stress': trend.stressLevel,
          'sleep': trend.sleepQuality,
        }).toList(),
        'averageMood': analytics.averageMood,
        'trendDirection': analytics.trendDirection,
        'mostCommonCategory': analytics.mostCommonCategory,
        'keywordFrequency': analytics.keywordFrequency,
        'correlations': analytics.correlationInsights,
        'moodRange': analytics.moodRange,
      };
    } catch (e) {
      throw Exception('Failed to fetch analytics data: $e');
    }
  }
  
  // Health check
  Future<bool> checkHealth() async {
    try {
      // Health endpoint is at /health, not /api/v1/health
      final response = await http.get(
        Uri.parse('http://localhost:8000/health'),
        headers: _headers,
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
} 