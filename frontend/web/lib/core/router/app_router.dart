import 'package:flutter/material.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/dashboard/presentation/pages/dashboard_page.dart';
import '../../features/dashboard/presentation/pages/checkin_page.dart';
import '../../features/analytics/presentation/pages/analytics_page.dart';
import 'auth_guard.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    final routeName = settings.name ?? '/';
    
    switch (routeName) {
      case '/':
      case '/dashboard':
        return MaterialPageRoute(
          builder: (context) => AuthGuard.getRouteWidget(
            context,
            routeName,
            () => const DashboardPage(),
          ),
        );
      case '/login':
        return MaterialPageRoute(
          builder: (context) => AuthGuard.getRouteWidget(
            context,
            routeName,
            () => const LoginPage(),
          ),
        );
      case '/checkin':
        return MaterialPageRoute(
          builder: (context) => AuthGuard.getRouteWidget(
            context,
            routeName,
            () => const CheckinPage(),
          ),
        );
      case '/analytics':
        return MaterialPageRoute(
          builder: (context) => AuthGuard.getRouteWidget(
            context,
            routeName,
            () => const AnalyticsPage(),
          ),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            body: Center(
              child: Text('No route defined for ${settings.name}'),
            ),
          ),
        );
    }
  }
  
  // For compatibility with the existing structure
  static final _router = _AppRouter();
  static _AppRouter get router => _router;
}

class _AppRouter {
  final String initialLocation = '/';
  
  Route<dynamic> call(RouteSettings settings) {
    return AppRouter.generateRoute(settings);
  }
} 