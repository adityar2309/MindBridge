import 'package:flutter/material.dart';
import 'package:responsive_framework/responsive_framework.dart';

class StatsCardsWidget extends StatelessWidget {
  final Map<String, dynamic> data;
  
  const StatsCardsWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return ResponsiveRowColumn(
      layout: ResponsiveBreakpoints.of(context).smallerThan(TABLET)
          ? ResponsiveRowColumnType.COLUMN
          : ResponsiveRowColumnType.ROW,
      rowSpacing: 16,
      columnSpacing: 16,
      children: [
        ResponsiveRowColumnItem(
          child: _StatCard(
            title: "Today's Mood",
            value: data['todaysMood']?.toString() ?? '7',
            icon: Icons.mood,
            color: const Color(0xFF22C55E),
          ),
        ),
        ResponsiveRowColumnItem(
          child: _StatCard(
            title: 'Current Streak',
            value: '${data['streak'] ?? 5} days',
            icon: Icons.local_fire_department,
            color: const Color(0xFFF59E0B),
          ),
        ),
        ResponsiveRowColumnItem(
          child: _StatCard(
            title: 'Weekly Average',
            value: data['weeklyAverage']?.toString() ?? '6.5',
            icon: Icons.trending_up,
            color: const Color(0xFF6366F1),
          ),
        ),
      ],
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color color;

  const _StatCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(icon, color: color, size: 24),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
} 