/**
 * API Utility Functions
 */

import { AxiosError } from 'axios';
import { ApiError } from '@/services/api';

export const handleApiError = (error: AxiosError | ApiError): string => {
  if ('response' in error) {
    // Axios error
    const axiosError = error as AxiosError;
    const data = axiosError.response?.data as any;
    return data?.detail || data?.message || axiosError.message || 'An error occurred';
  } else {
    // API service error
    const apiError = error as ApiError;
    return apiError.message || 'An error occurred';
  }
};

export const createQueryString = (params: Record<string, any>): string => {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      if (Array.isArray(value)) {
        value.forEach(v => searchParams.append(key, v.toString()));
      } else {
        searchParams.append(key, value.toString());
      }
    }
  });

  return searchParams.toString();
};

export const formatApiFilters = (filters: Record<string, any>) => {
  const formatted: Record<string, any> = {};

  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      formatted[key] = value;
    }
  });

  return formatted;
};

/**
 * Transform API Job (snake_case) to Frontend Job (camelCase)
 */
export const transformApiJobToFrontend = (apiJob: any): any => {
  return {
    id: apiJob.id,
    title: apiJob.title,
    company: apiJob.company,
    companyLogo: apiJob.company_logo,
    location: apiJob.location,
    type: apiJob.type,
    remote: apiJob.remote,
    salary: apiJob.salary ? {
      min: apiJob.salary.min,
      max: apiJob.salary.max,
      currency: apiJob.salary.currency,
    } : undefined,
    description: apiJob.description,
    requirements: apiJob.requirements || [],
    benefits: apiJob.benefits || [],
    tags: apiJob.tags || [],
    postedDate: apiJob.posted_date,
    expiryDate: apiJob.expiry_date,
    applicationUrl: apiJob.application_url,
    applyEmail: apiJob.apply_email,
    featured: apiJob.featured,
    saved: apiJob.saved,
  };
};