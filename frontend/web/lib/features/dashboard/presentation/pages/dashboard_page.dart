import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:responsive_framework/responsive_framework.dart';
import '../bloc/dashboard_bloc.dart';
import '../../widgets/mood_chart_widget.dart';
import '../../widgets/stats_cards_widget.dart';
import '../../widgets/recent_checkins_widget.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  @override
  void initState() {
    super.initState();
    context.read<DashboardBloc>().add(DashboardDataRequested());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('MindBridge Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.analytics),
            onPressed: () {
              // Navigate to analytics
            },
          ),
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () {
              // Navigate to profile
            },
          ),
        ],
      ),
      body: BlocBuilder<DashboardBloc, DashboardState>(
        builder: (context, state) {
          if (state is DashboardLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          
          if (state is DashboardError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 64, color: Colors.red),
                  const SizedBox(height: 16),
                  Text('Error: ${state.message}'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      context.read<DashboardBloc>().add(DashboardDataRequested());
                    },
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }
          
          if (state is DashboardLoaded) {
            return SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: ResponsiveRowColumn(
                layout: ResponsiveBreakpoints.of(context).isMobile
                    ? ResponsiveRowColumnType.COLUMN
                    : ResponsiveRowColumnType.ROW,
                rowCrossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  ResponsiveRowColumnItem(
                    rowFlex: 2,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Welcome back!',
                          style: Theme.of(context).textTheme.displaySmall,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Here\'s your mood overview for today',
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                        const SizedBox(height: 24),
                        StatsCardsWidget(data: state.data),
                        const SizedBox(height: 24),
                        MoodChartWidget(data: state.data),
                      ],
                    ),
                  ),
                  ResponsiveRowColumnItem(
                    rowFlex: 1,
                    child: Padding(
                      padding: ResponsiveBreakpoints.of(context).isMobile
                          ? const EdgeInsets.only(top: 24)
                          : const EdgeInsets.only(left: 24),
                      child: RecentCheckinsWidget(data: state.data),
                    ),
                  ),
                ],
              ),
            );
          }
          
          return const Center(child: Text('No data available'));
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          // Quick check-in action
        },
        icon: const Icon(Icons.add),
        label: const Text('Quick Check-in'),
      ),
    );
  }
} 