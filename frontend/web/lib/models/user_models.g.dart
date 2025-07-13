// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

User _$UserFromJson(Map<String, dynamic> json) => User(
      userId: (json['user_id'] as num).toInt(),
      email: json['email'] as String,
      firstName: json['first_name'] as String,
      lastName: json['last_name'] as String,
      dateOfBirth: json['date_of_birth'] == null
          ? null
          : DateTime.parse(json['date_of_birth'] as String),
      timezone: json['timezone'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      isActive: json['is_active'] as bool? ?? true,
      profilePictureUrl: json['profile_picture_url'] as String?,
    );

Map<String, dynamic> _$UserToJson(User instance) => <String, dynamic>{
      'user_id': instance.userId,
      'email': instance.email,
      'first_name': instance.firstName,
      'last_name': instance.lastName,
      'date_of_birth': instance.dateOfBirth?.toIso8601String(),
      'timezone': instance.timezone,
      'created_at': instance.createdAt.toIso8601String(),
      'updated_at': instance.updatedAt.toIso8601String(),
      'is_active': instance.isActive,
      'profile_picture_url': instance.profilePictureUrl,
    };

UserCreate _$UserCreateFromJson(Map<String, dynamic> json) => UserCreate(
      email: json['email'] as String,
      password: json['password'] as String,
      firstName: json['first_name'] as String,
      lastName: json['last_name'] as String,
      dateOfBirth: json['date_of_birth'] == null
          ? null
          : DateTime.parse(json['date_of_birth'] as String),
      timezone: json['timezone'] as String?,
    );

Map<String, dynamic> _$UserCreateToJson(UserCreate instance) =>
    <String, dynamic>{
      'email': instance.email,
      'password': instance.password,
      'first_name': instance.firstName,
      'last_name': instance.lastName,
      'date_of_birth': instance.dateOfBirth?.toIso8601String(),
      'timezone': instance.timezone,
    };

UserLogin _$UserLoginFromJson(Map<String, dynamic> json) => UserLogin(
      email: json['email'] as String,
      password: json['password'] as String,
    );

Map<String, dynamic> _$UserLoginToJson(UserLogin instance) => <String, dynamic>{
      'email': instance.email,
      'password': instance.password,
    };

TokenResponse _$TokenResponseFromJson(Map<String, dynamic> json) =>
    TokenResponse(
      accessToken: json['access_token'] as String,
      refreshToken: json['refresh_token'] as String?,
      tokenType: json['token_type'] as String? ?? 'Bearer',
      expiresIn: (json['expires_in'] as num?)?.toInt(),
      user: User.fromJson(json['user'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$TokenResponseToJson(TokenResponse instance) =>
    <String, dynamic>{
      'access_token': instance.accessToken,
      'refresh_token': instance.refreshToken,
      'token_type': instance.tokenType,
      'expires_in': instance.expiresIn,
      'user': instance.user,
    };

UserUpdate _$UserUpdateFromJson(Map<String, dynamic> json) => UserUpdate(
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      dateOfBirth: json['date_of_birth'] == null
          ? null
          : DateTime.parse(json['date_of_birth'] as String),
      timezone: json['timezone'] as String?,
      profilePictureUrl: json['profile_picture_url'] as String?,
    );

Map<String, dynamic> _$UserUpdateToJson(UserUpdate instance) =>
    <String, dynamic>{
      'first_name': instance.firstName,
      'last_name': instance.lastName,
      'date_of_birth': instance.dateOfBirth?.toIso8601String(),
      'timezone': instance.timezone,
      'profile_picture_url': instance.profilePictureUrl,
    };

PasswordChange _$PasswordChangeFromJson(Map<String, dynamic> json) =>
    PasswordChange(
      currentPassword: json['current_password'] as String,
      newPassword: json['new_password'] as String,
    );

Map<String, dynamic> _$PasswordChangeToJson(PasswordChange instance) =>
    <String, dynamic>{
      'current_password': instance.currentPassword,
      'new_password': instance.newPassword,
    };

PasswordReset _$PasswordResetFromJson(Map<String, dynamic> json) =>
    PasswordReset(
      email: json['email'] as String,
    );

Map<String, dynamic> _$PasswordResetToJson(PasswordReset instance) =>
    <String, dynamic>{
      'email': instance.email,
    };

PasswordResetConfirm _$PasswordResetConfirmFromJson(
        Map<String, dynamic> json) =>
    PasswordResetConfirm(
      token: json['token'] as String,
      newPassword: json['new_password'] as String,
    );

Map<String, dynamic> _$PasswordResetConfirmToJson(
        PasswordResetConfirm instance) =>
    <String, dynamic>{
      'token': instance.token,
      'new_password': instance.newPassword,
    };

UserPreferences _$UserPreferencesFromJson(Map<String, dynamic> json) =>
    UserPreferences(
      userId: (json['user_id'] as num).toInt(),
      themeMode: json['theme_mode'] as String? ?? 'system',
      notificationEnabled: json['notification_enabled'] as bool? ?? true,
      checkinReminderTime: json['checkin_reminder_time'] as String?,
      dataSharingEnabled: json['data_sharing_enabled'] as bool? ?? false,
      analyticsEnabled: json['analytics_enabled'] as bool? ?? true,
    );

Map<String, dynamic> _$UserPreferencesToJson(UserPreferences instance) =>
    <String, dynamic>{
      'user_id': instance.userId,
      'theme_mode': instance.themeMode,
      'notification_enabled': instance.notificationEnabled,
      'checkin_reminder_time': instance.checkinReminderTime,
      'data_sharing_enabled': instance.dataSharingEnabled,
      'analytics_enabled': instance.analyticsEnabled,
    };
