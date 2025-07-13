import 'package:flutter/material.dart';

class RecentCheckinsWidget extends StatelessWidget {
  final Map<String, dynamic> data;
  
  const RecentCheckinsWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final checkins = data['recentCheckins'] as List<dynamic>? ?? [];
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Recent Check-ins',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            if (checkins.isEmpty)
              Center(
                child: Column(
                  children: [
                    Icon(
                      Icons.sentiment_neutral,
                      size: 48,
                      color: Theme.of(context).colorScheme.outline,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'No recent check-ins',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                ),
              )
            else
              ...checkins.map((checkin) => _CheckinItem(
                date: checkin['date'] ?? '',
                mood: checkin['mood'] ?? 5,
                notes: checkin['notes'] ?? '',
              )).toList(),
          ],
        ),
      ),
    );
  }
}

class _CheckinItem extends StatelessWidget {
  final String date;
  final int mood;
  final String notes;

  const _CheckinItem({
    required this.date,
    required this.mood,
    required this.notes,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 32,
            height: 32,
            decoration: BoxDecoration(
              color: _getMoodColor(mood),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Center(
              child: Text(
                mood.toString(),
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _formatDate(date),
                  style: Theme.of(context).textTheme.titleSmall,
                ),
                const SizedBox(height: 2),
                if (notes.isNotEmpty)
                  Text(
                    notes,
                    style: Theme.of(context).textTheme.bodySmall,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Color _getMoodColor(int mood) {
    if (mood <= 3) return const Color(0xFFEF4444); // Red
    if (mood <= 5) return const Color(0xFFF59E0B); // Yellow
    if (mood <= 7) return const Color(0xFF22C55E); // Green
    return const Color(0xFF6366F1); // Blue
  }

  String _formatDate(String date) {
    try {
      final dateTime = DateTime.parse(date);
      final now = DateTime.now();
      final difference = now.difference(dateTime).inDays;
      
      if (difference == 0) return 'Today';
      if (difference == 1) return 'Yesterday';
      return '${difference} days ago';
    } catch (e) {
      return date;
    }
  }
} 