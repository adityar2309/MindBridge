import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:responsive_framework/responsive_framework.dart';
import '../bloc/dashboard_bloc.dart';
import '../../../auth/presentation/bloc/auth_bloc.dart';
import '../../widgets/checkin_form_widget.dart';
import '../../../../models/checkin_models.dart';
import '../../../../core/config/app_config.dart';

class CheckinPage extends StatefulWidget {
  const CheckinPage({super.key});

  @override
  State<CheckinPage> createState() => _CheckinPageState();
}

class _CheckinPageState extends State<CheckinPage> {
  bool _isSubmitting = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Daily Check-in'),
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard),
            onPressed: () {
              Navigator.pushReplacementNamed(context, '/dashboard');
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Center(
          child: Container(
            constraints: BoxConstraints(
              maxWidth: ResponsiveBreakpoints.of(context).isMobile ? double.infinity : 800,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (!ResponsiveBreakpoints.of(context).isMobile) ...[
                  _buildHeader(context),
                  const SizedBox(height: AppConfig.spacingXL),
                ],
                
                CheckinFormWidget(
                  onSubmit: _handleSubmit,
                  isLoading: _isSubmitting,
                ),
                
                const SizedBox(height: AppConfig.spacingXL),
                _buildTips(context),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(AppConfig.spacingXL),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Theme.of(context).colorScheme.primary.withOpacity(0.1),
            Theme.of(context).colorScheme.secondary.withOpacity(0.1),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(AppConfig.radiusLG),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'How are you feeling today?',
            style: Theme.of(context).textTheme.displaySmall?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: AppConfig.spacingMD),
          Text(
            'Take a moment to reflect on your mood, energy, and experiences. Your daily check-ins help track patterns and support your mental health journey.',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: Theme.of(context).colorScheme.onSurface.withOpacity(0.8),
            ),
          ),
          const SizedBox(height: AppConfig.spacingLG),
          
          // Quick stats row
          Row(
            children: [
              _buildQuickStat(
                context,
                Icons.calendar_today,
                'Daily',
                'Track progress',
              ),
              const SizedBox(width: AppConfig.spacingXL),
              _buildQuickStat(
                context,
                Icons.insights,
                'Insights',
                'Discover patterns',
              ),
              const SizedBox(width: AppConfig.spacingXL),
              _buildQuickStat(
                context,
                Icons.psychology,
                'Growth',
                'Improve wellbeing',
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildQuickStat(BuildContext context, IconData icon, String title, String subtitle) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(AppConfig.spacingMD),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
            borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          ),
          child: Icon(
            icon,
            color: Theme.of(context).colorScheme.primary,
            size: 24,
          ),
        ),
        const SizedBox(width: AppConfig.spacingMD),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              subtitle,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildTips(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.lightbulb_outline,
                  color: Theme.of(context).colorScheme.primary,
                ),
                const SizedBox(width: AppConfig.spacingSM),
                Text(
                  'Tips for Better Check-ins',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppConfig.spacingMD),
            
            _buildTipItem(
              context,
              'Be honest with yourself',
              'There are no right or wrong answers. Your authentic feelings matter most.',
            ),
            _buildTipItem(
              context,
              'Take your time',
              'Reflect on your day before rating. Consider what influenced your mood.',
            ),
            _buildTipItem(
              context,
              'Track consistently',
              'Daily check-ins help identify patterns and track your progress over time.',
            ),
            _buildTipItem(
              context,
              'Use keywords',
              'Select keywords that represent what affected your mood today.',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTipItem(BuildContext context, String title, String description) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppConfig.spacingMD),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 6,
            height: 6,
            margin: const EdgeInsets.only(top: 8),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: AppConfig.spacingMD),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: AppConfig.spacingXS),
                Text(
                  description,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _handleSubmit(DailyCheckinCreate checkin) async {
    setState(() {
      _isSubmitting = true;
    });

    try {
      final authState = context.read<AuthBloc>().state;
      if (authState is AuthAuthenticated) {
        // TODO: Submit checkin via API service
        // For now, simulate API call
        await Future.delayed(const Duration(seconds: 2));
        
        if (mounted) {
          // Show success message
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Row(
                children: [
                  Icon(Icons.check_circle, color: Colors.white),
                  SizedBox(width: AppConfig.spacingMD),
                  Text('Check-in completed successfully!'),
                ],
              ),
              backgroundColor: Colors.green,
              behavior: SnackBarBehavior.floating,
              action: SnackBarAction(
                label: 'View Dashboard',
                textColor: Colors.white,
                onPressed: () {
                  Navigator.pushReplacementNamed(context, '/dashboard');
                },
              ),
            ),
          );
          
          // Navigate back to dashboard after a short delay
          Future.delayed(const Duration(seconds: 2), () {
            if (mounted) {
              Navigator.pushReplacementNamed(context, '/dashboard');
            }
          });
        }
      } else {
        throw Exception('User not authenticated');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(
              children: [
                const Icon(Icons.error, color: Colors.white),
                const SizedBox(width: AppConfig.spacingMD),
                Text('Error: ${e.toString()}'),
              ],
            ),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });
      }
    }
  }
} 