import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../models/checkin_models.dart';
import '../../../core/config/app_config.dart';

class MoodChartWidget extends StatelessWidget {
  final Map<String, dynamic> data;
  
  const MoodChartWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final trends = _getTrendsFromData();
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Mood Trends',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                _buildPeriodSelector(context),
              ],
            ),
            const SizedBox(height: AppConfig.spacingLG),
            SizedBox(
              height: 300,
              child: trends.isNotEmpty 
                  ? _buildLineChart(context, trends)
                  : _buildEmptyState(context),
            ),
            const SizedBox(height: AppConfig.spacingMD),
            _buildLegend(context),
          ],
        ),
      ),
    );
  }

  List<MoodTrend> _getTrendsFromData() {
    final trendsData = data['trends'] as List<dynamic>? ?? [];
    return trendsData
        .map((trend) => MoodTrend.fromJson(trend as Map<String, dynamic>))
        .toList();
  }

  Widget _buildPeriodSelector(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppConfig.radiusMD),
        border: Border.all(color: Theme.of(context).colorScheme.outline),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildPeriodButton(context, '7D', true),
          _buildPeriodButton(context, '30D', false),
          _buildPeriodButton(context, '90D', false),
        ],
      ),
    );
  }

  Widget _buildPeriodButton(BuildContext context, String label, bool isSelected) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppConfig.spacingMD,
        vertical: AppConfig.spacingSM,
      ),
      decoration: BoxDecoration(
        color: isSelected 
            ? Theme.of(context).colorScheme.primary
            : Colors.transparent,
        borderRadius: BorderRadius.circular(AppConfig.radiusMD),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: isSelected 
              ? Theme.of(context).colorScheme.onPrimary
              : Theme.of(context).colorScheme.onSurface,
          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
        ),
      ),
    );
  }

  Widget _buildLineChart(BuildContext context, List<MoodTrend> trends) {
    final moodSpots = trends.asMap().entries.map((entry) {
      return FlSpot(entry.key.toDouble(), entry.value.moodRating);
    }).toList();

    final energySpots = trends.asMap().entries.map((entry) {
      return FlSpot(entry.key.toDouble(), entry.value.energyLevel ?? 5.0);
    }).toList();

    final stressSpots = trends.asMap().entries.map((entry) {
      return FlSpot(entry.key.toDouble(), entry.value.stressLevel ?? 5.0);
    }).toList();

    return LineChart(
      LineChartData(
        gridData: FlGridData(
          show: true,
          drawVerticalLine: true,
          horizontalInterval: 1,
          verticalInterval: 1,
          getDrawingHorizontalLine: (value) {
            return FlLine(
              color: Theme.of(context).colorScheme.outline.withOpacity(0.2),
              strokeWidth: 1,
            );
          },
          getDrawingVerticalLine: (value) {
            return FlLine(
              color: Theme.of(context).colorScheme.outline.withOpacity(0.2),
              strokeWidth: 1,
            );
          },
        ),
        titlesData: FlTitlesData(
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 30,
              interval: 1,
              getTitlesWidget: (value, meta) => _buildBottomTitle(value, trends),
            ),
          ),
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              interval: 1,
              getTitlesWidget: (value, meta) => Text(
                value.toInt().toString(),
                style: TextStyle(
                  color: Theme.of(context).colorScheme.onSurface,
                  fontSize: 12,
                ),
              ),
              reservedSize: 28,
            ),
          ),
        ),
        borderData: FlBorderData(
          show: true,
          border: Border.all(color: Theme.of(context).colorScheme.outline),
        ),
        minX: 0,
        maxX: (trends.length - 1).toDouble(),
        minY: 0,
        maxY: 10,
        lineBarsData: [
          LineChartBarData(
            spots: moodSpots,
            isCurved: true,
            color: AppConfig.chartColors[0],
            barWidth: 3,
            isStrokeCapRound: true,
            dotData: const FlDotData(show: true),
            belowBarData: BarAreaData(
              show: true,
              color: AppConfig.chartColors[0].withOpacity(0.1),
            ),
          ),
          LineChartBarData(
            spots: energySpots,
            isCurved: true,
            color: AppConfig.chartColors[1],
            barWidth: 2,
            isStrokeCapRound: true,
            dotData: const FlDotData(show: true),
            dashArray: [5, 5],
          ),
          LineChartBarData(
            spots: stressSpots,
            isCurved: true,
            color: AppConfig.chartColors[4],
            barWidth: 2,
            isStrokeCapRound: true,
            dotData: const FlDotData(show: true),
            dashArray: [2, 4],
          ),
        ],
        lineTouchData: LineTouchData(
          enabled: true,
          touchTooltipData: LineTouchTooltipData(
            getTooltipItems: (touchedSpots) {
              return touchedSpots.map((spot) {
                String label = '';
                if (spot.barIndex == 0) label = 'Mood: ${spot.y.toStringAsFixed(1)}';
                if (spot.barIndex == 1) label = 'Energy: ${spot.y.toStringAsFixed(1)}';
                if (spot.barIndex == 2) label = 'Stress: ${spot.y.toStringAsFixed(1)}';
                
                return LineTooltipItem(
                  label,
                  TextStyle(
                    color: Theme.of(context).colorScheme.onSurface,
                    fontWeight: FontWeight.bold,
                  ),
                );
              }).toList();
            },
          ),
        ),
      ),
    );
  }

  Widget _buildBottomTitle(double value, List<MoodTrend> trends) {
    if (value.toInt() >= trends.length) return const SizedBox.shrink();
    
    final trend = trends[value.toInt()];
    final date = DateTime.parse(trend.date);
    final dayLabel = '${date.month}/${date.day}';
    
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Text(
        dayLabel,
        style: const TextStyle(fontSize: 10),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.show_chart,
            size: 64,
            color: Theme.of(context).colorScheme.primary.withOpacity(0.5),
          ),
          const SizedBox(height: AppConfig.spacingMD),
          Text(
            'No mood data available',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: AppConfig.spacingSM),
          Text(
            'Complete your daily check-ins to see trends',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLegend(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _buildLegendItem(context, 'Mood', AppConfig.chartColors[0], true),
        const SizedBox(width: AppConfig.spacingLG),
        _buildLegendItem(context, 'Energy', AppConfig.chartColors[1], false),
        const SizedBox(width: AppConfig.spacingLG),
        _buildLegendItem(context, 'Stress', AppConfig.chartColors[4], false),
      ],
    );
  }

  Widget _buildLegendItem(BuildContext context, String label, Color color, bool isSolid) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 16,
          height: 3,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(2),
          ),
          child: isSolid ? null : CustomPaint(
            painter: DashedLinePainter(color),
          ),
        ),
        const SizedBox(width: AppConfig.spacingSM),
        Text(
          label,
          style: Theme.of(context).textTheme.bodySmall,
        ),
      ],
    );
  }
}

class DashedLinePainter extends CustomPainter {
  final Color color;

  DashedLinePainter(this.color);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2;

    const dashWidth = 3;
    const dashSpace = 2;
    double startX = 0;

    while (startX < size.width) {
      canvas.drawLine(
        Offset(startX, size.height / 2),
        Offset(startX + dashWidth, size.height / 2),
        paint,
      );
      startX += dashWidth + dashSpace;
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
} 