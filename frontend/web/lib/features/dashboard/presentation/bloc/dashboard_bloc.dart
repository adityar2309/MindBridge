import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/services/api_service.dart';
import '../../../../models/checkin_models.dart';

// Events
abstract class DashboardEvent {}
class DashboardDataRequested extends DashboardEvent {
  final int userId;
  DashboardDataRequested(this.userId);
}
class DashboardRefreshRequested extends DashboardEvent {
  final int userId;
  DashboardRefreshRequested(this.userId);
}

// States
abstract class DashboardState {}
class DashboardInitial extends DashboardState {}
class DashboardLoading extends DashboardState {}
class DashboardLoaded extends DashboardState {
  final Map<String, dynamic> data;
  final List<DailyCheckinResponse> recentCheckins;
  final MoodAnalytics? analytics;
  final CheckinStreak? streakData;
  
  DashboardLoaded({
    required this.data,
    required this.recentCheckins,
    this.analytics,
    this.streakData,
  });
}
class DashboardError extends DashboardState {
  final String message;
  DashboardError(this.message);
}

// Bloc
class DashboardBloc extends Bloc<DashboardEvent, DashboardState> {
  final ApiService apiService;

  DashboardBloc({required this.apiService}) : super(DashboardInitial()) {
    on<DashboardDataRequested>((event, emit) async {
      emit(DashboardLoading());
      try {
        final data = await apiService.getDashboardData(event.userId);
        
        // Extract structured data
        final recentCheckinsData = data['recentCheckins'] as List<dynamic>;
        final recentCheckins = recentCheckinsData.map((json) {
          // Convert the simplified format back to DailyCheckinResponse format
          return DailyCheckinResponse(
            checkinId: 0, // Placeholder ID
            userId: event.userId,
            timestamp: DateTime.parse(json['date']),
            moodRating: (json['mood'] as num).toDouble(),
            moodCategory: json['category'].toString().isEmpty ? null : json['category'],
            keywords: [],
            notes: json['notes'].toString().isEmpty ? null : json['notes'],
          );
        }).toList();
        
        emit(DashboardLoaded(
          data: data,
          recentCheckins: recentCheckins,
          analytics: data['analytics'] as MoodAnalytics?,
          streakData: data['streakData'] as CheckinStreak?,
        ));
      } catch (e) {
        emit(DashboardError(_getErrorMessage(e.toString())));
      }
    });

    on<DashboardRefreshRequested>((event, emit) async {
      // Don't show loading for refresh, just update data
      try {
        final data = await apiService.getDashboardData(event.userId);
        
        final recentCheckinsData = data['recentCheckins'] as List<dynamic>;
        final recentCheckins = recentCheckinsData.map((json) {
          return DailyCheckinResponse(
            checkinId: 0,
            userId: event.userId,
            timestamp: DateTime.parse(json['date']),
            moodRating: (json['mood'] as num).toDouble(),
            moodCategory: json['category'].toString().isEmpty ? null : json['category'],
            keywords: [],
            notes: json['notes'].toString().isEmpty ? null : json['notes'],
          );
        }).toList();
        
        emit(DashboardLoaded(
          data: data,
          recentCheckins: recentCheckins,
          analytics: data['analytics'] as MoodAnalytics?,
          streakData: data['streakData'] as CheckinStreak?,
        ));
      } catch (e) {
        // For refresh errors, keep current state but could show a snackbar
        emit(DashboardError(_getErrorMessage(e.toString())));
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