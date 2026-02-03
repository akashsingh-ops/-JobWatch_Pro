/**
 * User profile API service
 */

import { apiClient } from '@/api/client';

export interface UserProfile {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  profile_picture?: string;
  current_title?: string;
  current_company?: string;
  years_of_experience?: number;
  industry?: string;
  bio?: string;
  skills: string[];
  certifications?: Array<{
    name: string;
    issuer: string;
    date: string;
  }>;
  education?: Array<{
    degree: string;
    institution: string;
    year: number;
  }>;
  work_experience?: Array<{
    title: string;
    company: string;
    start_date: string;
    end_date?: string;
    description?: string;
  }>;
  job_preferences?: {
    locations: string[];
    job_types: string[];
    salary_min?: number;
    salary_max?: number;
    remote_ok: boolean;
  };
  resume_url?: string;
  portfolio_url?: string;
  linkedin_url?: string;
  github_url?: string;
  profile_visibility: string;
  email_notifications: boolean;
  sms_notifications: boolean;
  push_notifications: boolean;
  created_at: string;
  updated_at: string;
  profile_completeness_score?: number;
}

export interface UpdateProfileRequest {
  first_name?: string;
  last_name?: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  current_title?: string;
  current_company?: string;
  years_of_experience?: number;
  industry?: string;
  bio?: string;
  skills?: string[];
  profile_visibility?: string;
  email_notifications?: boolean;
  sms_notifications?: boolean;
  push_notifications?: boolean;
}

export interface UpdatePreferencesRequest {
  locations?: string[];
  job_types?: string[];
  salary_min?: number;
  salary_max?: number;
  remote_ok?: boolean;
}

export const usersService = {
  /**
   * Get current user profile
   */
  async getProfile(): Promise<UserProfile> {
    const response = await apiClient.get<UserProfile>('/users/profile');
    return response.data;
  },

  /**
   * Update user profile
   */
  async updateProfile(profileData: UpdateProfileRequest): Promise<UserProfile> {
    const response = await apiClient.put<UserProfile>('/users/profile', profileData);
    return response.data;
  },

  /**
   * Update user job preferences
   */
  async updatePreferences(preferences: UpdatePreferencesRequest): Promise<UserProfile> {
    const response = await apiClient.put<UserProfile>('/users/preferences', preferences);
    return response.data;
  },

  /**
   * Upload resume
   */
  async uploadResume(file: File): Promise<{ resume_url: string }> {
    const formData = new FormData();
    formData.append('resume', file);

    const response = await apiClient.post<{ resume_url: string }>('/users/resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Upload profile picture
   */
  async uploadProfilePicture(file: File): Promise<{ profile_picture: string }> {
    const formData = new FormData();
    formData.append('profile_picture', file);

    const response = await apiClient.post<{ profile_picture: string }>('/users/profile-picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Delete resume
   */
  async deleteResume(): Promise<{ message: string }> {
    const response = await apiClient.delete<{ message: string }>('/users/resume');
    return response.data;
  },

  /**
   * Get user's job applications
   */
  async getJobApplications(): Promise<any[]> {
    const response = await apiClient.get<any[]>('/applications/');
    return response.data;
  }
};
