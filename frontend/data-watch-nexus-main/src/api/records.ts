import { apiClient } from './client';
import { Record, RecordsResponse, RecordFilters } from '@/types/records';

export const recordsApi = {
  // Get all records with filtering and pagination
  getRecords: async (filters: RecordFilters = {}): Promise<RecordsResponse> => {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.category) params.append('category', filters.category);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.limit) params.append('limit', filters.limit.toString());

    const response = await apiClient.get(`/records?${params.toString()}`);
    return response.data;
  },

  // Get a single record by ID
  getRecord: async (id: string): Promise<Record> => {
    const response = await apiClient.get(`/records/${id}`);
    return response.data;
  },

  // Get available categories
  getCategories: async (): Promise<string[]> => {
    const response = await apiClient.get('/records/categories');
    return response.data;
  },
};