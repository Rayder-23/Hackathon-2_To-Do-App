/**
 * BetterAuth integration service for handling authentication operations in the frontend
 * This service works with BetterAuth to manage user sessions and JWT tokens for backend API access
 */

import { createAuthClient } from 'better-auth/react';
import { jwtClient } from 'better-auth/client/plugins';

// Initialize BetterAuth client with JWT plugin for backend API authentication
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000',
  plugins: [
    jwtClient()  // This plugin enables JWT token retrieval for backend API authentication
  ]
});

// Type definitions
interface UserCredentials {
  email: string;
  password: string;
}

interface RegisterData extends UserCredentials {
  confirmPassword?: string;
}

interface BetterAuthUser {
  id: string;
  email: string;
  name?: string;
}

/**
 * BetterAuth Service Class
 * Handles integration between BetterAuth frontend authentication and backend API authentication
 */
class BetterAuthService {
  private BACKEND_API_URL: string = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  /**
   * Register a new user using BetterAuth
   */
  async register(userData: RegisterData): Promise<{user: BetterAuthUser, jwt: string}> {
    // Basic validation
    if (!userData.email || !userData.password) {
      throw new Error('Email and password are required');
    }

    if (userData.password !== userData.confirmPassword) {
      throw new Error('Passwords do not match');
    }

    try {
      // Use BetterAuth to register the user
      const result = await authClient.signUp.email({
        email: userData.email,
        password: userData.password,
        name: userData.email.split('@')[0] // Use part of email as name
      });

      if (!result || result.error) {
        throw new Error(result?.error?.message || 'Registration failed');
      }

      // Get JWT token for backend API authentication
      const jwtResult = await authClient.token();
      if (!jwtResult || jwtResult.error) {
        throw new Error(jwtResult?.error?.message || 'Failed to get authentication token');
      }

      return {
        user: result.data.user,
        jwt: jwtResult.data.token
      };
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  /**
   * Login a user using BetterAuth
   */
  async login(credentials: UserCredentials): Promise<{user: BetterAuthUser, jwt: string}> {
    try {
      // Use BetterAuth to authenticate the user
      const result = await authClient.signIn.email({
        email: credentials.email,
        password: credentials.password,
      });

      if (!result || result.error) {
        throw new Error(result?.error?.message || 'Login failed');
      }

      // Get JWT token for backend API authentication
      const jwtResult = await authClient.token();
      if (!jwtResult || jwtResult.error) {
        throw new Error(jwtResult?.error?.message || 'Failed to get authentication token');
      }

      return {
        user: result.data.user,
        jwt: jwtResult.data.token
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Logout the current user
   */
  async logout(): Promise<void> {
    try {
      await authClient.signOut();
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  /**
   * Check if the user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      const session = await authClient.getSession();
      return !!session?.data?.user;
    } catch (error) {
      console.error('Session check error:', error);
      return false;
    }
  }

  /**
   * Get the current user
   */
  async getCurrentUser(): Promise<BetterAuthUser | null> {
    try {
      const session = await authClient.getSession();
      return session?.data?.user || null;
    } catch (error) {
      console.error('Get user error:', error);
      return null;
    }
  }

  /**
   * Get JWT token for backend API calls
   */
  async getJWTToken(): Promise<string | null> {
    try {
      const result = await authClient.token();
      return result?.data?.token || null;
    } catch (error) {
      console.error('Get JWT token error:', error);
      return null;
    }
  }

  /**
   * Parse JWT token to extract payload
   */
  parseJwt(token: string): any {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));

      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Error parsing JWT:', error);
      throw new Error('Invalid JWT token');
    }
  }

  /**
   * Make authenticated API request to backend
   */
  async authenticatedRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getJWTToken();

    if (!token) {
      throw new Error('User not authenticated');
    }

    const url = `${this.BACKEND_API_URL}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Session might be invalid, clear local session
        await this.logout();
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API request failed: ${response.status}`);
    }

    return response.json();
  }
}

export const betterAuthService = new BetterAuthService();
export type { UserCredentials, RegisterData, BetterAuthUser };