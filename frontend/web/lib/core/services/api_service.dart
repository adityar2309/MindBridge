import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';

class ApiService {
  static const String _baseUrl = AppConfig.baseUrl;
  
  // Placeholder methods for API calls
  Future<Map<String, dynamic>> login(String email, String password) async {
    // Placeholder implementation
    await Future.delayed(const Duration(seconds: 1));
    return {
      'success': true,
      'user': {'email': email, 'name': 'Test User'},
      'token': 'placeholder_token',
    };
  }
  
  Future<Map<String, dynamic>> getDashboardData() async {
    // Placeholder implementation
    await Future.delayed(const Duration(seconds: 1));
    return {
      'todaysMood': 7,
      'streak': 5,
      'weeklyAverage': 6.5,
      'recentCheckins': [
        {'date': '2024-01-15', 'mood': 8, 'notes': 'Great day!'},
        {'date': '2024-01-14', 'mood': 6, 'notes': 'Average day'},
        {'date': '2024-01-13', 'mood': 7, 'notes': 'Good mood'},
      ],
    };
  }
  
  Future<Map<String, dynamic>> getAnalyticsData() async {
    // Placeholder implementation
    await Future.delayed(const Duration(seconds: 1));
    return {
      'moodTrends': [
        {'date': '2024-01-01', 'mood': 6},
        {'date': '2024-01-02', 'mood': 7},
        {'date': '2024-01-03', 'mood': 5},
        {'date': '2024-01-04', 'mood': 8},
        {'date': '2024-01-05', 'mood': 7},
      ],
      'correlations': {
        'sleep': 0.7,
        'exercise': 0.6,
        'stress': -0.8,
      },
    };
  }
} 