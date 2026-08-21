import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Job, JobFilters, JobsResponse } from '@/types/jobs';
import { jobsApi } from '@/api/jobs';

export const mockJobs: Job[] = [
  {
    id: 'job-1',
    title: 'Senior Full Stack Engineer (React / Python)',
    company: 'Nexus Technologies',
    location: 'San Francisco, CA (Hybrid)',
    type: 'Full-time',
    category: 'Engineering',
    description: 'Join Nexus Technologies to architect high-throughput web telemetry platforms. You will design scalable React frontends and Django/PostgreSQL microservices processing real-time developer metrics.',
    requirements: [
      '5+ years experience building production React and TypeScript applications',
      'Proficiency in Python backend frameworks (Django, FastAPI)',
      'Strong database optimization skills in PostgreSQL',
      'Experience with containerized CI/CD workflows (Docker, GitHub Actions)'
    ],
    salary: '$165,000 - $195,000',
    postedDate: 'Just now',
    applyUrl: 'https://example.com/apply',
    saved: false,
    featured: true,
    experienceLevel: 'Senior',
  },
  {
    id: 'job-2',
    title: 'Staff AI & Machine Learning Researcher',
    company: 'Cortex Data Labs',
    location: 'Remote / US',
    type: 'Remote',
    category: 'AI & Data Science',
    description: 'Lead our core AI intelligence group developing foundation model fine-tuning and retrieval-augmented generation pipelines for automated talent telemetry.',
    requirements: [
      'M.S. or Ph.D. in Computer Science, Machine Learning, or related field',
      'Deep expertise with PyTorch, Transformer architectures, and vector search',
      'Track record of deploying LLM systems in high-availability environments',
      'Strong Python software engineering practices'
    ],
    salary: '$210,000 - $260,000',
    postedDate: '2h ago',
    applyUrl: 'https://example.com/apply',
    saved: true,
    featured: true,
    experienceLevel: 'Lead',
  },
  {
    id: 'job-3',
    title: 'Lead Cloud Infrastructure / DevOps Architect',
    company: 'Aether Dynamics',
    location: 'Austin, TX (On-site)',
    type: 'Full-time',
    category: 'DevOps',
    description: 'Scale multi-region Kubernetes clusters across AWS and GCP. Build resilient infrastructure-as-code and automated canary deployments.',
    requirements: [
      '6+ years in DevOps / Platform engineering',
      'Mastery of Terraform, Kubernetes, and Helm',
      'Deep understanding of network security, VPC peering, and observability'
    ],
    salary: '$180,000 - $220,000',
    postedDate: '4h ago',
    applyUrl: 'https://example.com/apply',
    saved: false,
    featured: false,
    experienceLevel: 'Lead',
  },
  {
    id: 'job-4',
    title: 'Principal Product Designer (Design Systems)',
    company: 'Orbit Media',
    location: 'Remote / Global',
    type: 'Remote',
    category: 'Design',
    description: 'Design intuitive, accessible UI component ecosystems and telemetry dashboards for enterprise recruitment teams.',
    requirements: [
      'Portfolio demonstrating end-to-end design systems in Figma',
      'Strong understanding of HTML/CSS, Tailwind, and React design tokens',
      'Proven experience in rapid prototyping and user research'
    ],
    salary: '$145,000 - $175,000',
    postedDate: '1d ago',
    applyUrl: 'https://example.com/apply',
    saved: false,
    featured: true,
    experienceLevel: 'Senior',
  },
  {
    id: 'job-5',
    title: 'Senior Backend Engineer (Go / PostgreSQL)',
    company: 'Pulse Platform',
    location: 'Seattle, WA (Hybrid)',
    type: 'Full-time',
    category: 'Engineering',
    description: 'Architect low-latency financial transaction pipelines and distributed event streams handling millions of events per hour.',
    requirements: [
      '4+ years building high-throughput systems in Go or Rust',
      'Advanced PostgreSQL indexing, partitioning, and connection pooling',
      'Experience with event streams and Redis caching'
    ],
    salary: '$170,000 - $205,000',
    postedDate: '1d ago',
    applyUrl: 'https://example.com/apply',
    saved: true,
    featured: false,
    experienceLevel: 'Senior',
  },
  {
    id: 'job-6',
    title: 'Application Security & Pen-Testing Specialist',
    company: 'Vanguard Security',
    location: 'Boston, MA (Hybrid)',
    type: 'Full-time',
    category: 'Security',
    description: 'Lead threat modeling, automated vulnerability scans, and security audits across our SaaS infrastructure.',
    requirements: [
      'Experience conducting SAST/DAST reviews in CI/CD pipelines',
      'Knowledge of OWASP Top 10, OAuth2, and zero-trust architectures',
      'Certifications like OSCP, CISSP, or equivalent experience'
    ],
    salary: '$150,000 - $185,000',
    postedDate: '2d ago',
    applyUrl: 'https://example.com/apply',
    saved: false,
    featured: false,
    experienceLevel: 'Mid',
  }
];

const getStoredJobs = (): Job[] => {
  const stored = localStorage.getItem('jobwatch_jobs');
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // fallback
    }
  }
  return mockJobs;
};

const saveStoredJobs = (jobs: Job[]) => {
  localStorage.setItem('jobwatch_jobs', JSON.stringify(jobs));
};

export const useJobs = (filters: JobFilters = {}) => {
  return useQuery<JobsResponse>({
    queryKey: ['jobs', filters],
    queryFn: async () => {
      try {
        const res = await jobsApi.getJobs(filters);
        if (res && res.jobs && res.jobs.length > 0) {
          saveStoredJobs(res.jobs);
          return res;
        }
      } catch (err) {
        console.warn('Backend query fallback to local cache:', err);
      }

      // Fallback filtering on local cached jobs
      let jobs = getStoredJobs();

      if (filters.search) {
        const q = filters.search.toLowerCase();
        jobs = jobs.filter(
          (j) =>
            j.title.toLowerCase().includes(q) ||
            j.company.toLowerCase().includes(q) ||
            j.description.toLowerCase().includes(q) ||
            j.location.toLowerCase().includes(q)
        );
      }

      if (filters.category && filters.category !== 'all') {
        jobs = jobs.filter(
          (j) => j.category.toLowerCase() === filters.category!.toLowerCase()
        );
      }

      if (filters.type && filters.type !== 'all') {
        jobs = jobs.filter(
          (j) => j.type.toLowerCase() === filters.type!.toLowerCase()
        );
      }

      if (filters.experienceLevel && filters.experienceLevel !== 'all') {
        jobs = jobs.filter(
          (j) => j.experienceLevel === filters.experienceLevel
        );
      }

      const page = filters.page || 1;
      const limit = filters.limit || 12;
      const total = jobs.length;
      const totalPages = Math.ceil(total / limit) || 1;
      const start = (page - 1) * limit;
      const paginated = jobs.slice(start, start + limit);

      return {
        jobs: paginated,
        total,
        page,
        totalPages,
      };
    },
  });
};

export const useJob = (jobId: string) => {
  return useQuery<Job | null>({
    queryKey: ['job', jobId],
    queryFn: async () => {
      try {
        return await jobsApi.getJob(jobId);
      } catch {
        const jobs = getStoredJobs();
        const job = jobs.find((j) => j.id === jobId);
        return job || null;
      }
    },
    enabled: !!jobId,
  });
};

export const useSavedJobs = () => {
  return useQuery<Job[]>({
    queryKey: ['savedJobs'],
    queryFn: async () => {
      try {
        const data = await jobsApi.getSavedJobs();
        if (data && data.length > 0) return data;
      } catch (err) {
        console.warn('Fallback to local saved jobs:', err);
      }
      const jobs = getStoredJobs();
      return jobs.filter((j) => j.saved);
    },
  });
};

export const useSaveJob = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (jobId: string) => {
      try {
        await jobsApi.saveJob(jobId);
      } catch (e) {
        console.warn('Local fallback save:', e);
      }
      const jobs = getStoredJobs();
      const updated = jobs.map((j) =>
        j.id === jobId ? { ...j, saved: true } : j
      );
      saveStoredJobs(updated);
      return jobId;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      queryClient.invalidateQueries({ queryKey: ['savedJobs'] });
      queryClient.invalidateQueries({ queryKey: ['job'] });
    },
  });
};

export const useUnsaveJob = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (jobId: string) => {
      try {
        await jobsApi.unsaveJob(jobId);
      } catch (e) {
        console.warn('Local fallback unsave:', e);
      }
      const jobs = getStoredJobs();
      const updated = jobs.map((j) =>
        j.id === jobId ? { ...j, saved: false } : j
      );
      saveStoredJobs(updated);
      return jobId;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      queryClient.invalidateQueries({ queryKey: ['savedJobs'] });
      queryClient.invalidateQueries({ queryKey: ['job'] });
    },
  });
};

export const useCreateJob = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (newJobData: Partial<Job>) => {
      let createdJob: Job | null = null;
      try {
        createdJob = await jobsApi.createJob(newJobData);
      } catch (e) {
        console.warn('Fallback create:', e);
      }

      if (!createdJob) {
        createdJob = {
          id: 'job-' + Date.now(),
          title: newJobData.title || 'Untitled Role',
          company: newJobData.company || 'Confidential',
          location: newJobData.location || 'Remote',
          type: newJobData.type || 'Full-time',
          category: newJobData.category || 'Engineering',
          description: newJobData.description || 'Job description details.',
          requirements: newJobData.requirements || ['Relevant industry experience'],
          salary: newJobData.salary || '$100,000 - $140,000',
          postedDate: 'Just now',
          applyUrl: newJobData.applyUrl || 'https://example.com/apply',
          saved: false,
          featured: newJobData.featured || false,
          experienceLevel: newJobData.experienceLevel || 'Mid',
        };
      }

      const jobs = getStoredJobs();
      jobs.unshift(createdJob);
      saveStoredJobs(jobs);
      return createdJob;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    },
  });
};

export const useDeleteJob = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (jobId: string) => {
      try {
        await jobsApi.deleteJob(jobId);
      } catch (e) {
        console.warn('Fallback delete:', e);
      }
      const jobs = getStoredJobs();
      const updated = jobs.filter((j) => j.id !== jobId);
      saveStoredJobs(updated);
      return jobId;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      queryClient.invalidateQueries({ queryKey: ['savedJobs'] });
    },
  });
};

