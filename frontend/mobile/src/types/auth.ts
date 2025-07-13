// Authentication related types matching backend schemas

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
  timezone?: string;
  language?: string;
  settings?: UserSettings;
}

export interface UserSettings {
  notifications: {
    daily_reminder: boolean;
    weekly_summary: boolean;
    mood_alerts: boolean;
    reminder_time: string;
  };
  privacy: {
    data_sharing: boolean;
    anonymous_analytics: boolean;
  };
  ui: {
    theme: string;
    font_size: string;
    animations: boolean;
  };
}

export interface UserResponse {
  user_id: number;
  name: string;
  email: string;
  registration_date: string; // ISO datetime string
  is_active: boolean;
  settings: { [key: string]: any };
  last_login?: string;
  timezone: string;
  language: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token?: string;
  user: UserResponse;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
  confirm_password: string;
}

export interface PasswordChange {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

// Default user settings
export const DEFAULT_USER_SETTINGS: UserSettings = {
  notifications: {
    daily_reminder: true,
    weekly_summary: true,
    mood_alerts: true,
    reminder_time: '09:00',
  },
  privacy: {
    data_sharing: false,
    anonymous_analytics: true,
  },
  ui: {
    theme: 'auto',
    font_size: 'medium',
    animations: true,
  },
};

// Legacy types for backward compatibility (to be removed)
export interface LoginRequest extends UserLogin {}
export interface RegisterRequest extends UserCreate {}
export interface AuthResponse extends TokenResponse {}
export interface User extends UserResponse {} 