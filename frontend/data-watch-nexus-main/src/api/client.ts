import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { API_BASE_URL, API_TIMEOUT, isDevelopment } from '@/config/env';

// API Response types
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  status?: string;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}

// Create axios instance with configuration
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Request interceptor to add auth token and logging
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Add authorization header
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Add request ID for tracking
    if (config.headers) {
      config.headers['X-Request-ID'] = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    // Log requests in development
    if (isDevelopment) {
      console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`, config);
    }

    return config;
  },
  (error: AxiosError) => {
    if (isDevelopment) {
      console.error('❌ Request Error:', error);
    }
    return Promise.reject(error);
  }
);

// Response interceptor for error handling and retry logic
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log successful responses in development
    if (isDevelopment) {
      console.log(`✅ API Response: ${response.status} ${response.config.method?.toUpperCase()} ${response.config.url}`);
    }
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    // Handle 401 Unauthorized - redirect to login
    if (error.response?.status === 401 && !originalRequest._retry) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');

      // Avoid redirect loop for auth endpoints
      if (!originalRequest.url?.includes('/auth/')) {
        window.location.href = '/login';
      }
    }

    // Handle 403 Forbidden
    if (error.response?.status === 403) {
      console.error('❌ Access Forbidden:', error.response.data);
    }

    // Handle 429 Too Many Requests - implement retry with backoff
    if (error.response?.status === 429 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Get retry-after header or default to 1 second
      const retryAfter = parseInt(error.response.headers['retry-after'] || '1', 10);

      if (isDevelopment) {
        console.log(`⏳ Rate limited. Retrying in ${retryAfter} seconds...`);
      }

      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      return apiClient(originalRequest);
    }

    // Handle network errors with retry
    if (!error.response && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isDevelopment) {
        console.log('🔄 Network error. Retrying...');
      }

      await new Promise(resolve => setTimeout(resolve, 1000));
      return apiClient(originalRequest);
    }

    // Log errors in development
    if (isDevelopment) {
      console.error('❌ API Error:', {
        status: error.response?.status,
        url: originalRequest.url,
        method: originalRequest.method,
        data: error.response?.data,
        message: error.message
      });
    }

    return Promise.reject(error);
  }
);

// Utility functions for common API operations
export const apiUtils = {
  // Format API errors for user display
  formatError: (error: AxiosError): string => {
    if (error.response?.data?.detail) {
      return error.response.data.detail;
    }

    if (error.response?.data?.message) {
      return error.response.data.message;
    }

    if (error.response?.status === 401) {
      return 'Please log in to continue.';
    }

    if (error.response?.status === 403) {
      return 'You do not have permission to perform this action.';
    }

    if (error.response?.status === 404) {
      return 'The requested resource was not found.';
    }

    if (error.response?.status === 429) {
      return 'Too many requests. Please try again later.';
    }

    if (error.response?.status >= 500) {
      return 'Server error. Please try again later.';
    }

    if (!error.response) {
      return 'Network error. Please check your connection.';
    }

    return 'An unexpected error occurred. Please try again.';
  },

  // Check if error is authentication related
  isAuthError: (error: AxiosError): boolean => {
    return error.response?.status === 401;
  },

  // Check if error is network related
  isNetworkError: (error: AxiosError): boolean => {
    return !error.response;
  },

  // Check if error should trigger retry
  shouldRetry: (error: AxiosError): boolean => {
    return !error.response || error.response.status >= 500;
  }
};