import 'package:json_annotation/json_annotation.dart';

part 'user_models.g.dart';

@JsonSerializable()
class User {
  @JsonKey(name: 'user_id')
  final int userId;
  
  final String email;
  
  @JsonKey(name: 'first_name')
  final String firstName;
  
  @JsonKey(name: 'last_name') 
  final String lastName;
  
  @JsonKey(name: 'date_of_birth')
  final DateTime? dateOfBirth;
  
  final String? timezone;
  
  @JsonKey(name: 'created_at')
  final DateTime createdAt;
  
  @JsonKey(name: 'updated_at')
  final DateTime updatedAt;
  
  @JsonKey(name: 'is_active')
  final bool isActive;
  
  @JsonKey(name: 'profile_picture_url')
  final String? profilePictureUrl;

  const User({
    required this.userId,
    required this.email,
    required this.firstName,
    required this.lastName,
    this.dateOfBirth,
    this.timezone,
    required this.createdAt,
    required this.updatedAt,
    this.isActive = true,
    this.profilePictureUrl,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);

  String get fullName => '$firstName $lastName';
  
  User copyWith({
    int? userId,
    String? email,
    String? firstName,
    String? lastName,
    DateTime? dateOfBirth,
    String? timezone,
    DateTime? createdAt,
    DateTime? updatedAt,
    bool? isActive,
    String? profilePictureUrl,
  }) {
    return User(
      userId: userId ?? this.userId,
      email: email ?? this.email,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      dateOfBirth: dateOfBirth ?? this.dateOfBirth,
      timezone: timezone ?? this.timezone,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      isActive: isActive ?? this.isActive,
      profilePictureUrl: profilePictureUrl ?? this.profilePictureUrl,
    );
  }
}

@JsonSerializable()
class UserCreate {
  final String email;
  final String password;
  
  @JsonKey(name: 'first_name')
  final String firstName;
  
  @JsonKey(name: 'last_name')
  final String lastName;
  
  @JsonKey(name: 'date_of_birth')
  final DateTime? dateOfBirth;
  
  final String? timezone;

  const UserCreate({
    required this.email,
    required this.password,
    required this.firstName,
    required this.lastName,
    this.dateOfBirth,
    this.timezone,
  });

  factory UserCreate.fromJson(Map<String, dynamic> json) => _$UserCreateFromJson(json);
  Map<String, dynamic> toJson() => _$UserCreateToJson(this);
}

@JsonSerializable()
class UserLogin {
  final String email;
  final String password;

  const UserLogin({
    required this.email,
    required this.password,
  });

  factory UserLogin.fromJson(Map<String, dynamic> json) => _$UserLoginFromJson(json);
  Map<String, dynamic> toJson() => _$UserLoginToJson(this);
}

@JsonSerializable()
class TokenResponse {
  @JsonKey(name: 'access_token')
  final String accessToken;
  
  @JsonKey(name: 'refresh_token')
  final String? refreshToken;
  
  @JsonKey(name: 'token_type')
  final String tokenType;
  
  @JsonKey(name: 'expires_in')
  final int? expiresIn;
  
  final User user;

  const TokenResponse({
    required this.accessToken,
    this.refreshToken,
    this.tokenType = 'Bearer',
    this.expiresIn,
    required this.user,
  });

  factory TokenResponse.fromJson(Map<String, dynamic> json) => _$TokenResponseFromJson(json);
  Map<String, dynamic> toJson() => _$TokenResponseToJson(this);
}

@JsonSerializable()
class UserUpdate {
  @JsonKey(name: 'first_name')
  final String? firstName;
  
  @JsonKey(name: 'last_name')
  final String? lastName;
  
  @JsonKey(name: 'date_of_birth')
  final DateTime? dateOfBirth;
  
  final String? timezone;
  
  @JsonKey(name: 'profile_picture_url')
  final String? profilePictureUrl;

  const UserUpdate({
    this.firstName,
    this.lastName,
    this.dateOfBirth,
    this.timezone,
    this.profilePictureUrl,
  });

  factory UserUpdate.fromJson(Map<String, dynamic> json) => _$UserUpdateFromJson(json);
  Map<String, dynamic> toJson() => _$UserUpdateToJson(this);
}

@JsonSerializable()
class PasswordChange {
  @JsonKey(name: 'current_password')
  final String currentPassword;
  
  @JsonKey(name: 'new_password')
  final String newPassword;

  const PasswordChange({
    required this.currentPassword,
    required this.newPassword,
  });

  factory PasswordChange.fromJson(Map<String, dynamic> json) => _$PasswordChangeFromJson(json);
  Map<String, dynamic> toJson() => _$PasswordChangeToJson(this);
}

@JsonSerializable()
class PasswordReset {
  final String email;

  const PasswordReset({
    required this.email,
  });

  factory PasswordReset.fromJson(Map<String, dynamic> json) => _$PasswordResetFromJson(json);
  Map<String, dynamic> toJson() => _$PasswordResetToJson(this);
}

@JsonSerializable()
class PasswordResetConfirm {
  final String token;
  
  @JsonKey(name: 'new_password')
  final String newPassword;

  const PasswordResetConfirm({
    required this.token,
    required this.newPassword,
  });

  factory PasswordResetConfirm.fromJson(Map<String, dynamic> json) => _$PasswordResetConfirmFromJson(json);
  Map<String, dynamic> toJson() => _$PasswordResetConfirmToJson(this);
}

// User preferences and settings
@JsonSerializable()
class UserPreferences {
  @JsonKey(name: 'user_id')
  final int userId;
  
  @JsonKey(name: 'theme_mode')
  final String themeMode; // 'light', 'dark', 'system'
  
  @JsonKey(name: 'notification_enabled')
  final bool notificationEnabled;
  
  @JsonKey(name: 'checkin_reminder_time')
  final String? checkinReminderTime; // HH:MM format
  
  @JsonKey(name: 'data_sharing_enabled')
  final bool dataSharingEnabled;
  
  @JsonKey(name: 'analytics_enabled')
  final bool analyticsEnabled;

  const UserPreferences({
    required this.userId,
    this.themeMode = 'system',
    this.notificationEnabled = true,
    this.checkinReminderTime,
    this.dataSharingEnabled = false,
    this.analyticsEnabled = true,
  });

  factory UserPreferences.fromJson(Map<String, dynamic> json) => _$UserPreferencesFromJson(json);
  Map<String, dynamic> toJson() => _$UserPreferencesToJson(this);

  UserPreferences copyWith({
    int? userId,
    String? themeMode,
    bool? notificationEnabled,
    String? checkinReminderTime,
    bool? dataSharingEnabled,
    bool? analyticsEnabled,
  }) {
    return UserPreferences(
      userId: userId ?? this.userId,
      themeMode: themeMode ?? this.themeMode,
      notificationEnabled: notificationEnabled ?? this.notificationEnabled,
      checkinReminderTime: checkinReminderTime ?? this.checkinReminderTime,
      dataSharingEnabled: dataSharingEnabled ?? this.dataSharingEnabled,
      analyticsEnabled: analyticsEnabled ?? this.analyticsEnabled,
    );
  }
} 