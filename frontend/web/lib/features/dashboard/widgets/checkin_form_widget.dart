import 'package:flutter/material.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:form_builder_validators/form_builder_validators.dart';
import '../../../models/checkin_models.dart';
import '../../../core/config/app_config.dart';

class CheckinFormWidget extends StatefulWidget {
  final Function(DailyCheckinCreate) onSubmit;
  final bool isLoading;

  const CheckinFormWidget({
    super.key,
    required this.onSubmit,
    this.isLoading = false,
  });

  @override
  State<CheckinFormWidget> createState() => _CheckinFormWidgetState();
}

class _CheckinFormWidgetState extends State<CheckinFormWidget> {
  final _formKey = GlobalKey<FormBuilderState>();
  double _moodRating = 5.0;
  String? _selectedCategory;
  List<String> _selectedKeywords = [];
  double _energyLevel = 5.0;
  double _stressLevel = 5.0;
  double _sleepQuality = 5.0;
  double _socialInteraction = 5.0;

  final List<String> _moodCategories = [
    'happy', 'content', 'calm', 'excited', 'optimistic',
    'sad', 'anxious', 'stressed', 'angry', 'frustrated',
    'tired', 'energetic', 'focused', 'confused', 'lonely',
    'grateful', 'hopeful', 'overwhelmed', 'peaceful', 'neutral'
  ];

  final List<String> _keywords = [
    'work', 'family', 'friends', 'exercise', 'sleep',
    'meditation', 'social', 'creative', 'learning', 'relaxation',
    'challenge', 'achievement', 'travel', 'nature', 'music',
    'food', 'health', 'relationship', 'hobby', 'spiritual'
  ];

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppConfig.spacingLG),
        child: FormBuilder(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Daily Check-in',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const SizedBox(height: AppConfig.spacingLG),
              
              _buildMoodRatingSection(),
              const SizedBox(height: AppConfig.spacingXL),
              
              _buildMoodCategorySection(),
              const SizedBox(height: AppConfig.spacingXL),
              
              _buildKeywordsSection(),
              const SizedBox(height: AppConfig.spacingXL),
              
              _buildMetricsSection(),
              const SizedBox(height: AppConfig.spacingXL),
              
              _buildNotesSection(),
              const SizedBox(height: AppConfig.spacingXL),
              
              _buildLocationWeatherSection(),
              const SizedBox(height: AppConfig.spacingXXL),
              
              _buildSubmitButton(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMoodRatingSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'How are you feeling today?',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: AppConfig.spacingMD),
        
        // Visual mood indicator
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(AppConfig.spacingLG),
          decoration: BoxDecoration(
            color: _getMoodColor(_moodRating).withOpacity(0.1),
            borderRadius: BorderRadius.circular(AppConfig.radiusLG),
            border: Border.all(color: _getMoodColor(_moodRating)),
          ),
          child: Column(
            children: [
              Text(
                _getMoodEmoji(_moodRating),
                style: const TextStyle(fontSize: 48),
              ),
              const SizedBox(height: AppConfig.spacingSM),
              Text(
                _getMoodLabel(_moodRating),
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: _getMoodColor(_moodRating),
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                _moodRating.toStringAsFixed(1),
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ],
          ),
        ),
        
        const SizedBox(height: AppConfig.spacingMD),
        
        // Mood slider
        SliderTheme(
          data: SliderTheme.of(context).copyWith(
            activeTrackColor: _getMoodColor(_moodRating),
            thumbColor: _getMoodColor(_moodRating),
            overlayColor: _getMoodColor(_moodRating).withOpacity(0.2),
          ),
          child: Slider(
            value: _moodRating,
            min: 1,
            max: 10,
            divisions: 18,
            onChanged: (value) {
              setState(() {
                _moodRating = value;
              });
            },
          ),
        ),
        
        // Scale labels
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('Very Low (1)', style: Theme.of(context).textTheme.bodySmall),
            Text('Neutral (5)', style: Theme.of(context).textTheme.bodySmall),
            Text('Very High (10)', style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
      ],
    );
  }

  Widget _buildMoodCategorySection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'What describes your mood best?',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: AppConfig.spacingMD),
        
        Wrap(
          spacing: AppConfig.spacingSM,
          runSpacing: AppConfig.spacingSM,
          children: _moodCategories.map((category) {
            final isSelected = _selectedCategory == category;
            return FilterChip(
              label: Text(category),
              selected: isSelected,
              onSelected: (selected) {
                setState(() {
                  _selectedCategory = selected ? category : null;
                });
              },
              selectedColor: Theme.of(context).colorScheme.primary.withOpacity(0.2),
              checkmarkColor: Theme.of(context).colorScheme.primary,
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildKeywordsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'What influenced your mood today?',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: AppConfig.spacingSM),
        Text(
          'Select all that apply',
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
            color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
          ),
        ),
        const SizedBox(height: AppConfig.spacingMD),
        
        Wrap(
          spacing: AppConfig.spacingSM,
          runSpacing: AppConfig.spacingSM,
          children: _keywords.map((keyword) {
            final isSelected = _selectedKeywords.contains(keyword);
            return FilterChip(
              label: Text(keyword),
              selected: isSelected,
              onSelected: (selected) {
                setState(() {
                  if (selected) {
                    _selectedKeywords.add(keyword);
                  } else {
                    _selectedKeywords.remove(keyword);
                  }
                });
              },
              selectedColor: Theme.of(context).colorScheme.secondary.withOpacity(0.2),
              checkmarkColor: Theme.of(context).colorScheme.secondary,
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildMetricsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Additional Metrics',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: AppConfig.spacingMD),
        
        _buildMetricSlider(
          'Energy Level',
          _energyLevel,
          (value) => setState(() => _energyLevel = value),
          AppConfig.chartColors[1],
        ),
        const SizedBox(height: AppConfig.spacingLG),
        
        _buildMetricSlider(
          'Stress Level',
          _stressLevel,
          (value) => setState(() => _stressLevel = value),
          AppConfig.chartColors[4],
        ),
        const SizedBox(height: AppConfig.spacingLG),
        
        _buildMetricSlider(
          'Sleep Quality',
          _sleepQuality,
          (value) => setState(() => _sleepQuality = value),
          AppConfig.chartColors[2],
        ),
        const SizedBox(height: AppConfig.spacingLG),
        
        _buildMetricSlider(
          'Social Interaction',
          _socialInteraction,
          (value) => setState(() => _socialInteraction = value),
          AppConfig.chartColors[6],
        ),
      ],
    );
  }

  Widget _buildMetricSlider(String label, double value, Function(double) onChanged, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: Theme.of(context).textTheme.bodyLarge),
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: AppConfig.spacingSM,
                vertical: AppConfig.spacingXS,
              ),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(AppConfig.radiusSM),
              ),
              child: Text(
                value.toStringAsFixed(1),
                style: TextStyle(
                  color: color,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: AppConfig.spacingSM),
        
        SliderTheme(
          data: SliderTheme.of(context).copyWith(
            activeTrackColor: color,
            thumbColor: color,
            overlayColor: color.withOpacity(0.2),
          ),
          child: Slider(
            value: value,
            min: 1,
            max: 10,
            divisions: 18,
            onChanged: onChanged,
          ),
        ),
      ],
    );
  }

  Widget _buildNotesSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Additional Notes',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: AppConfig.spacingSM),
        Text(
          'Anything else you\'d like to record about today?',
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
            color: Theme.of(context).colorScheme.onSurface.withOpacity(0.7),
          ),
        ),
        const SizedBox(height: AppConfig.spacingMD),
        
        FormBuilderTextField(
          name: 'notes',
          maxLines: 4,
          decoration: const InputDecoration(
            hintText: 'Write your thoughts, experiences, or anything noteworthy...',
            border: OutlineInputBorder(),
          ),
        ),
      ],
    );
  }

  Widget _buildLocationWeatherSection() {
    return Row(
      children: [
        Expanded(
          child: FormBuilderTextField(
            name: 'location',
            decoration: const InputDecoration(
              labelText: 'Location (optional)',
              prefixIcon: Icon(Icons.location_on),
              border: OutlineInputBorder(),
            ),
          ),
        ),
        const SizedBox(width: AppConfig.spacingMD),
        Expanded(
          child: FormBuilderTextField(
            name: 'weather',
            decoration: const InputDecoration(
              labelText: 'Weather (optional)',
              prefixIcon: Icon(Icons.wb_sunny),
              border: OutlineInputBorder(),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSubmitButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: widget.isLoading ? null : _submitForm,
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.all(AppConfig.spacingLG),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConfig.radiusLG),
          ),
        ),
        child: widget.isLoading
            ? const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                  SizedBox(width: AppConfig.spacingMD),
                  Text('Submitting...'),
                ],
              )
            : const Text(
                'Complete Check-in',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
      ),
    );
  }

  void _submitForm() {
    if (_formKey.currentState?.saveAndValidate() == true) {
      final formData = _formKey.currentState!.value;
      
      final checkin = DailyCheckinCreate(
        moodRating: _moodRating,
        moodCategory: _selectedCategory,
        keywords: _selectedKeywords,
        notes: formData['notes'] as String?,
        location: formData['location'] as String?,
        weather: formData['weather'] as String?,
        energyLevel: _energyLevel,
        stressLevel: _stressLevel,
        sleepQuality: _sleepQuality,
        socialInteraction: _socialInteraction,
      );
      
      widget.onSubmit(checkin);
    }
  }

  Color _getMoodColor(double mood) {
    if (mood <= 2) return const Color(0xFFEF4444); // Red
    if (mood <= 4) return const Color(0xFFF97316); // Orange
    if (mood <= 6) return const Color(0xFFFBBF24); // Yellow
    if (mood <= 8) return const Color(0xFF22C55E); // Green
    return const Color(0xFF6366F1); // Blue
  }

  String _getMoodEmoji(double mood) {
    if (mood <= 2) return '😢';
    if (mood <= 4) return '😕';
    if (mood <= 6) return '😐';
    if (mood <= 8) return '😊';
    return '😄';
  }

  String _getMoodLabel(double mood) {
    if (mood <= 2) return 'Very Low';
    if (mood <= 4) return 'Low';
    if (mood <= 6) return 'Neutral';
    if (mood <= 8) return 'Good';
    return 'Excellent';
  }
} 