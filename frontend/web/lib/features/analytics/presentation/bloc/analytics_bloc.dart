import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/services/api_service.dart';

// Events
abstract class AnalyticsEvent {}
class AnalyticsDataRequested extends AnalyticsEvent {}

// States
abstract class AnalyticsState {}
class AnalyticsInitial extends AnalyticsState {}
class AnalyticsLoading extends AnalyticsState {}
class AnalyticsLoaded extends AnalyticsState {
  final Map<String, dynamic> data;
  AnalyticsLoaded(this.data);
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
        final data = await apiService.getAnalyticsData();
        emit(AnalyticsLoaded(data));
      } catch (e) {
        emit(AnalyticsError(e.toString()));
      }
    });
  }
} 