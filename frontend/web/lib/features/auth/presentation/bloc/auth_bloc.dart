import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../../core/services/api_service.dart';
import '../../../../models/user_models.dart';

// Events
abstract class AuthEvent {}
class AuthCheckRequested extends AuthEvent {}
class AuthLoginRequested extends AuthEvent {
  final String email;
  final String password;
  AuthLoginRequested(this.email, this.password);
}
class AuthRegisterRequested extends AuthEvent {
  final UserCreate userData;
  AuthRegisterRequested(this.userData);
}
class AuthLogoutRequested extends AuthEvent {}

// States
abstract class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final UserResponse user;
  final String accessToken;
  AuthAuthenticated(this.user, this.accessToken);
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
      try {
        // Check for stored authentication token
        final prefs = await SharedPreferences.getInstance();
        final storedToken = prefs.getString('auth_token');
        
        if (storedToken != null) {
          apiService.setAuthToken(storedToken);
          
          // Verify token is still valid by checking health endpoint
          final isHealthy = await apiService.checkHealth();
          if (isHealthy) {
            // For now, create a demo user since we don't have a "me" endpoint
            // In a real app, you'd fetch the current user profile
            final demoUser = UserResponse(
              userId: 1,
              name: 'Demo User',
              email: 'demo@mindbridge.app',
              registrationDate: DateTime.now(),
              isActive: true,
              settings: UserSettings.defaultSettings.toJson(),
              timezone: 'UTC',
              language: 'en',
            );
            emit(AuthAuthenticated(demoUser, storedToken));
            return;
          }
        }
        
        // No valid token found
        emit(AuthUnauthenticated());
      } catch (e) {
        emit(AuthUnauthenticated());
      }
    });

    on<AuthLoginRequested>((event, emit) async {
      emit(AuthLoading());
      try {
        final tokenResponse = await apiService.login(event.email, event.password);
        
        // Store token for persistence
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', tokenResponse.accessToken);
        
        emit(AuthAuthenticated(tokenResponse.user, tokenResponse.accessToken));
      } catch (e) {
        emit(AuthError(_getErrorMessage(e.toString())));
      }
    });

    on<AuthRegisterRequested>((event, emit) async {
      emit(AuthLoading());
      try {
        final tokenResponse = await apiService.register(event.userData);
        
        // Store token for persistence
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', tokenResponse.accessToken);
        
        emit(AuthAuthenticated(tokenResponse.user, tokenResponse.accessToken));
      } catch (e) {
        emit(AuthError(_getErrorMessage(e.toString())));
      }
    });

    on<AuthLogoutRequested>((event, emit) async {
      try {
        await apiService.logout();
        
        // Clear stored token
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove('auth_token');
        
        emit(AuthUnauthenticated());
      } catch (e) {
        // Even if logout fails, clear local state
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove('auth_token');
        emit(AuthUnauthenticated());
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