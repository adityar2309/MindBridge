import 'package:flutter/material.dart';

class AppConfig {
  static const String appName = 'MindBridge Web';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  static const String baseUrl = bool.fromEnvironment('dart.vm.product')
      ? 'https://api.mindbridge.app/v1'
      : 'http://localhost:8000/api/v1';
  
  // Breakpoints
  static const double mobileBreakpoint = 450;
  static const double tabletBreakpoint = 800;
  static const double desktopBreakpoint = 1200;
  
  // Spacing
  static const double spacingXS = 4.0;
  static const double spacingSM = 8.0;
  static const double spacingMD = 16.0;
  static const double spacingLG = 24.0;
  static const double spacingXL = 32.0;
  static const double spacingXXL = 48.0;
  
  // Border Radius
  static const double radiusSM = 4.0;
  static const double radiusMD = 8.0;
  static const double radiusLG = 12.0;
  static const double radiusXL = 16.0;
  
  // Animation Durations
  static const Duration animationFast = Duration(milliseconds: 150);
  static const Duration animationMedium = Duration(milliseconds: 300);
  static const Duration animationSlow = Duration(milliseconds: 500);
  
  // Chart Colors
  static const List<Color> chartColors = [
    Color(0xFF6366F1), // Primary
    Color(0xFF8B5CF6), // Secondary
    Color(0xFF22C55E), // Success
    Color(0xFFF59E0B), // Warning
    Color(0xFFEF4444), // Error
    Color(0xFF06B6D4), // Info
    Color(0xFFEC4899), // Pink
    Color(0xFF84CC16), // Lime
  ];
  
  // Mood Scale Colors
  static const Map<int, Color> moodColors = {
    1: Color(0xFFEF4444), // Very sad - Red
    2: Color(0xFFF97316), // Sad - Orange
    3: Color(0xFFFBBF24), // Somewhat sad - Yellow
    4: Color(0xFF84CC16), // Neutral - Light green
    5: Color(0xFF22C55E), // Okay - Green
    6: Color(0xFF06B6D4), // Good - Cyan
    7: Color(0xFF3B82F6), // Happy - Blue
    8: Color(0xFF8B5CF6), // Very happy - Purple
    9: Color(0xFFEC4899), // Excellent - Pink
    10: Color(0xFFF59E0B), // Amazing - Amber
  };
}

class AppStrings {
  // App
  static const String appName = 'MindBridge';
  static const String appTagline = 'Your Mental Health Companion';
  
  // Navigation
  static const String navDashboard = 'Dashboard';
  static const String navAnalytics = 'Analytics';
  static const String navCheckins = 'Check-ins';
  static const String navProfile = 'Profile';
  static const String navSettings = 'Settings';
  
  // Auth
  static const String signIn = 'Sign In';
  static const String signUp = 'Sign Up';
  static const String signOut = 'Sign Out';
  static const String email = 'Email';
  static const String password = 'Password';
  static const String forgotPassword = 'Forgot Password?';
  
  // Dashboard
  static const String welcomeBack = 'Welcome back';
  static const String todaysMood = "Today's Mood";
  static const String recentCheckins = 'Recent Check-ins';
  static const String moodTrends = 'Mood Trends';
  static const String quickStats = 'Quick Stats';
  
  // Analytics
  static const String moodAnalytics = 'Mood Analytics';
  static const String correlations = 'Correlations';
  static const String patterns = 'Patterns';
  static const String insights = 'AI Insights';
  
  // Common
  static const String loading = 'Loading...';
  static const String error = 'Error';
  static const String retry = 'Retry';
  static const String save = 'Save';
  static const String cancel = 'Cancel';
  static const String delete = 'Delete';
  static const String edit = 'Edit';
  static const String view = 'View';
  static const String close = 'Close';
} 