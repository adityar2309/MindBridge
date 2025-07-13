import 'package:flutter/material.dart';
import '../config/app_config.dart';

class AppTheme {
  static const Color primaryColor = Color(0xFF6366F1);
  static const Color secondaryColor = Color(0xFF8B5CF6);
  static const Color accentColor = Color(0xFF22C55E);
  static const Color errorColor = Color(0xFFEF4444);
  static const Color warningColor = Color(0xFFF59E0B);
  static const Color surfaceColor = Color(0xFFFAFAFA);
  static const Color onSurfaceColor = Color(0xFF1F2937);

  // Light Theme
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: const ColorScheme.light(
        primary: primaryColor,
        secondary: secondaryColor,
        tertiary: accentColor,
        error: errorColor,
        surface: surfaceColor,
        onSurface: onSurfaceColor,
        background: Color(0xFFFFFFFF),
        onBackground: Color(0xFF1F2937),
        surfaceVariant: Color(0xFFF3F4F6),
        onSurfaceVariant: Color(0xFF6B7280),
        outline: Color(0xFFD1D5DB),
        outlineVariant: Color(0xFFE5E7EB),
      ),
      scaffoldBackgroundColor: const Color(0xFFFFFFFF),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFFFFFFFF),
        foregroundColor: Color(0xFF1F2937),
        elevation: 0,
        shadowColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        titleTextStyle: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: Color(0xFF1F2937),
        ),
        iconTheme: IconThemeData(color: Color(0xFF6B7280)),
      ),
      cardTheme: CardThemeData(
        color: const Color(0xFFFFFFFF),
        shadowColor: Colors.black.withOpacity(0.05),
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusLG),
        ),
        margin: EdgeInsets.zero,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(
            horizontal: AppConfig.spacingLG,
            vertical: AppConfig.spacingMD,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: primaryColor,
          side: const BorderSide(color: primaryColor),
          padding: const EdgeInsets.symmetric(
            horizontal: AppConfig.spacingLG,
            vertical: AppConfig.spacingMD,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: primaryColor,
          padding: const EdgeInsets.symmetric(
            horizontal: AppConfig.spacingMD,
            vertical: AppConfig.spacingSM,
          ),
          textStyle: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFFF9FAFB),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: Color(0xFFD1D5DB)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: Color(0xFFE5E7EB)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: primaryColor, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: errorColor),
        ),
        contentPadding: const EdgeInsets.all(AppConfig.spacingMD),
        labelStyle: const TextStyle(color: Color(0xFF6B7280)),
        hintStyle: const TextStyle(color: Color(0xFF9CA3AF)),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: const Color(0xFFF3F4F6),
        selectedColor: primaryColor.withOpacity(0.1),
        secondarySelectedColor: secondaryColor.withOpacity(0.1),
        labelStyle: const TextStyle(color: Color(0xFF374151)),
        secondaryLabelStyle: const TextStyle(color: primaryColor),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
        ),
      ),
      sliderTheme: SliderThemeData(
        activeTrackColor: primaryColor,
        inactiveTrackColor: const Color(0xFFE5E7EB),
        thumbColor: primaryColor,
        overlayColor: primaryColor.withOpacity(0.1),
        trackHeight: 4,
        thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 8),
        overlayShape: const RoundSliderOverlayShape(overlayRadius: 16),
      ),
      textTheme: _buildTextTheme(Brightness.light),
    );
  }

  // Dark Theme
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: const ColorScheme.dark(
        primary: Color(0xFF818CF8),
        secondary: Color(0xFFA78BFA),
        tertiary: Color(0xFF34D399),
        error: Color(0xFFF87171),
        surface: Color(0xFF1F2937),
        onSurface: Color(0xFFF9FAFB),
        background: Color(0xFF111827),
        onBackground: Color(0xFFF9FAFB),
        surfaceVariant: Color(0xFF374151),
        onSurfaceVariant: Color(0xFF9CA3AF),
        outline: Color(0xFF4B5563),
        outlineVariant: Color(0xFF374151),
      ),
      scaffoldBackgroundColor: const Color(0xFF111827),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFF1F2937),
        foregroundColor: Color(0xFFF9FAFB),
        elevation: 0,
        shadowColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        titleTextStyle: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: Color(0xFFF9FAFB),
        ),
        iconTheme: IconThemeData(color: Color(0xFF9CA3AF)),
      ),
      cardTheme: CardThemeData(
        color: const Color(0xFF1F2937),
        shadowColor: Colors.black.withOpacity(0.2),
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusLG),
        ),
        margin: EdgeInsets.zero,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF818CF8),
          foregroundColor: const Color(0xFF111827),
          elevation: 0,
          padding: const EdgeInsets.symmetric(
            horizontal: AppConfig.spacingLG,
            vertical: AppConfig.spacingMD,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFF818CF8),
          side: const BorderSide(color: Color(0xFF818CF8)),
          padding: const EdgeInsets.symmetric(
            horizontal: AppConfig.spacingLG,
            vertical: AppConfig.spacingMD,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: const Color(0xFF818CF8),
          padding: const EdgeInsets.symmetric(
            horizontal: AppConfig.spacingMD,
            vertical: AppConfig.spacingSM,
          ),
          textStyle: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: const Color(0xFF374151),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: Color(0xFF4B5563)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: Color(0xFF6B7280)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: Color(0xFF818CF8), width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
          borderSide: const BorderSide(color: Color(0xFFF87171)),
        ),
        contentPadding: const EdgeInsets.all(AppConfig.spacingMD),
        labelStyle: const TextStyle(color: Color(0xFF9CA3AF)),
        hintStyle: const TextStyle(color: Color(0xFF6B7280)),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: const Color(0xFF374151),
        selectedColor: const Color(0xFF818CF8).withOpacity(0.2),
        secondarySelectedColor: const Color(0xFFA78BFA).withOpacity(0.2),
        labelStyle: const TextStyle(color: Color(0xFFF9FAFB)),
        secondaryLabelStyle: const TextStyle(color: Color(0xFF818CF8)),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppConfig.radiusMD),
        ),
      ),
      sliderTheme: SliderThemeData(
        activeTrackColor: const Color(0xFF818CF8),
        inactiveTrackColor: const Color(0xFF4B5563),
        thumbColor: const Color(0xFF818CF8),
        overlayColor: const Color(0xFF818CF8).withOpacity(0.2),
        trackHeight: 4,
        thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 8),
        overlayShape: const RoundSliderOverlayShape(overlayRadius: 16),
      ),
      textTheme: _buildTextTheme(Brightness.dark),
    );
  }

  static TextTheme _buildTextTheme(Brightness brightness) {
    final baseColor = brightness == Brightness.light 
        ? const Color(0xFF1F2937)
        : const Color(0xFFF9FAFB);
    final subtleColor = brightness == Brightness.light
        ? const Color(0xFF6B7280)
        : const Color(0xFF9CA3AF);

    return TextTheme(
      displayLarge: TextStyle(
        fontSize: 57,
        fontWeight: FontWeight.w400,
        letterSpacing: -0.25,
        color: baseColor,
      ),
      displayMedium: TextStyle(
        fontSize: 45,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
        color: baseColor,
      ),
      displaySmall: TextStyle(
        fontSize: 36,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
        color: baseColor,
      ),
      headlineLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.w600,
        letterSpacing: 0,
        color: baseColor,
      ),
      headlineMedium: TextStyle(
        fontSize: 28,
        fontWeight: FontWeight.w600,
        letterSpacing: 0,
        color: baseColor,
      ),
      headlineSmall: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.w600,
        letterSpacing: 0,
        color: baseColor,
      ),
      titleLarge: TextStyle(
        fontSize: 22,
        fontWeight: FontWeight.w600,
        letterSpacing: 0,
        color: baseColor,
      ),
      titleMedium: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.15,
        color: baseColor,
      ),
      titleSmall: TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.1,
        color: baseColor,
      ),
      labelLarge: TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.1,
        color: baseColor,
      ),
      labelMedium: TextStyle(
        fontSize: 12,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.5,
        color: baseColor,
      ),
      labelSmall: TextStyle(
        fontSize: 11,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.5,
        color: subtleColor,
      ),
      bodyLarge: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.5,
        color: baseColor,
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.25,
        color: baseColor,
      ),
      bodySmall: TextStyle(
        fontSize: 12,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.4,
        color: subtleColor,
      ),
    );
  }

  // Helper methods for mood colors
  static Color getMoodColor(double mood) {
    if (mood <= 2) return const Color(0xFFEF4444);
    if (mood <= 4) return const Color(0xFFF59E0B);
    if (mood <= 6) return const Color(0xFF84CC16);
    if (mood <= 8) return const Color(0xFF22C55E);
    return const Color(0xFF6366F1);
  }

  static String getMoodEmoji(double mood) {
    if (mood <= 2) return '😢';
    if (mood <= 4) return '😔';
    if (mood <= 6) return '😐';
    if (mood <= 8) return '😊';
    return '😄';
  }

  static String getMoodLabel(double mood) {
    if (mood <= 2) return 'Very Low';
    if (mood <= 4) return 'Low';
    if (mood <= 6) return 'Neutral';
    if (mood <= 8) return 'Good';
    return 'Excellent';
  }
} 