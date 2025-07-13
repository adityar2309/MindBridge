import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '@/constants';
import { LoginRequest, RegisterRequest, AuthResponse, User } from '@/types';

class AuthService {
  /**
   * Login user with email and password.
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>(
        API_ENDPOINTS.auth.login,
        credentials
      );
      
      // Set the token in the API client
      apiClient.setAuthToken(response.accessToken);
      
      return response;
    } catch (error) {
      throw error;
    }
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