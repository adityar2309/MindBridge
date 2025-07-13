// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserLogin _$UserLoginFromJson(Map<String, dynamic> json) => UserLogin(
      email: json['email'] as String,
      password: json['password'] as String,
    );

Map<String, dynamic> _$UserLoginToJson(UserLogin instance) => <String, dynamic>{
      'email': instance.email,
      'password': instance.password,
    };

UserCreate _$UserCreateFromJson(Map<String, dynamic> json) => UserCreate(
      name: json['name'] as String,
      email: json['email'] as String,
      password: json['password'] as String,
      timezone: json['timezone'] as String? ?? 'UTC',
      language: json['language'] as String? ?? 'en',
      settings: json['settings'] == null
          ? null
          : UserSettings.fromJson(json['settings'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$UserCreateToJson(UserCreate instance) =>
    <String, dynamic>{
      'name': instance.name,
      'email': instance.email,
      'password': instance.password,
      'timezone': instance.timezone,
      'language': instance.language,
      'settings': instance.settings,
    };

UserSettings _$UserSettingsFromJson(Map<String, dynamic> json) => UserSettings(
      notifications: json['notifications'] as Map<String, dynamic>,
      privacy: json['privacy'] as Map<String, dynamic>,
      ui: json['ui'] as Map<String, dynamic>,
    );

Map<String, dynamic> _$UserSettingsToJson(UserSettings instance) =>
    <String, dynamic>{
      'notifications': instance.notifications,
      'privacy': instance.privacy,
      'ui': instance.ui,
    };

UserResponse _$UserResponseFromJson(Map<String, dynamic> json) => UserResponse(
      userId: (json['user_id'] as num).toInt(),
      name: json['name'] as String,
      email: json['email'] as String,
      registrationDate: DateTime.parse(json['registration_date'] as String),
      isActive: json['is_active'] as bool,
      settings: json['settings'] as Map<String, dynamic>,
      lastLogin: json['last_login'] == null
          ? null
          : DateTime.parse(json['last_login'] as String),
      timezone: json['timezone'] as String,
      language: json['language'] as String,
    );

Map<String, dynamic> _$UserResponseToJson(UserResponse instance) =>
    <String, dynamic>{
      'user_id': instance.userId,
      'name': instance.name,
      'email': instance.email,
      'registration_date': instance.registrationDate.toIso8601String(),
      'is_active': instance.isActive,
      'settings': instance.settings,
      'last_login': instance.lastLogin?.toIso8601String(),
      'timezone': instance.timezone,
      'language': instance.language,
    };

TokenResponse _$TokenResponseFromJson(Map<String, dynamic> json) =>
    TokenResponse(
      accessToken: json['access_token'] as String,
      tokenType: json['token_type'] as String? ?? 'bearer',
      expiresIn: (json['expires_in'] as num).toInt(),
      refreshToken: json['refresh_token'] as String?,
      user: UserResponse.fromJson(json['user'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$TokenResponseToJson(TokenResponse instance) =>
    <String, dynamic>{
      'access_token': instance.accessToken,
      'token_type': instance.tokenType,
      'expires_in': instance.expiresIn,
      'refresh_token': instance.refreshToken,
      'user': instance.user,
    };

RefreshTokenRequest _$RefreshTokenRequestFromJson(Map<String, dynamic> json) =>
    RefreshTokenRequest(
      refreshToken: json['refresh_token'] as String,
    );

Map<String, dynamic> _$RefreshTokenRequestToJson(
        RefreshTokenRequest instance) =>
    <String, dynamic>{
      'refresh_token': instance.refreshToken,
    };

ForgotPasswordRequest _$ForgotPasswordRequestFromJson(
        Map<String, dynamic> json) =>
    ForgotPasswordRequest(
      email: json['email'] as String,
    );

Map<String, dynamic> _$ForgotPasswordRequestToJson(
        ForgotPasswordRequest instance) =>
    <String, dynamic>{
      'email': instance.email,
    };

ResetPasswordRequest _$ResetPasswordRequestFromJson(
        Map<String, dynamic> json) =>
    ResetPasswordRequest(
      token: json['token'] as String,
      newPassword: json['new_password'] as String,
      confirmPassword: json['confirm_password'] as String,
    );

Map<String, dynamic> _$ResetPasswordRequestToJson(
        ResetPasswordRequest instance) =>
    <String, dynamic>{
      'token': instance.token,
      'new_password': instance.newPassword,
      'confirm_password': instance.confirmPassword,
    };

PasswordChange _$PasswordChangeFromJson(Map<String, dynamic> json) =>
    PasswordChange(
      currentPassword: json['current_password'] as String,
      newPassword: json['new_password'] as String,
      confirmPassword: json['confirm_password'] as String,
    );

Map<String, dynamic> _$PasswordChangeToJson(PasswordChange instance) =>
    <String, dynamic>{
      'current_password': instance.currentPassword,
      'new_password': instance.newPassword,
      'confirm_password': instance.confirmPassword,
    };
