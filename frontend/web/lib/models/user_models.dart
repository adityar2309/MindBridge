import 'package:json_annotation/json_annotation.dart';

part 'user_models.g.dart';

@JsonSerializable()
class UserLogin {
  final String email;
  final String password;

  const UserLogin({
    required this.email,
    required this.password,
  });

  factory UserLogin.fromJson(Map<String, dynamic> json) =>
      _$UserLoginFromJson(json);

  Map<String, dynamic> toJson() => _$UserLoginToJson(this);
}

@JsonSerializable()
class UserCreate {
  final String name;
  final String email;
  final String password;
  final String timezone;
  final String language;
  final UserSettings? settings;

  const UserCreate({
    required this.name,
    required this.email,
    required this.password,
    this.timezone = 'UTC',
    this.language = 'en',
    this.settings,
  });

  factory UserCreate.fromJson(Map<String, dynamic> json) =>
      _$UserCreateFromJson(json);

  Map<String, dynamic> toJson() => _$UserCreateToJson(this);
}

@JsonSerializable()
class UserSettings {
  final Map<String, dynamic> notifications;
  final Map<String, dynamic> privacy;
  final Map<String, dynamic> ui;

  const UserSettings({
    required this.notifications,
    required this.privacy,
    required this.ui,
  });

  factory UserSettings.fromJson(Map<String, dynamic> json) =>
      _$UserSettingsFromJson(json);

  Map<String, dynamic> toJson() => _$UserSettingsToJson(this);

  static UserSettings get defaultSettings => const UserSettings(
    notifications: {
      'daily_reminder': true,
      'weekly_summary': true,
      'mood_alerts': true,
      'reminder_time': '09:00',
    },
    privacy: {
      'data_sharing': false,
      'anonymous_analytics': true,
    },
    ui: {
      'theme': 'auto',
      'font_size': 'medium',
      'animations': true,
    },
  );
}

@JsonSerializable()
class UserResponse {
  @JsonKey(name: 'user_id')
  final int userId;
  
  final String name;
  final String email;
  
  @JsonKey(name: 'registration_date')
  final DateTime registrationDate;
  
  @JsonKey(name: 'is_active')
  final bool isActive;
  
  final Map<String, dynamic> settings;
  
  @JsonKey(name: 'last_login')
  final DateTime? lastLogin;
  
  final String timezone;
  final String language;

  const UserResponse({
    required this.userId,
    required this.name,
    required this.email,
    required this.registrationDate,
    required this.isActive,
    required this.settings,
    this.lastLogin,
    required this.timezone,
    required this.language,
  });

  factory UserResponse.fromJson(Map<String, dynamic> json) =>
      _$UserResponseFromJson(json);

  Map<String, dynamic> toJson() => _$UserResponseToJson(this);
}

@JsonSerializable()
class TokenResponse {
  @JsonKey(name: 'access_token')
  final String accessToken;
  
  @JsonKey(name: 'token_type')
  final String tokenType;
  
  @JsonKey(name: 'expires_in')
  final int expiresIn;
  
  @JsonKey(name: 'refresh_token')
  final String? refreshToken;
  
  final UserResponse user;

  const TokenResponse({
    required this.accessToken,
    this.tokenType = 'bearer',
    required this.expiresIn,
    this.refreshToken,
    required this.user,
  });

  factory TokenResponse.fromJson(Map<String, dynamic> json) =>
      _$TokenResponseFromJson(json);

  Map<String, dynamic> toJson() => _$TokenResponseToJson(this);
}

@JsonSerializable()
class RefreshTokenRequest {
  @JsonKey(name: 'refresh_token')
  final String refreshToken;

  const RefreshTokenRequest({
    required this.refreshToken,
  });

  factory RefreshTokenRequest.fromJson(Map<String, dynamic> json) =>
      _$RefreshTokenRequestFromJson(json);

  Map<String, dynamic> toJson() => _$RefreshTokenRequestToJson(this);
}

@JsonSerializable()
class ForgotPasswordRequest {
  final String email;

  const ForgotPasswordRequest({
    required this.email,
  });

  factory ForgotPasswordRequest.fromJson(Map<String, dynamic> json) =>
      _$ForgotPasswordRequestFromJson(json);

  Map<String, dynamic> toJson() => _$ForgotPasswordRequestToJson(this);
}

@JsonSerializable()
class ResetPasswordRequest {
  final String token;
  
  @JsonKey(name: 'new_password')
  final String newPassword;
  
  @JsonKey(name: 'confirm_password')
  final String confirmPassword;

  const ResetPasswordRequest({
    required this.token,
    required this.newPassword,
    required this.confirmPassword,
  });

  factory ResetPasswordRequest.fromJson(Map<String, dynamic> json) =>
      _$ResetPasswordRequestFromJson(json);

  Map<String, dynamic> toJson() => _$ResetPasswordRequestToJson(this);
}

@JsonSerializable()
class PasswordChange {
  @JsonKey(name: 'current_password')
  final String currentPassword;
  
  @JsonKey(name: 'new_password')
  final String newPassword;
  
  @JsonKey(name: 'confirm_password')
  final String confirmPassword;

  const PasswordChange({
    required this.currentPassword,
    required this.newPassword,
    required this.confirmPassword,
  });

  factory PasswordChange.fromJson(Map<String, dynamic> json) =>
      _$PasswordChangeFromJson(json);

  Map<String, dynamic> toJson() => _$PasswordChangeToJson(this);
}

// Generic API response wrapper - removed JsonSerializable due to type parameter issues
class ApiResponse<T> {
  final bool success;
  final String? message;
  final T? data;
  final String? error;

  const ApiResponse({
    required this.success,
    this.message,
    this.data,
    this.error,
  });

  factory ApiResponse.fromJson(Map<String, dynamic> json, T Function(Object? json) fromJsonT) {
    return ApiResponse<T>(
      success: json['success'] as bool,
      message: json['message'] as String?,
      data: json['data'] != null ? fromJsonT(json['data']) : null,
      error: json['error'] as String?,
    );
  }

  Map<String, dynamic> toJson(Object? Function(T value) toJsonT) {
    return {
      'success': success,
      'message': message,
      'data': data != null ? toJsonT(data as T) : null,
      'error': error,
    };
  }
} 