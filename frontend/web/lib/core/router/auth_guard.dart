import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../features/auth/presentation/bloc/auth_bloc.dart';
import '../../features/auth/presentation/pages/login_page.dart';

/// Authentication guard that checks if user is authenticated
class AuthGuard {
  /// Checks if the current route requires authentication
  static bool requiresAuth(String route) {
    const publicRoutes = ['/login', '/register'];
    return !publicRoutes.contains(route);
  }
  
  /// Returns the appropriate widget based on authentication state
  static Widget getRouteWidget(BuildContext context, String route, Widget Function() widgetBuilder) {
    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, authState) {
        // If route requires auth and user is not authenticated, redirect to login
        if (requiresAuth(route) && authState is! AuthAuthenticated) {
          return const LoginPage();
        }
        
        // If user is authenticated and trying to access login, redirect to dashboard
        if (!requiresAuth(route) && authState is AuthAuthenticated) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
          });
          return const SizedBox.shrink(); // Return empty widget while redirecting
        }
        
        // Return the requested widget
        return widgetBuilder();
      },
    );
  }
} 