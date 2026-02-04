/**
 * Jobs API service
 */

import { apiClient, ApiResponse } from '@/api/client';

export interface JobFilters {
  search?: string;
  location?: string;
  type?: string;
  remote?: boolean;
  salary_min?: number;
  salary_max?: number;
  page?: number;
  limit?: number;
}

export interface Salary {
  min?: number;
  max?: number;
  currency: string;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  company_logo?: string;
  location: string;
  type: string;
  remote: boolean;
  salary?: Salary;
  description: string;
  requirements: string[];
  benefits: string[];
  tags: string[];
  posted_date: string;
  expiry_date?: string;
  application_url?: string;
  apply_email?: string;
  featured: boolean;
  saved?: boolean;
}

export interface JobsResponse {
  jobs: Job[];
  total: number;
  page: number;
  total_pages: number;
}

export interface JobApplicationRequest {
  cover_letter?: string;
  expected_salary?: number;
  resume_url?: string;
}

export interface JobApplication {
  id: number;
  job_id: string;
  user_id: string;
  status: string;
  applied_at: string;
  cover_letter?: string;
  expected_salary?: number;
  resume_url?: string;
}

export const jobsService = {
  /**
   * Get jobs with filtering and pagination
   */
  async getJobs(filters: JobFilters = {}): Promise<JobsResponse> {
    const params = new URLSearchParams();

    if (filters.search) params.append('search', filters.search);
    if (filters.location) params.append('location', filters.location);
    if (filters.type) params.append('type', filters.type);
    if (filters.remote !== undefined) params.append('remote', filters.remote.toString());
    if (filters.salary_min) params.append('salary_min', filters.salary_min.toString());
    if (filters.salary_max) params.append('salary_max', filters.salary_max.toString());
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.limit) params.append('limit', filters.limit.toString());

    const response = await apiClient.get<JobsResponse>(`/jobs/?${params.toString()}`);
    return response.data;
  },

  /**
   * Get job by ID
   */
  async getJob(jobId: string): Promise<Job> {
    const response = await apiClient.get<Job>(`/jobs/${jobId}`);
    return response.data;
  },

  /**
   * Save a job for the current user
   */
  async saveJob(jobId: string): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>('/jobs/save', { job_id: jobId });
    return response.data;
  },

  /**
   * Unsave a job for the current user
   */
  async unsaveJob(jobId: string): Promise<{ message: string }> {
    const response = await apiClient.delete<{ message: string }>(`/jobs/${jobId}/save`);
    return response.data;
  },

  /**
   * Get saved jobs for the current user
   */
  async getSavedJobs(): Promise<Job[]> {
    const response = await apiClient.get<Job[]>('/jobs/saved/list');
    return response.data;
  },

  /**
   * Apply for a job
   */
  async applyForJob(jobId: string, applicationData: JobApplicationRequest = {}): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>(`/jobs/${jobId}/apply`, applicationData);
    return response.data;
  },

  /**
   * Get job applications for current user
   */
  async getJobApplications(): Promise<JobApplication[]> {
    const response = await apiClient.get<JobApplication[]>('/applications/');
    return response.data;
  },

  /**
   * Get job categories/tags
   */
  async getJobCategories(): Promise<string[]> {
    const response = await apiClient.get<string[]>('/jobs/meta/categories');
    return response.data;
  },

  /**
   * Get job types
   */
  async getJobTypes(): Promise<string[]> {
    const response = await apiClient.get<string[]>('/jobs/meta/types');
    return response.data;
  },

  /**
   * Get job recommendations for current user
   */
  async getJobRecommendations(limit: number = 10): Promise<JobsResponse> {
    const response = await apiClient.get<JobsResponse>(`/recommendations/jobs?limit=${limit}`);
    return response.data;
  },

  /**
   * Get trending jobs
   */
  async getTrendingJobs(limit: number = 10): Promise<Job[]> {
    const response = await apiClient.get<Job[]>(`/recommendations/trending?limit=${limit}`);
    return response.data;
  }
};
