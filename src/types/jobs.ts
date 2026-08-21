export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  type: 'Full-time' | 'Part-time' | 'Contract' | 'Remote' | 'Internship';
  category: string;
  description: string;
  requirements?: string[];
  salary?: string;
  postedDate: string;
  applyUrl?: string;
  saved?: boolean;
  featured?: boolean;
  experienceLevel?: 'Entry' | 'Mid' | 'Senior' | 'Lead';
}

export interface JobFilters {
  search?: string;
  category?: string;
  type?: string;
  location?: string;
  experienceLevel?: string;
  page?: number;
  limit?: number;
}

export interface JobsResponse {
  jobs: Job[];
  total: number;
  page: number;
  totalPages: number;
}
