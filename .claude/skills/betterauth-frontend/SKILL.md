---
name: betterauth-frontend
description: Implement BetterAuth components in frontend applications with proper JWT handling, session management, and UI integration. Use this skill when setting up authentication in React/Next.js applications with BetterAuth. (Proficiency: B1 - Students can independently implement authentication components with guidance on security best practices)
---

# BetterAuth Frontend Implementation

## Overview

This skill provides guidance for implementing BetterAuth components in frontend applications. It covers JWT token handling, session management, UI integration, and proper security practices for React/Next.js applications.

### Proficiency Mapping (CEFR/Bloom's/DigComp Alignment)
- **Level**: B1 (Independent User / Applying Level)
- **Cognitive Load**: 4-5 concepts per step (auth service, API integration, protected routes, UI components, security)
- **Measurable Indicators**:
  - Student can independently create auth service with JWT handling
  - Student can implement protected routes with proper session management
  - Student can build secure login/register forms with validation
  - Student can integrate with backend authentication APIs
- **Prerequisites**: Basic knowledge of React/Next.js, HTTP protocols, JWT concepts

## When to Use This Skill

Use this skill when:
- Setting up authentication in React/Next.js applications using BetterAuth
- Implementing login/logout functionality with JWT tokens
- Creating protected routes and session management
- Building authentication UI components (login, register, profile)
- Integrating with backend authentication APIs
- Implementing proper error handling for authentication flows

### Required Clarifications

1. What specific authentication providers are you planning to use? (BetterAuth, social login, custom providers)
2. What frontend framework are you using? (React, Next.js, other)
3. What backend technology are you using with BetterAuth? (Node.js, Python, etc.)
4. Do you need social authentication (Google, GitHub, etc.) or just email/password?
5. What specific UI framework are you using? (Tailwind, Material UI, custom CSS)

### Optional Clarifications (if relevant)

6. Do you need refresh token functionality?
7. What specific error handling requirements do you have?
8. Do you need multi-factor authentication?
9. Are there specific compliance requirements (GDPR, CCPA, etc.)?
10. Do you need offline/cached authentication support?

Note: Ask clarifying questions before implementing to ensure the solution matches specific requirements.

## Prerequisites

Before implementing BetterAuth components:
1. BetterAuth backend is properly configured with JWT token issuance
2. Environment variables are set (BETTER_AUTH_SECRET, API endpoints)
3. Frontend project is set up with required dependencies (axios/fetch, react-router, etc.)
4. Backend API routes are available for authentication operations

## Implementation Steps

### 1. Set Up Authentication Service

Create an authentication service to handle JWT token operations:

```typescript
// frontend/src/services/auth-service.ts
interface AuthTokens {
  jwt_token?: string;
}

class AuthService {
  private tokenKey = 'betterauth_jwt';

  // Store JWT token from BetterAuth response
  setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  // Get stored JWT token
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  // Remove stored token on logout
  clearToken(): void {
    localStorage.removeItem(this.tokenKey);
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      // Decode JWT to check expiration
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch (e) {
      return false;
    }
  }

  // Add auth headers to API requests
  getAuthHeaders(): Record<string, string> {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
}

export const authService = new AuthService();
```

### 2. Create API Client with Auth Integration

Implement an API client that automatically includes authentication headers:

```typescript
// frontend/src/services/api-client.ts
import axios from 'axios';
import { authService } from './auth-service';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth headers
apiClient.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login on auth failure
      authService.clearToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### 3. Implement Protected Route Wrapper

Create a protected route component that checks authentication:

```tsx
// frontend/src/components/auth/ProtectedRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { authService } from '../services/auth-service';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  redirectTo = '/login'
}) => {
  const isAuthenticated = authService.isAuthenticated();

  return isAuthenticated ? <>{children}</> : <Navigate to={redirectTo} />;
};
```

### 4. Create Login Form Component

Build a login form with proper validation and error handling:

```tsx
// frontend/src/components/auth/LoginForm.tsx
import React, { useState } from 'react';
import { authService } from '../../services/auth-service';
import { apiClient } from '../../services/api-client';

interface LoginFormData {
  email: string;
  password: string;
}

export const LoginForm: React.FC<{ onSuccess?: () => void }> = ({ onSuccess }) => {
  const [formData, setFormData] = useState<LoginFormData>({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.post('/api/users/login', formData);

      // Store JWT token received from BetterAuth
      if (response.data.jwt_token) {
        authService.setToken(response.data.jwt_token);

        // Redirect or call success callback
        if (onSuccess) {
          onSuccess();
        } else {
          window.location.href = '/dashboard';
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-indigo-100">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">
        <div className="text-center mb-8">
          <div className="mx-auto h-12 w-12 bg-linear-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Welcome Back</h2>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <a href="#" className="text-sm text-blue-600 hover:text-blue-500 transition-colors">
                Forgot password?
              </a>
            </div>
            <input
              id="password"
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white"
              placeholder="••••••••"
            />
          </div>

          <div className="flex items-center">
            <input
              id="remember-me"
              type="checkbox"
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
              Remember me
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg text-white font-medium transition-all duration-200 ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-linear-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Signing in...
              </span>
            ) : (
              'Sign in'
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="/register" className="font-medium text-blue-600 hover:text-blue-500 transition-colors">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};
```

### 5. Create Registration Form Component

Build a registration form with validation and user feedback:

```tsx
// frontend/src/components/auth/RegisterForm.tsx
import React, { useState } from 'react';
import { authService } from '../../services/auth-service';
import { apiClient } from '../../services/api-client';

interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

export const RegisterForm: React.FC<{ onSuccess?: () => void }> = ({ onSuccess }) => {
  const [formData, setFormData] = useState<RegisterFormData>({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPasswordRequirements, setShowPasswordRequirements] = useState(false);

  const validatePassword = (password: string): boolean => {
    // Check for minimum requirements: 8 chars, uppercase, lowercase, number, special char
    const hasMinLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    return hasMinLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validate password requirements
    if (!validatePassword(formData.password)) {
      setError('Password must be at least 8 characters with uppercase, lowercase, number, and special character');
      setLoading(false);
      return;
    }

    // Validate password match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await apiClient.post('/api/users/register', {
        email: formData.email,
        password: formData.password,
        confirmPassword: formData.confirmPassword
      });

      // Store JWT token received from BetterAuth
      if (response.data.jwt_token) {
        authService.setToken(response.data.jwt_token);

        // Redirect or call success callback
        if (onSuccess) {
          onSuccess();
        } else {
          window.location.href = '/dashboard';
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-green-50 to-emerald-100">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">
        <div className="text-center mb-8">
          <div className="mx-auto h-12 w-12 bg-linear-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Create Account</h2>
          <p className="text-gray-600 mt-2">Join us to get started</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              onFocus={() => setShowPasswordRequirements(true)}
              onBlur={() => setShowPasswordRequirements(false)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white"
              placeholder="••••••••"
            />

            {showPasswordRequirements && (
              <div className="mt-2 text-xs text-gray-600 bg-gray-50 p-3 rounded-lg border">
                <p className="font-medium mb-1">Password must contain:</p>
                <ul className="space-y-1">
                  <li className="flex items-center">
                    <span className="mr-2">•</span>
                    Minimum 8 characters
                  </li>
                  <li className="flex items-center">
                    <span className="mr-2">•</span>
                    Uppercase letter (A-Z)
                  </li>
                  <li className="flex items-center">
                    <span className="mr-2">•</span>
                    Lowercase letter (a-z)
                  </li>
                  <li className="flex items-center">
                    <span className="mr-2">•</span>
                    Number (0-9)
                  </li>
                  <li className="flex items-center">
                    <span className="mr-2">•</span>
                    Special character (!@#$%^&*)
                  </li>
                </ul>
              </div>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              required
              value={formData.confirmPassword}
              onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-gray-50 focus:bg-white"
              placeholder="••••••••"
            />
          </div>

          <div className="flex items-start">
            <div className="flex items-center h-5">
              <input
                id="terms"
                aria-describedby="terms-description"
                name="terms"
                type="checkbox"
                required
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
            </div>
            <div className="ml-3 text-sm">
              <label htmlFor="terms" className="font-medium text-gray-700">
                I agree to the{' '}
                <a href="#" className="text-green-600 hover:text-green-500 transition-colors">
                  Terms and Conditions
                </a>
              </label>
              <p id="terms-description" className="text-gray-500">
                By creating an account, you agree to our privacy policy and terms of service.
              </p>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg text-white font-medium transition-all duration-200 ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-linear-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating account...
              </span>
            ) : (
              'Create account'
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <a href="/login" className="font-medium text-green-600 hover:text-green-500 transition-colors">
              Sign in
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};
```

### 6. Implement Logout Functionality

Create a logout function that properly clears the session:

```tsx
// frontend/src/components/auth/LogoutButton.tsx
import React from 'react';
import { authService } from '../../services/auth-service';

interface LogoutButtonProps {
  onLogout?: () => void;
}

export const LogoutButton: React.FC<LogoutButtonProps> = ({ onLogout }) => {
  const handleLogout = () => {
    // Clear authentication token
    authService.clearToken();

    // Call any additional logout logic
    if (onLogout) {
      onLogout();
    }

    // Redirect to login page
    window.location.href = '/login';
  };

  return (
    <button
      onClick={handleLogout}
      className="w-full flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
      </svg>
      Sign out
    </button>
  );
};
```

## Best Practices

### Security Considerations
- Store JWT tokens in localStorage or sessionStorage (avoid cookies for SPA)
- Implement token expiration checks
- Use HTTPS in production
- Sanitize user inputs
- Implement proper error handling

### Error Handling
- Handle authentication errors gracefully
- Implement token refresh mechanisms if needed
- Provide clear error messages to users
- Log authentication failures for monitoring

### UI/UX Guidelines
- Provide loading states during authentication operations
- Show clear feedback for success/error states
- Implement proper form validation
- Ensure responsive design for all auth components

## Testing

Always test the following scenarios:
- Successful login and registration
- Invalid credentials handling
- Token expiration handling
- Protected route access without authentication
- Logout functionality
- Form validation for registration

### Validation Checklist
- [ ] Authentication service properly stores/retrieves JWT tokens
- [ ] API client adds authentication headers automatically
- [ ] Protected routes redirect unauthenticated users
- [ ] Login form handles errors gracefully
- [ ] Registration form validates password requirements
- [ ] Logout clears all authentication tokens
- [ ] Token expiration is properly detected and handled
- [ ] Error messages are user-friendly but don't leak security details
- [ ] Loading states are properly displayed during auth operations
- [ ] All auth components are responsive across device sizes

## Documentation & References

### Official Documentation
| Resource | URL | Use For |
|----------|-----|---------|
| BetterAuth Official Docs | https://www.better-auth.com/docs | Authentication setup and configuration |
| JWT RFC 7519 | https://datatracker.ietf.org/doc/html/rfc7519 | JWT token specification |
| OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | Security best practices |
| React Router Docs | https://reactrouter.com/ | Protected route implementation |
| Axios Documentation | https://axios-http.com/ | HTTP client configuration |

### Additional Resources
- **React Authentication Patterns**: For understanding different authentication approaches in React
- **JWT Best Practices**: For secure token handling and storage
- **CORS Configuration**: For cross-origin authentication requests

## Validation and Coherence

### Proficiency Validation Tests
1. **Uniqueness**: Skill name is canonical and specific to BetterAuth frontend implementation
2. **Progression**: B1 level builds upon A1/A2 foundations (basic React/JS knowledge)
3. **Prerequisites**: Assumes basic knowledge of React/Next.js, HTTP, JWT concepts
4. **Connectivity**: Connects to backend auth services and security best practices
5. **Assessment**: Implementation can be validated through functional testing

### Coherence Checks
- Skill progresses logically from auth service setup → API integration → UI components → security
- Each step builds upon previous concepts without regression
- Security considerations are woven throughout rather than isolated

## Important Note

This skill requires access to up-to-date BetterAuth documentation. When implementing BetterAuth components:

1. **First priority**: Use the BetterAuth MCP Server to look up the latest documentation and API specifications
2. **Fallback**: If the BetterAuth MCP Server is not available, use the Context7 MCP Server to consult the most recent BetterAuth documentation
3. **Always**: Reference the most current documentation to ensure compatibility with the latest BetterAuth features and security practices

Consulting the latest documentation is necessary because authentication libraries evolve rapidly and security practices change over time. Using outdated implementation patterns could introduce security vulnerabilities.