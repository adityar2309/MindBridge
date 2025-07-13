import 'package:json_annotation/json_annotation.dart';

part 'checkin_models.g.dart';

// List of valid mood categories
const List<String> validMoodCategories = [
  'happy', 'content', 'calm', 'excited', 'optimistic',
  'sad', 'anxious', 'stressed', 'angry', 'frustrated',
  'tired', 'energetic', 'focused', 'confused', 'lonely',
  'grateful', 'hopeful', 'overwhelmed', 'peaceful', 'neutral'
];

@JsonSerializable()
class DailyCheckinCreate {
  @JsonKey(name: 'mood_rating')
  final double moodRating;
  
  @JsonKey(name: 'mood_category')
  final String? moodCategory;
  
  final List<String>? keywords;
  final String? notes;
  final String? location;
  final String? weather;
  
  @JsonKey(name: 'energy_level')
  final double? energyLevel;
  
  @JsonKey(name: 'stress_level')
  final double? stressLevel;
  
  @JsonKey(name: 'sleep_quality')
  final double? sleepQuality;
  
  @JsonKey(name: 'social_interaction')
  final double? socialInteraction;

  const DailyCheckinCreate({
    required this.moodRating,
    this.moodCategory,
    this.keywords,
    this.notes,
    this.location,
    this.weather,
    this.energyLevel,
    this.stressLevel,
    this.sleepQuality,
    this.socialInteraction,
  });

  factory DailyCheckinCreate.fromJson(Map<String, dynamic> json) =>
      _$DailyCheckinCreateFromJson(json);

  Map<String, dynamic> toJson() => _$DailyCheckinCreateToJson(this);
}

@JsonSerializable()
class DailyCheckinResponse {
  @JsonKey(name: 'checkin_id')
  final int checkinId;
  
  @JsonKey(name: 'user_id')
  final int userId;
  
  final DateTime timestamp;
  
  @JsonKey(name: 'mood_rating')
  final double moodRating;
  
  @JsonKey(name: 'mood_category')
  final String? moodCategory;
  
  final List<String> keywords;
  final String? notes;
  final String? location;
  final String? weather;
  
  @JsonKey(name: 'energy_level')
  final double? energyLevel;
  
  @JsonKey(name: 'stress_level')
  final double? stressLevel;
  
  @JsonKey(name: 'sleep_quality')
  final double? sleepQuality;
  
  @JsonKey(name: 'social_interaction')
  final double? socialInteraction;

  const DailyCheckinResponse({
    required this.checkinId,
    required this.userId,
    required this.timestamp,
    required this.moodRating,
    this.moodCategory,
    required this.keywords,
    this.notes,
    this.location,
    this.weather,
    this.energyLevel,
    this.stressLevel,
    this.sleepQuality,
    this.socialInteraction,
  });

  factory DailyCheckinResponse.fromJson(Map<String, dynamic> json) =>
      _$DailyCheckinResponseFromJson(json);

  Map<String, dynamic> toJson() => _$DailyCheckinResponseToJson(this);
}

@JsonSerializable()
class MoodTrend {
  final String date;
  
  @JsonKey(name: 'mood_rating')
  final double moodRating;
  
  @JsonKey(name: 'energy_level')
  final double? energyLevel;
  
  @JsonKey(name: 'stress_level')
  final double? stressLevel;
  
  @JsonKey(name: 'sleep_quality')
  final double? sleepQuality;

  const MoodTrend({
    required this.date,
    required this.moodRating,
    this.energyLevel,
    this.stressLevel,
    this.sleepQuality,
  });

  factory MoodTrend.fromJson(Map<String, dynamic> json) =>
      _$MoodTrendFromJson(json);

  Map<String, dynamic> toJson() => _$MoodTrendToJson(this);
}

@JsonSerializable()
class MoodAnalytics {
  final String period;
  
  @JsonKey(name: 'average_mood')
  final double averageMood;
  
  @JsonKey(name: 'mood_range')
  final Map<String, double> moodRange;
  
  @JsonKey(name: 'most_common_category')
  final String? mostCommonCategory;
  
  @JsonKey(name: 'trend_direction')
  final String trendDirection;
  
  @JsonKey(name: 'trend_data')
  final List<MoodTrend> trendData;
  
  @JsonKey(name: 'keyword_frequency')
  final Map<String, int> keywordFrequency;
  
  @JsonKey(name: 'correlation_insights')
  final Map<String, dynamic> correlationInsights;

  const MoodAnalytics({
    required this.period,
    required this.averageMood,
    required this.moodRange,
    this.mostCommonCategory,
    required this.trendDirection,
    required this.trendData,
    required this.keywordFrequency,
    required this.correlationInsights,
  });

  factory MoodAnalytics.fromJson(Map<String, dynamic> json) =>
      _$MoodAnalyticsFromJson(json);

  Map<String, dynamic> toJson() => _$MoodAnalyticsToJson(this);
}

@JsonSerializable()
class CheckinStreak {
  @JsonKey(name: 'current_streak')
  final int currentStreak;
  
  @JsonKey(name: 'longest_streak')
  final int longestStreak;
  
  @JsonKey(name: 'total_checkins')
  final int totalCheckins;
  
  @JsonKey(name: 'streak_start_date')
  final DateTime? streakStartDate;
  
  @JsonKey(name: 'days_since_last_checkin')
  final int daysSinceLastCheckin;

  const CheckinStreak({
    required this.currentStreak,
    required this.longestStreak,
    required this.totalCheckins,
    this.streakStartDate,
    required this.daysSinceLastCheckin,
  });

  factory CheckinStreak.fromJson(Map<String, dynamic> json) =>
      _$CheckinStreakFromJson(json);

  Map<String, dynamic> toJson() => _$CheckinStreakToJson(this);
}

@JsonSerializable()
class QuickMoodEntry {
  @JsonKey(name: 'mood_rating')
  final double moodRating;
  
  @JsonKey(name: 'mood_category')
  final String? moodCategory;
  
  final List<String>? keywords;

  const QuickMoodEntry({
    required this.moodRating,
    this.moodCategory,
    this.keywords,
  });

  factory QuickMoodEntry.fromJson(Map<String, dynamic> json) =>
      _$QuickMoodEntryFromJson(json);

  Map<String, dynamic> toJson() => _$QuickMoodEntryToJson(this);
} 