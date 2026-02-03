/**
 * Centralized API Service Layer
 * Handles all API interactions with proper error handling, authentication, and environment configuration
 */

import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

// Environment configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const API_TIMEOUT = 30000; // 30 seconds

// API Response types
export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  totalPages: number;
  hasMore: boolean;
}

export interface ApiError {
  message: string;
  code: string;
  details?: any;
}

// User types
export interface User {
  id: string;
  email: string;
  name: string;
  firstName?: string;
  lastName?: string;
  phone?: string;
  bio?: string;
  profilePicture?: string;
  resumeUrl?: string;
  linkedinUrl?: string;
  githubUrl?: string;
  skills?: string[];
  preferences?: {
    locations?: string[];
    jobTypes?: string[];
    salaryMin?: number;
    remoteOk?: boolean;
  };
  profileCompleteness?: number;
  isActive: boolean;
  createdAt: string;
  lastLogin?: string;
}

// Job types
export interface Job {
  id: string;
  title: string;
  company: string;
  companyLogo?: string;
  location: string;
  type: string;
  remote: boolean;
  salary?: {
    min: number;
    max: number;
    currency: string;
  };
  description: string;
  requirements: string[];
  benefits: string[];
  tags: string[];
  postedDate: string;
  expiryDate?: string;
  applicationUrl?: string;
  applyEmail?: string;
  featured: boolean;
  saved?: boolean;
  viewCount?: number;
  applicationCount?: number;
}

// Job application types
export interface JobApplication {
  id: string;
  jobId: string;
  userId: string;
  status: 'applied' | 'under_review' | 'interview_scheduled' | 'rejected' | 'accepted' | 'withdrawn';
  coverLetter?: string;
  expectedSalary?: number;
  resumeUrl?: string;
  appliedAt: string;
  updatedAt: string;
  job?: Job;
}

// Notification types
export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'job_alert' | 'application_update' | 'system' | 'marketing';
  isRead: boolean;
  actionUrl?: string;
  createdAt: string;
  metadata?: any;
}

// Filter types
export interface JobFilters {
  search?: string;
  location?: string;
  type?: string;
  remote?: boolean;
  salaryMin?: number;
  salaryMax?: number;
  skills?: string[];
  page?: number;
  limit?: number;
}

export interface ApplicationFilters {
  status?: string;
  page?: number;
  limit?: number;
}

/**
 * Main API Service Class
 */
class ApiService {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    this.setupInterceptors();
    this.loadToken();
  }

  private setupInterceptors() {
    // Request interceptor - Add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - Handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(this.handleApiError(error));
      }
    );
  }

  private loadToken() {
    this.token = localStorage.getItem('token');
  }

  private setToken(token: string) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  private clearToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  private handleApiError(error: AxiosError): ApiError {
    if (error.response) {
      // Server responded with error status
      const data = error.response.data as any;
      return {
        message: data?.detail || data?.message || 'An error occurred',
        code: error.response.status.toString(),
        details: data,
      };
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'Network error - please check your connection',
        code: 'NETWORK_ERROR',
        details: error.request,
      };
    } else {
      // Something else happened
      return {
        message: error.message || 'An unexpected error occurred',
        code: 'UNKNOWN_ERROR',
        details: error,
      };
    }
  }

  // ============ AUTHENTICATION APIs ============

  async register(data: { email: string; password: string; name: string }): Promise<User> {
    const response = await this.client.post('/auth/register', data);
    const { token, user } = response.data;
    this.setToken(token);
    return user;
  }

  async login(data: { email: string; password: string }): Promise<User> {
    const response = await this.client.post('/auth/login', data);
    const { token, user } = response.data;
    this.setToken(token);
    return user;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  logout() {
    this.clearToken();
  }

  // ============ JOB APIs ============

  async getJobs(filters: JobFilters = {}): Promise<PaginatedResponse<Job>> {
    const params = new URLSearchParams();

    if (filters.search) params.append('search', filters.search);
    if (filters.location) params.append('location', filters.location);
    if (filters.type) params.append('type', filters.type);
    if (filters.remote !== undefined) params.append('remote', filters.remote.toString());
    if (filters.salaryMin) params.append('salary_min', filters.salaryMin.toString());
    if (filters.salaryMax) params.append('salary_max', filters.salaryMax.toString());
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.limit) params.append('limit', filters.limit.toString());

    const response = await this.client.get(`/jobs/?${params.toString()}`);
    const data = response.data;

    return {
      data: data.jobs,
      total: data.total,
      page: data.page,
      totalPages: data.totalPages,
      hasMore: data.page < data.totalPages,
    };
  }

  async getJob(jobId: string): Promise<Job> {
    const response = await this.client.get(`/jobs/${jobId}`);
    return response.data;
  }

  async saveJob(jobId: string): Promise<void> {
    await this.client.post('/jobs/save', { job_id: jobId });
  }

  async unsaveJob(jobId: string): Promise<void> {
    await this.client.delete(`/jobs/${jobId}/save`);
  }

  async getSavedJobs(): Promise<Job[]> {
    const response = await this.client.get('/jobs/saved/list');
    return response.data;
  }

  async getJobCategories(): Promise<string[]> {
    const response = await this.client.get('/jobs/meta/categories');
    return response.data;
  }

  async getJobTypes(): Promise<string[]> {
    const response = await this.client.get('/jobs/meta/types');
    return response.data;
  }

  // ============ JOB APPLICATION APIs ============

  async applyForJob(jobId: string, data: {
    coverLetter?: string;
    expectedSalary?: number;
    resumeUrl?: string;
  }): Promise<JobApplication> {
    const response = await this.client.post(`/jobs/${jobId}/apply`, data);
    return response.data;
  }

  async getMyApplications(filters: ApplicationFilters = {}): Promise<PaginatedResponse<JobApplication>> {
    const params = new URLSearchParams();

    if (filters.status) params.append('status', filters.status);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.limit) params.append('limit', filters.limit.toString());

    const response = await this.client.get(`/applications/?${params.toString()}`);
    const data = response.data;

    return {
      data: data.applications,
      total: data.total,
      page: data.page,
      totalPages: data.totalPages,
      hasMore: data.page < data.totalPages,
    };
  }

  async getApplication(applicationId: string): Promise<JobApplication> {
    const response = await this.client.get(`/applications/${applicationId}`);
    return response.data;
  }

  async withdrawApplication(applicationId: string): Promise<void> {
    await this.client.post(`/applications/${applicationId}/withdraw`);
  }

  // ============ RECOMMENDATION APIs ============

  async getJobRecommendations(limit: number = 10): Promise<Job[]> {
    const response = await this.client.get(`/recommendations/jobs?limit=${limit}`);
    return response.data.recommendations || [];
  }

  async getTrendingJobs(limit: number = 10): Promise<Job[]> {
    const response = await this.client.get(`/recommendations/trending?limit=${limit}`);
    return response.data.jobs || [];
  }

  async submitRecommendationFeedback(recommendationId: string, feedback: 'helpful' | 'not_helpful'): Promise<void> {
    await this.client.post('/recommendations/feedback', {
      recommendation_id: recommendationId,
      feedback,
    });
  }

  // ============ USER PROFILE APIs ============

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await this.client.put('/users/profile', data);
    return response.data;
  }

  async updateUserPreferences(preferences: any): Promise<User> {
    const response = await this.client.put('/users/preferences', { preferences });
    return response.data;
  }

  async uploadResume(file: File): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append('resume', file);

    const response = await this.client.post('/users/upload-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // ============ NOTIFICATION APIs ============

  async getNotifications(includeRead: boolean = true, limit: number = 50): Promise<{
    notifications: Notification[];
    total: number;
    unreadCount: number;
  }> {
    const response = await this.client.get(`/notifications/?include_read=${includeRead}&limit=${limit}`);
    return response.data;
  }

  async markNotificationRead(notificationId: string): Promise<void> {
    await this.client.put(`/notifications/${notificationId}/read`);
  }

  async getUnreadNotificationCount(): Promise<number> {
    const response = await this.client.get('/notifications/unread/count');
    return response.data.unread_count;
  }

  // ============ ANALYTICS APIs ============

  async trackJobView(jobId: string): Promise<void> {
    try {
      await this.client.post('/analytics/job-view', { job_id: jobId });
    } catch (error) {
      // Non-critical - don't fail if analytics fails
      console.warn('Failed to track job view:', error);
    }
  }

  async trackSearch(query: string, filters: any): Promise<void> {
    try {
      await this.client.post('/analytics/search', { query, filters });
    } catch (error) {
      console.warn('Failed to track search:', error);
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export types
export type { ApiService };
