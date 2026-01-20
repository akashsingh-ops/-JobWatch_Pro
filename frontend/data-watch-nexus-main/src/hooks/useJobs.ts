import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { JobFilters, JobsResponse, Job } from '@/types/jobs';

// Mock job data
const mockJobs: Job[] = [
  {
    id: '1',
    title: 'Senior Frontend Developer',
    company: 'TechCorp Inc.',
    companyLogo: '/placeholder.svg',
    location: 'San Francisco, CA',
    type: 'Full-time',
    remote: true,
    salary: { min: 120000, max: 180000, currency: '$' },
    description: 'Join our team to build amazing user experiences with React, TypeScript, and modern web technologies. We are looking for a passionate developer who loves creating intuitive interfaces.',
    requirements: ['React', 'TypeScript', 'Next.js', '5+ years experience'],
    benefits: ['Health Insurance', 'Remote Work', '401k Matching'],
    tags: ['React', 'TypeScript', 'Frontend', 'Remote'],
    postedDate: '2024-01-15T10:00:00Z',
    applicationUrl: 'https://example.com/apply',
    featured: true,
    saved: false
  },
  {
    id: '2',
    title: 'Product Manager',
    company: 'StartupXYZ',
    location: 'New York, NY',
    type: 'Full-time',
    remote: false,
    salary: { min: 100000, max: 140000, currency: '$' },
    description: 'Drive product strategy and execution for our growing SaaS platform. Work closely with engineering and design teams to deliver exceptional user experiences.',
    requirements: ['Product Management', 'Agile', '3+ years experience', 'Technical background'],
    benefits: ['Equity Package', 'Health Insurance', 'Flexible PTO'],
    tags: ['Product', 'Strategy', 'SaaS', 'Agile'],
    postedDate: '2024-01-14T15:30:00Z',
    featured: false,
    saved: true
  },
  {
    id: '3',
    title: 'Full Stack Engineer',
    company: 'InnovateLab',
    location: 'Austin, TX',
    type: 'Full-time',
    remote: true,
    salary: { min: 90000, max: 130000, currency: '$' },
    description: 'Build scalable web applications using modern technologies. Work on both frontend and backend systems in a collaborative environment.',
    requirements: ['JavaScript', 'Node.js', 'React', 'Database design'],
    tags: ['Full Stack', 'JavaScript', 'Node.js', 'Remote'],
    postedDate: '2024-01-13T09:00:00Z',
    featured: false,
    saved: false
  },
  {
    id: '4',
    title: 'UX Designer',
    company: 'DesignStudio',
    location: 'Seattle, WA',
    type: 'Contract',
    remote: true,
    description: 'Create beautiful and functional user interfaces for web and mobile applications. Collaborate with product teams to deliver user-centered designs.',
    requirements: ['Figma', 'User Research', 'Prototyping', 'Portfolio required'],
    tags: ['UX', 'Design', 'Figma', 'Remote'],
    postedDate: '2024-01-12T14:00:00Z',
    featured: false,
    saved: false
  },
  {
    id: '5',
    title: 'DevOps Engineer',
    company: 'CloudTech Solutions',
    location: 'Remote',
    type: 'Full-time',
    remote: true,
    salary: { min: 110000, max: 160000, currency: '$' },
    description: 'Manage cloud infrastructure and deployment pipelines. Help scale our systems to handle millions of users worldwide.',
    requirements: ['AWS', 'Docker', 'Kubernetes', 'CI/CD', '4+ years experience'],
    tags: ['DevOps', 'AWS', 'Docker', 'Remote'],
    postedDate: '2024-01-11T11:00:00Z',
    featured: true,
    saved: false
  },
  {
    id: '6',
    title: 'Data Scientist',
    company: 'AI Innovations',
    location: 'Boston, MA',
    type: 'Full-time',
    remote: false,
    salary: { min: 130000, max: 190000, currency: '$' },
    description: 'Apply machine learning and statistical analysis to solve complex business problems. Work with large datasets to derive actionable insights.',
    requirements: ['Python', 'Machine Learning', 'SQL', 'Statistics', 'PhD preferred'],
    tags: ['Data Science', 'Python', 'ML', 'Analytics'],
    postedDate: '2024-01-10T16:00:00Z',
    featured: false,
    saved: true
  }
];

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const useJobs = (filters: JobFilters = {}) => {
  return useQuery({
    queryKey: ['jobs', filters],
    queryFn: async (): Promise<JobsResponse> => {
      await delay(800); // Simulate network delay
      
      let filteredJobs = [...mockJobs];
      
      // Apply filters
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        filteredJobs = filteredJobs.filter(job =>
          job.title.toLowerCase().includes(searchLower) ||
          job.company.toLowerCase().includes(searchLower) ||
          job.tags.some(tag => tag.toLowerCase().includes(searchLower)) ||
          job.description.toLowerCase().includes(searchLower)
        );
      }
      
      if (filters.location) {
        filteredJobs = filteredJobs.filter(job =>
          job.location.toLowerCase().includes(filters.location!.toLowerCase())
        );
      }
      
      if (filters.type) {
        filteredJobs = filteredJobs.filter(job => job.type === filters.type);
      }
      
      if (filters.remote !== undefined) {
        filteredJobs = filteredJobs.filter(job => job.remote === filters.remote);
      }
      
      if (filters.salaryMin && filters.salaryMax) {
        filteredJobs = filteredJobs.filter(job => {
          if (!job.salary) return false;
          return job.salary.min >= filters.salaryMin! && job.salary.max <= filters.salaryMax!;
        });
      }
      
      // Pagination
      const page = filters.page || 1;
      const limit = filters.limit || 12;
      const total = filteredJobs.length;
      const totalPages = Math.ceil(total / limit);
      const startIndex = (page - 1) * limit;
      const jobs = filteredJobs.slice(startIndex, startIndex + limit);
      
      return {
        jobs,
        total,
        page,
        totalPages
      };
    },
  });
};

export const useJob = (jobId: string) => {
  return useQuery({
    queryKey: ['job', jobId],
    queryFn: async (): Promise<Job | null> => {
      await delay(500);
      return mockJobs.find(job => job.id === jobId) || null;
    },
  });
};

export const useJobCategories = () => {
  return useQuery({
    queryKey: ['job-categories'],
    queryFn: async (): Promise<string[]> => {
      await delay(300);
      const allTags = mockJobs.flatMap(job => job.tags);
      return [...new Set(allTags)].sort();
    },
  });
};

export const useJobTypes = () => {
  return useQuery({
    queryKey: ['job-types'],
    queryFn: async (): Promise<string[]> => {
      await delay(300);
      const allTypes = mockJobs.map(job => job.type);
      return [...new Set(allTypes)].sort();
    },
  });
};

export const useSaveJob = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (jobId: string): Promise<void> => {
      await delay(500);
      // In a real app, this would make an API call
      console.log('Saving job:', jobId);
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
    mutationFn: async (jobId: string): Promise<void> => {
      await delay(500);
      console.log('Unsaving job:', jobId);
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
      await delay(600);
      return mockJobs.filter(job => job.saved);
    },
  });
};