import { Record, RecordsResponse, RecordFilters } from '@/types/records';

export const mockRecords: Record[] = [
  {
    id: '1',
    title: 'Machine Learning Trends 2024',
    description: 'Comprehensive analysis of machine learning trends and their impact on various industries including healthcare, finance, and enterprise automation.',
    source: 'TechInsights',
    category: 'Technology',
    publishedDate: '2024-01-15T08:00:00Z',
    url: 'https://example.com/ml-trends-2024',
    createdAt: '2024-01-15T08:00:00Z',
  },
  {
    id: '2',
    title: 'Remote Work Productivity Study',
    description: 'Research findings on remote work productivity, asynchronous communication patterns, and employee satisfaction in distributed teams.',
    source: 'Workforce Analytics',
    category: 'Business',
    publishedDate: '2024-01-14T12:00:00Z',
    url: 'https://example.com/remote-work-study',
    createdAt: '2024-01-14T12:00:00Z',
  },
  {
    id: '3',
    title: 'Healthcare Biotechnology Advancements',
    description: 'Breakthrough innovations in personalized genomics and CRISPR-assisted drug discovery methodologies.',
    source: 'BioHealth Review',
    category: 'Healthcare',
    publishedDate: '2024-01-13T10:30:00Z',
    url: 'https://example.com/biotech-advancements',
    createdAt: '2024-01-13T10:30:00Z',
  },
  {
    id: '4',
    title: 'Global Fintech & Decentralized Finance 2024',
    description: 'Overview of modern payment gateways, cross-border settlement protocols, and regulatory developments.',
    source: 'Financial Market Watch',
    category: 'Finance',
    publishedDate: '2024-01-12T14:15:00Z',
    url: 'https://example.com/fintech-trends',
    createdAt: '2024-01-12T14:15:00Z',
  },
  {
    id: '5',
    title: 'Modern UI/UX Design Patterns for Enterprise SaaS',
    description: 'Best practices for accessibility, component design systems, and rapid prototyping workflows.',
    source: 'Design Digest',
    category: 'Design',
    publishedDate: '2024-01-11T09:45:00Z',
    url: 'https://example.com/modern-design-patterns',
    createdAt: '2024-01-11T09:45:00Z',
  }
];

export const recordsApi = {
  // Get all records with filtering and pagination
  getRecords: async (filters: RecordFilters = {}): Promise<RecordsResponse> => {
    let list = [...mockRecords];
    if (filters.search) {
      const q = filters.search.toLowerCase();
      list = list.filter(r =>
        r.title.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.source.toLowerCase().includes(q)
      );
    }
    if (filters.category && filters.category !== 'all') {
      list = list.filter(r => r.category.toLowerCase() === filters.category!.toLowerCase());
    }

    const page = filters.page || 1;
    const limit = filters.limit || 12;
    const total = list.length;
    const totalPages = Math.ceil(total / limit) || 1;
    const start = (page - 1) * limit;
    const records = list.slice(start, start + limit);

    return {
      records,
      total,
      page,
      totalPages,
    };
  },

  // Get a single record by ID
  getRecord: async (id: string): Promise<Record> => {
    const found = mockRecords.find(r => r.id === id);
    if (!found) {
      throw new Error('Record not found');
    }
    return found;
  },

  // Get available categories
  getCategories: async (): Promise<string[]> => {
    const categories = Array.from(new Set(mockRecords.map(r => r.category)));
    return categories.sort();
  },
};