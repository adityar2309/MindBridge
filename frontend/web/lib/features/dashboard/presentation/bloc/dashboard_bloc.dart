import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/services/api_service.dart';

// Events
abstract class DashboardEvent {}
class DashboardDataRequested extends DashboardEvent {}

// States
abstract class DashboardState {}
class DashboardInitial extends DashboardState {}
class DashboardLoading extends DashboardState {}
class DashboardLoaded extends DashboardState {
  final Map<String, dynamic> data;
  DashboardLoaded(this.data);
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
        final data = await apiService.getDashboardData();
        emit(DashboardLoaded(data));
      } catch (e) {
        emit(DashboardError(e.toString()));
      }
    });
  }
} 