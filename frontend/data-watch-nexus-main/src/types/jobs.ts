export interface Job {
  id: string;
  title: string;
  company: string;
  companyLogo?: string;
  location: string;
  type: 'Full-time' | 'Part-time' | 'Contract' | 'Freelance' | 'Internship';
  remote: boolean;
  salary?: {
    min: number;
    max: number;
    currency: string;
  };
  description: string;
  requirements: string[];
  benefits?: string[];
  tags: string[];
  postedDate: string;
  expiryDate?: string;
  applicationUrl?: string;
  applyEmail?: string;
  featured?: boolean;
  saved?: boolean;
}

export interface JobFilters {
  search?: string;
  location?: string;
  type?: string;
  remote?: boolean;
  salaryMin?: number;
  salaryMax?: number;
  page?: number;
  limit?: number;
}

export interface JobsResponse {
  jobs: Job[];
  total: number;
  page: number;
  totalPages: number;
}

export interface SavedJob {
  id: string;
  jobId: string;
  userId: string;
  savedAt: string;
  job: Job;
}