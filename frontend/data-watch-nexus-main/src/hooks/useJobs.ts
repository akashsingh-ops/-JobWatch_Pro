import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { JobFilters, Job } from '@/types/jobs';
import { jobsService } from '@/services/api/jobs';
import { transformApiJobToFrontend } from '@/utils/api';

export const useJobs = (filters: JobFilters = {}) => {
  return useQuery({
    queryKey: ['jobs', filters],
    queryFn: async () => {
      const apiResponse = await jobsService.getJobs(filters);
      return {
        jobs: apiResponse.jobs.map(transformApiJobToFrontend),
        total: apiResponse.total,
        page: apiResponse.page,
        totalPages: apiResponse.total_pages,
      };
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (React Query v5)
  });
};

export const useJob = (jobId: string) => {
  return useQuery({
    queryKey: ['job', jobId],
    queryFn: async (): Promise<Job | null> => {
      if (!jobId) return null;
      const apiJob = await jobsService.getJob(jobId);
      return transformApiJobToFrontend(apiJob);
    },
    enabled: !!jobId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useJobCategories = () => {
  return useQuery({
    queryKey: ['job-categories'],
    queryFn: async (): Promise<string[]> => {
      return await jobsService.getJobCategories();
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useJobTypes = () => {
  return useQuery({
    queryKey: ['job-types'],
    queryFn: async (): Promise<string[]> => {
      return await jobsService.getJobTypes();
    },
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useSaveJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (jobId: string): Promise<{ message: string }> => {
      return await jobsService.saveJob(jobId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      queryClient.invalidateQueries({ queryKey: ['saved-jobs'] });
    },
  });
};

export const useUnsaveJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (jobId: string): Promise<{ message: string }> => {
      return await jobsService.unsaveJob(jobId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      queryClient.invalidateQueries({ queryKey: ['saved-jobs'] });
    },
  });
};

export const useSavedJobs = () => {
  return useQuery({
    queryKey: ['saved-jobs'],
    queryFn: async (): Promise<Job[]> => {
      const apiJobs = await jobsService.getSavedJobs();
      return apiJobs.map(transformApiJobToFrontend);
    },
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

// Job Application Hooks
export const useApplyForJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      jobId,
      applicationData
    }: {
      jobId: string;
      applicationData?: any
    }): Promise<{ message: string }> => {
      return await jobsService.applyForJob(jobId, applicationData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['job-applications'] });
    },
  });
};

export const useJobApplications = () => {
  return useQuery({
    queryKey: ['job-applications'],
    queryFn: async () => {
      return await jobsService.getJobApplications();
    },
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

// Job Recommendation Hooks
export const useJobRecommendations = (limit: number = 10) => {
  return useQuery({
    queryKey: ['job-recommendations', limit],
    queryFn: async () => {
      const apiResponse = await jobsService.getJobRecommendations(limit);
      return {
        jobs: apiResponse.jobs.map(transformApiJobToFrontend),
        total: apiResponse.total,
        page: apiResponse.page,
        totalPages: apiResponse.total_pages,
      };
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useTrendingJobs = (limit: number = 10) => {
  return useQuery({
    queryKey: ['trending-jobs', limit],
    queryFn: async (): Promise<Job[]> => {
      const apiJobs = await jobsService.getTrendingJobs(limit);
      return apiJobs.map(transformApiJobToFrontend);
    },
    staleTime: 15 * 60 * 1000, // 15 minutes
  });
};