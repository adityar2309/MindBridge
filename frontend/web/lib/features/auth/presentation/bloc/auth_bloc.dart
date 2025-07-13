import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/services/api_service.dart';

// Events
abstract class AuthEvent {}
class AuthCheckRequested extends AuthEvent {}
class AuthLoginRequested extends AuthEvent {
  final String email;
  final String password;
  AuthLoginRequested(this.email, this.password);
}
class AuthLogoutRequested extends AuthEvent {}

// States
abstract class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final Map<String, dynamic> user;
  AuthAuthenticated(this.user);
}
class AuthUnauthenticated extends AuthState {}
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

// Bloc
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final ApiService apiService;

  AuthBloc({required this.apiService}) : super(AuthInitial()) {
    on<AuthCheckRequested>((event, emit) async {
      emit(AuthLoading());
      // Placeholder: assume authenticated for demo
      await Future.delayed(const Duration(milliseconds: 500));
      emit(AuthAuthenticated({'email': 'demo@mindbridge.app', 'name': 'Demo User'}));
    });

    on<AuthLoginRequested>((event, emit) async {
      emit(AuthLoading());
      try {
        final result = await apiService.login(event.email, event.password);
        if (result['success']) {
          emit(AuthAuthenticated(result['user']));
        } else {
          emit(AuthError('Login failed'));
        }
      } catch (e) {
        emit(AuthError(e.toString()));
      }
    });

    on<AuthLogoutRequested>((event, emit) async {
      emit(AuthUnauthenticated());
    });
  }
} 