/**
 * API client for interacting with the Todo App backend
 */

interface ApiOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: any;
}

class ApiClient {
  private BASE_URL: string = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  private AUTH_HEADER = 'Authorization';

  /**
   * Make an API request
   */
  async request(endpoint: string, options: ApiOptions = {}): Promise<any> {
    const url = `${this.BASE_URL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add authorization header if token exists
    const authToken = await this.getAuthToken();
    if (authToken) {
      (headers as Record<string, string>)[this.AUTH_HEADER] = `Bearer ${authToken}`;
    }

    const config: RequestInit = {
      method: options.method || 'GET',
      headers,
    };

    if (options.body) {
      config.body = typeof options.body === 'string' ? options.body : JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);

      // Handle RFC 7807 Problem Details for error responses
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        // If it's a Problem Details response, use its details
        if (errorData.title && errorData.status) {
          throw {
            type: 'problem_details',
            title: errorData.title,
            status: errorData.status,
            detail: errorData.detail || errorData.detail,
            instance: errorData.instance,
          };
        }

        // Otherwise, use generic error
        const errorMessage = `HTTP ${response.status}: ${errorData.detail || response.statusText}`;
        throw {
          type: 'generic_error',
          status: response.status,
          message: errorMessage,
          detail: errorData.detail || response.statusText,
        };
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${url}`, error);

      // Re-throw the error in a consistent format
      if (typeof error === 'object' && error !== null && 'type' in error) {
        throw error;
      } else {
        throw {
          type: 'network_error',
          message: error instanceof Error ? error.message : 'Network request failed',
        };
      }
    }
  }

  /**
   * Get the auth token from BetterAuth service
   */
  private async getAuthToken(): Promise<string | null> {
    // Use BetterAuth service to get JWT token
    const { betterAuthService } = await import('@/services/auth-service');
    return betterAuthService.getJWTToken();
  }

  /**
   * User-related API methods
   */
  async register(userData: { email: string; password: string }): Promise<any> {
    return this.request('/api/users/register', {
      method: 'POST',
      body: userData,
    });
  }

  async login(credentials: { email: string; password: string }): Promise<any> {
    return this.request('/api/users/login', {
      method: 'POST',
      body: credentials,
    });
  }

  /**
   * Task-related API methods
   */
  async getTasks(userId: number): Promise<any[]> {
    return this.request(`/api/${userId}/tasks`);
  }

  async createTask(userId: number, taskData: { title: string; description?: string }): Promise<any> {
    return this.request(`/api/${userId}/tasks`, {
      method: 'POST',
      body: taskData,
    });
  }

  async updateTask(userId: number, taskId: number, taskData: { title?: string; description?: string; completed?: boolean }): Promise<any> {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: taskData,
    });
  }

  async deleteTask(userId: number, taskId: number): Promise<any> {
    return this.request(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(userId: number, taskId: number): Promise<any> {
    return this.request(`/api/${userId}/tasks/${taskId}/toggle`, {
      method: 'PATCH',
    });
  }

  async getDeletedTasks(userId: number): Promise<any[]> {
    return this.request(`/api/${userId}/tasks/deleted`);
  }
}

export const apiClient = new ApiClient();