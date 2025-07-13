import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';
import { 
  UserLogin, 
  UserCreate, 
  TokenResponse, 
  UserResponse,
  RefreshTokenRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  PasswordChange,
  // Legacy types for backward compatibility
  LoginRequest, 
  RegisterRequest, 
  AuthResponse, 
  User 
} from '@/types';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { STORAGE_KEYS } from '@/constants';

class AuthService {
  /**
   * Login user with email and password.
   */
  async login(credentials: UserLogin | LoginRequest): Promise<TokenResponse> {
    try {
      const response = await apiClient.post<TokenResponse>(
        API_ENDPOINTS.auth.login,
        credentials
      );
      
      // Set the token in the API client
      apiClient.setAuthToken(response.access_token);
      
      // Store tokens for persistence
      await AsyncStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, response.access_token);
      if (response.refresh_token) {
        await AsyncStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.refresh_token);
      }
      
      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Register new user.
   */
  async register(userData: UserCreate | RegisterRequest): Promise<TokenResponse> {
    try {
      const response = await apiClient.post<TokenResponse>(
        API_ENDPOINTS.auth.register,
        userData
      );
      
      // Set the token in the API client
      apiClient.setAuthToken(response.access_token);
      
      // Store tokens for persistence
      await AsyncStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, response.access_token);
      if (response.refresh_token) {
        await AsyncStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.refresh_token);
      }
      
      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Logout user.
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post(API_ENDPOINTS.auth.logout);
    } catch (error) {
      // Ignore logout errors, clear local state anyway
    } finally {
      // Clear tokens and local state
      apiClient.clearAuthToken();
      await AsyncStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
      await AsyncStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    }
  }

  /**
   * Get current user profile.
   */
  async getProfile(): Promise<UserResponse> {
    try {
      const response = await apiClient.get<UserResponse>(
        API_ENDPOINTS.auth.profile
      );
      return response;
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Refresh authentication token.
   */
  async refreshToken(): Promise<TokenResponse> {
    try {
      const refreshToken = await AsyncStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const request: RefreshTokenRequest = { refresh_token: refreshToken };
      const response = await apiClient.post<TokenResponse>(
        API_ENDPOINTS.auth.refresh,
        request
      );
      
      // Update stored tokens
      apiClient.setAuthToken(response.access_token);
      await AsyncStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, response.access_token);
      if (response.refresh_token) {
        await AsyncStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.refresh_token);
      }
      
      return response;
    } catch (error) {
      // If refresh fails, clear tokens
      await this.logout();
      throw this.handleAuthError(error);
    }
  }

  /**
   * Request password reset.
   */
  async forgotPassword(email: string): Promise<void> {
    try {
      const request: ForgotPasswordRequest = { email };
      await apiClient.post('/auth/forgot-password', request);
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Reset password with token.
   */
  async resetPassword(token: string, newPassword: string, confirmPassword: string): Promise<void> {
    try {
      const request: ResetPasswordRequest = {
        token,
        new_password: newPassword,
        confirm_password: confirmPassword,
      };
      await apiClient.post('/auth/reset-password', request);
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Change password for authenticated user.
   */
  async changePassword(currentPassword: string, newPassword: string, confirmPassword: string): Promise<void> {
    try {
      const request: PasswordChange = {
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
      };
      await apiClient.post('/auth/change-password', request);
    } catch (error) {
      throw this.handleAuthError(error);
    }
  }

  /**
   * Check if user is authenticated by verifying stored token.
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      const token = await AsyncStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
      if (!token) {
        return false;
      }

      // Set token and verify with a simple API call
      apiClient.setAuthToken(token);
      
      // Try to get profile to verify token is valid
      await this.getProfile();
      return true;
    } catch (error) {
      // Token is invalid, clear it
      await this.logout();
      return false;
    }
  }

  /**
   * Initialize auth state from stored tokens.
   */
  async initializeAuth(): Promise<TokenResponse | null> {
    try {
      const token = await AsyncStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
      if (!token) {
        return null;
      }

      apiClient.setAuthToken(token);
      
      // Verify token is still valid
      const user = await this.getProfile();
      
      return {
        access_token: token,
        token_type: 'bearer',
        expires_in: 3600, // Default expiry
        user,
      };
    } catch (error) {
      // Token is invalid, try to refresh
      try {
        return await this.refreshToken();
      } catch (refreshError) {
        // Both token and refresh failed, clear auth state
        await this.logout();
        return null;
      }
    }
  }

  /**
   * Handle authentication errors with consistent formatting.
   */
  private handleAuthError(error: any): Error {
    if (error.response?.data?.message) {
      return new Error(error.response.data.message);
    }
    if (error.message) {
      return new Error(error.message);
    }
    return new Error('Authentication failed');
  }

  /**
   * Register a new user.
   */
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>(
        API_ENDPOINTS.auth.register,
        userData
      );
      
      // Set the token in the API client
      apiClient.setAuthToken(response.accessToken);
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Refresh authentication token.
   */
  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>(
        API_ENDPOINTS.auth.refresh,
        { refreshToken }
      );
      
      // Update the token in the API client
      apiClient.setAuthToken(response.accessToken);
      
      return response;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get current user profile.
   */
  async getProfile(): Promise<User> {
    try {
      const user = await apiClient.get<User>(API_ENDPOINTS.auth.profile);
      return user;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Update user profile.
   */
  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const updatedUser = await apiClient.patch<User>(
        API_ENDPOINTS.auth.profile,
        userData
      );
      return updatedUser;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Logout user.
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post(API_ENDPOINTS.auth.logout);
      
      // Clear the token from the API client
      apiClient.clearAuthToken();
    } catch (error) {
      // Always clear token even if logout fails
      apiClient.clearAuthToken();
      throw error;
    }
  }

  /**
   * Change user password.
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      await apiClient.post(`${API_ENDPOINTS.auth.profile}/change-password`, {
        currentPassword,
        newPassword,
      });
    } catch (error) {
      throw error;
    }
  }

  /**
   * Request password reset.
   */
  async requestPasswordReset(email: string): Promise<void> {
    try {
      await apiClient.post('/auth/request-password-reset', { email });
    } catch (error) {
      throw error;
    }
  }

  /**
   * Reset password with token.
   */
  async resetPassword(token: string, newPassword: string): Promise<void> {
    try {
      await apiClient.post('/auth/reset-password', { token, newPassword });
    } catch (error) {
      throw error;
    }
  }

  /**
   * Verify email address.
   */
  async verifyEmail(token: string): Promise<void> {
    try {
      await apiClient.post('/auth/verify-email', { token });
    } catch (error) {
      throw error;
    }
  }

  /**
   * Resend email verification.
   */
  async resendEmailVerification(): Promise<void> {
    try {
      await apiClient.post('/auth/resend-verification');
    } catch (error) {
      throw error;
    }
  }
}

export const authService = new AuthService(); 