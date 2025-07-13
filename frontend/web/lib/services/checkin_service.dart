import '../core/services/api_service.dart';
import '../models/checkin_models.dart';

class CheckinService {
  final ApiService _apiService;

  CheckinService(this._apiService);

  /// Create a new daily check-in
  Future<DailyCheckinResponse> createCheckin(DailyCheckinCreate checkinData, int userId) async {
    return await _apiService.createCheckin(checkinData, userId);
  }

  /// Get user's recent check-ins
  Future<List<DailyCheckinResponse>> getRecentCheckins(int userId, {int limit = 5}) async {
    return await _apiService.getUserCheckins(userId, limit: limit);
  }

  /// Get mood analytics
  Future<MoodAnalytics> getMoodAnalytics(int userId, {String period = 'monthly'}) async {
    return await _apiService.getMoodAnalytics(userId, period: period);
  }

  /// Get check-in streak
  Future<CheckinStreak> getCheckinStreak(int userId) async {
    return await _apiService.getCheckinStreak(userId);
  }

  /// Create a quick mood entry
  Future<DailyCheckinResponse> createQuickMood(double moodRating, int userId, {String? category}) async {
    final checkinData = DailyCheckinCreate(
      moodRating: moodRating,
      moodCategory: category,
    );
    return await createCheckin(checkinData, userId);
  }

  /// Check if user has checked in today
  Future<bool> hasCheckedInToday(int userId) async {
    try {
      final recentCheckins = await getRecentCheckins(userId, limit: 1);
      if (recentCheckins.isEmpty) return false;
      
      final today = DateTime.now();
      final latestCheckin = recentCheckins.first;
      
      return latestCheckin.timestamp.year == today.year &&
             latestCheckin.timestamp.month == today.month &&
             latestCheckin.timestamp.day == today.day;
    } catch (e) {
      return false;
    }
  }

  /// Get today's check-in if it exists
  Future<DailyCheckinResponse?> getTodaysCheckin(int userId) async {
    try {
      final recentCheckins = await getRecentCheckins(userId, limit: 5);
      final today = DateTime.now();
      
      for (final checkin in recentCheckins) {
        if (checkin.timestamp.year == today.year &&
            checkin.timestamp.month == today.month &&
            checkin.timestamp.day == today.day) {
          return checkin;
        }
      }
      return null;
    } catch (e) {
      return null;
    }
  }
} 