// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'checkin_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DailyCheckinCreate _$DailyCheckinCreateFromJson(Map<String, dynamic> json) =>
    DailyCheckinCreate(
      moodRating: (json['mood_rating'] as num).toDouble(),
      moodCategory: json['mood_category'] as String?,
      keywords: (json['keywords'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList(),
      notes: json['notes'] as String?,
      location: json['location'] as String?,
      weather: json['weather'] as String?,
      energyLevel: (json['energy_level'] as num?)?.toDouble(),
      stressLevel: (json['stress_level'] as num?)?.toDouble(),
      sleepQuality: (json['sleep_quality'] as num?)?.toDouble(),
      socialInteraction: (json['social_interaction'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$DailyCheckinCreateToJson(DailyCheckinCreate instance) =>
    <String, dynamic>{
      'mood_rating': instance.moodRating,
      'mood_category': instance.moodCategory,
      'keywords': instance.keywords,
      'notes': instance.notes,
      'location': instance.location,
      'weather': instance.weather,
      'energy_level': instance.energyLevel,
      'stress_level': instance.stressLevel,
      'sleep_quality': instance.sleepQuality,
      'social_interaction': instance.socialInteraction,
    };

DailyCheckinResponse _$DailyCheckinResponseFromJson(
        Map<String, dynamic> json) =>
    DailyCheckinResponse(
      checkinId: (json['checkin_id'] as num).toInt(),
      userId: (json['user_id'] as num).toInt(),
      timestamp: DateTime.parse(json['timestamp'] as String),
      moodRating: (json['mood_rating'] as num).toDouble(),
      moodCategory: json['mood_category'] as String?,
      keywords:
          (json['keywords'] as List<dynamic>).map((e) => e as String).toList(),
      notes: json['notes'] as String?,
      location: json['location'] as String?,
      weather: json['weather'] as String?,
      energyLevel: (json['energy_level'] as num?)?.toDouble(),
      stressLevel: (json['stress_level'] as num?)?.toDouble(),
      sleepQuality: (json['sleep_quality'] as num?)?.toDouble(),
      socialInteraction: (json['social_interaction'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$DailyCheckinResponseToJson(
        DailyCheckinResponse instance) =>
    <String, dynamic>{
      'checkin_id': instance.checkinId,
      'user_id': instance.userId,
      'timestamp': instance.timestamp.toIso8601String(),
      'mood_rating': instance.moodRating,
      'mood_category': instance.moodCategory,
      'keywords': instance.keywords,
      'notes': instance.notes,
      'location': instance.location,
      'weather': instance.weather,
      'energy_level': instance.energyLevel,
      'stress_level': instance.stressLevel,
      'sleep_quality': instance.sleepQuality,
      'social_interaction': instance.socialInteraction,
    };

MoodTrend _$MoodTrendFromJson(Map<String, dynamic> json) => MoodTrend(
      date: json['date'] as String,
      moodRating: (json['mood_rating'] as num).toDouble(),
      energyLevel: (json['energy_level'] as num?)?.toDouble(),
      stressLevel: (json['stress_level'] as num?)?.toDouble(),
      sleepQuality: (json['sleep_quality'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$MoodTrendToJson(MoodTrend instance) => <String, dynamic>{
      'date': instance.date,
      'mood_rating': instance.moodRating,
      'energy_level': instance.energyLevel,
      'stress_level': instance.stressLevel,
      'sleep_quality': instance.sleepQuality,
    };

MoodAnalytics _$MoodAnalyticsFromJson(Map<String, dynamic> json) =>
    MoodAnalytics(
      period: json['period'] as String,
      averageMood: (json['average_mood'] as num).toDouble(),
      moodRange: (json['mood_range'] as Map<String, dynamic>).map(
        (k, e) => MapEntry(k, (e as num).toDouble()),
      ),
      mostCommonCategory: json['most_common_category'] as String?,
      trendDirection: json['trend_direction'] as String,
      trendData: (json['trend_data'] as List<dynamic>)
          .map((e) => MoodTrend.fromJson(e as Map<String, dynamic>))
          .toList(),
      keywordFrequency: Map<String, int>.from(json['keyword_frequency'] as Map),
      correlationInsights: json['correlation_insights'] as Map<String, dynamic>,
    );

Map<String, dynamic> _$MoodAnalyticsToJson(MoodAnalytics instance) =>
    <String, dynamic>{
      'period': instance.period,
      'average_mood': instance.averageMood,
      'mood_range': instance.moodRange,
      'most_common_category': instance.mostCommonCategory,
      'trend_direction': instance.trendDirection,
      'trend_data': instance.trendData,
      'keyword_frequency': instance.keywordFrequency,
      'correlation_insights': instance.correlationInsights,
    };

CheckinStreak _$CheckinStreakFromJson(Map<String, dynamic> json) =>
    CheckinStreak(
      currentStreak: (json['current_streak'] as num).toInt(),
      longestStreak: (json['longest_streak'] as num).toInt(),
      totalCheckins: (json['total_checkins'] as num).toInt(),
      streakStartDate: json['streak_start_date'] == null
          ? null
          : DateTime.parse(json['streak_start_date'] as String),
      daysSinceLastCheckin: (json['days_since_last_checkin'] as num).toInt(),
    );

Map<String, dynamic> _$CheckinStreakToJson(CheckinStreak instance) =>
    <String, dynamic>{
      'current_streak': instance.currentStreak,
      'longest_streak': instance.longestStreak,
      'total_checkins': instance.totalCheckins,
      'streak_start_date': instance.streakStartDate?.toIso8601String(),
      'days_since_last_checkin': instance.daysSinceLastCheckin,
    };

QuickMoodEntry _$QuickMoodEntryFromJson(Map<String, dynamic> json) =>
    QuickMoodEntry(
      moodRating: (json['mood_rating'] as num).toDouble(),
      moodCategory: json['mood_category'] as String?,
      keywords: (json['keywords'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList(),
    );

Map<String, dynamic> _$QuickMoodEntryToJson(QuickMoodEntry instance) =>
    <String, dynamic>{
      'mood_rating': instance.moodRating,
      'mood_category': instance.moodCategory,
      'keywords': instance.keywords,
    };
