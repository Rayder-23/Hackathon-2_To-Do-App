/**
 * Type definitions for the Todo App
 */

export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  status: number;
  title: string;
  detail: string;
}