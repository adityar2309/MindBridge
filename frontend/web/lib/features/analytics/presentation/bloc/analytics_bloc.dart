import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/services/api_service.dart';
import '../../../../models/checkin_models.dart';

// Events
abstract class AnalyticsEvent {}
class AnalyticsDataRequested extends AnalyticsEvent {
  final int userId;
  final String period;
  AnalyticsDataRequested(this.userId, {this.period = 'monthly'});
}
class AnalyticsRefreshRequested extends AnalyticsEvent {
  final int userId;
  final String period;
  AnalyticsRefreshRequested(this.userId, {this.period = 'monthly'});
}

// States
abstract class AnalyticsState {}
class AnalyticsInitial extends AnalyticsState {}
class AnalyticsLoading extends AnalyticsState {}
class AnalyticsLoaded extends AnalyticsState {
  final Map<String, dynamic> data;
  final MoodAnalytics? moodAnalytics;
  final List<MoodTrend> trends;
  
  AnalyticsLoaded({
    required this.data,
    this.moodAnalytics,
    required this.trends,
  });
}
class AnalyticsError extends AnalyticsState {
  final String message;
  AnalyticsError(this.message);
}

// Bloc
class AnalyticsBloc extends Bloc<AnalyticsEvent, AnalyticsState> {
  final ApiService apiService;

  AnalyticsBloc({required this.apiService}) : super(AnalyticsInitial()) {
    on<AnalyticsDataRequested>((event, emit) async {
      emit(AnalyticsLoading());
      try {
        final data = await apiService.getAnalyticsData(event.userId);
        final moodAnalytics = await apiService.getMoodAnalytics(event.userId, period: event.period);
        
        // Extract trends
        final trendsData = data['moodTrends'] as List<dynamic>;
        final trends = trendsData.map((json) => MoodTrend(
          date: json['date'],
          moodRating: (json['mood'] as num).toDouble(),
          energyLevel: json['energy'] != null ? (json['energy'] as num).toDouble() : null,
          stressLevel: json['stress'] != null ? (json['stress'] as num).toDouble() : null,
          sleepQuality: json['sleep'] != null ? (json['sleep'] as num).toDouble() : null,
        )).toList();
        
        emit(AnalyticsLoaded(
          data: data,
          moodAnalytics: moodAnalytics,
          trends: trends,
        ));
      } catch (e) {
        emit(AnalyticsError(_getErrorMessage(e.toString())));
      }
    });

    on<AnalyticsRefreshRequested>((event, emit) async {
      // Don't show loading for refresh, just update data
      try {
        final data = await apiService.getAnalyticsData(event.userId);
        final moodAnalytics = await apiService.getMoodAnalytics(event.userId, period: event.period);
        
        final trendsData = data['moodTrends'] as List<dynamic>;
        final trends = trendsData.map((json) => MoodTrend(
          date: json['date'],
          moodRating: (json['mood'] as num).toDouble(),
          energyLevel: json['energy'] != null ? (json['energy'] as num).toDouble() : null,
          stressLevel: json['stress'] != null ? (json['stress'] as num).toDouble() : null,
          sleepQuality: json['sleep'] != null ? (json['sleep'] as num).toDouble() : null,
        )).toList();
        
        emit(AnalyticsLoaded(
          data: data,
          moodAnalytics: moodAnalytics,
          trends: trends,
        ));
      } catch (e) {
        emit(AnalyticsError(_getErrorMessage(e.toString())));
      }
    });
  }
  
  // Helper method to format error messages
  String _getErrorMessage(String error) {
    if (error.contains('Exception:')) {
      return error.replaceFirst('Exception: ', '');
    }
    return error;
  }
} 