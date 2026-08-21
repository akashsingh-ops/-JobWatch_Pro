import { apiClient } from './client';
import { Job, JobFilters, JobsResponse } from '@/types/jobs';

export interface AIMatchResponse {
  success: boolean;
  job_id: string;
  match: {
    score: number;
    reasons: string[];
    missing_skills: string[];
    matching_skills: string[];
    recommendations: string[];
  };
  analysis?: {
    job_id: string;
    title: string;
    seniority: string;
    remote_classification: string;
    summary: string;
  };
}

export interface ParseResumeResponse {
  success: boolean;
  parsed: {
    detected_skills: string[];
    estimated_experience_years: number;
    summary: string;
  };
}

export const jobsApi = {
  getJobs: async (filters: JobFilters = {}): Promise<JobsResponse> => {
    const params: Record<string, string | number | boolean> = {};
    if (filters.search) params.search = filters.search;
    if (filters.category && filters.category !== 'all') params.category = filters.category;
    if (filters.type && filters.type !== 'all') params.type = filters.type;
    if (filters.experienceLevel && filters.experienceLevel !== 'all') params.experienceLevel = filters.experienceLevel;
    if (filters.page) params.page = filters.page;
    if (filters.limit) params.limit = filters.limit;

    const response = await apiClient.get('/jobs/', { params });
    const data = response.data;

    // Handle both { jobs: [], total: N } and { results: [], count: N }
    const jobsList: Job[] = data.jobs || data.results || (Array.isArray(data) ? data : []);
    const total = data.total ?? data.count ?? jobsList.length;
    const page = data.page ?? filters.page ?? 1;
    const limit = filters.limit || 12;
    const totalPages = data.totalPages ?? (Math.ceil(total / limit) || 1);

    return {
      jobs: jobsList,
      total,
      page,
      totalPages,
    };
  },

  getJob: async (jobId: string): Promise<Job> => {
    const response = await apiClient.get(`/jobs/${jobId}/`);
    return response.data;
  },

  createJob: async (jobData: Partial<Job>): Promise<Job> => {
    const response = await apiClient.post('/jobs/', jobData);
    return response.data;
  },

  deleteJob: async (jobId: string): Promise<void> => {
    await apiClient.delete(`/jobs/${jobId}/`);
  },

  getSavedJobs: async (): Promise<Job[]> => {
    const response = await apiClient.get('/saved-jobs/');
    const data = response.data;
    if (Array.isArray(data)) return data;
    if (data.results) return data.results;
    if (data.jobs) return data.jobs;
    return [];
  },

  saveJob: async (jobId: string): Promise<{ success: boolean; saved: boolean; job: Job }> => {
    const response = await apiClient.post('/saved-jobs/', { job_id: jobId });
    return response.data;
  },

  unsaveJob: async (jobId: string): Promise<{ success: boolean; message: string }> => {
    const response = await apiClient.delete(`/saved-jobs/${jobId}/`);
    return response.data;
  },

  getAiMatch: async (jobId: string): Promise<AIMatchResponse> => {
    const response = await apiClient.get(`/ai/match/${jobId}/`);
    return response.data;
  },

  getAiRecommendations: async (): Promise<Job[]> => {
    const response = await apiClient.get('/ai/recommendations/');
    return response.data.recommendations || [];
  },

  parseResume: async (resumeText: string): Promise<ParseResumeResponse> => {
    const response = await apiClient.post('/ai/parse-resume/', { resume_text: resumeText });
    return response.data;
  },
};
