/**
 * Records API service
 */

import { apiClient } from '@/api/client';

export interface Record {
  id: string;
  title: string;
  description: string;
  source: string;
  category: string;
  published_date: string;
  url?: string;
  created_at: string;
}

export interface RecordsFilters {
  search?: string;
  category?: string;
  page?: number;
  limit?: number;
}

export interface RecordsResponse {
  records: Record[];
  total: number;
  page: number;
  total_pages: number;
}

export const recordsService = {
  /**
   * Get records with filtering and pagination
   */
  async getRecords(filters: RecordsFilters = {}): Promise<RecordsResponse> {
    const params = new URLSearchParams();

    if (filters.search) params.append('search', filters.search);
    if (filters.category) params.append('category', filters.category);
    if (filters.page) params.append('page', filters.page.toString());
    if (filters.limit) params.append('limit', filters.limit.toString());

    const response = await apiClient.get<RecordsResponse>(`/records/?${params.toString()}`);
    return response.data;
  },

  /**
   * Get record by ID
   */
  async getRecord(recordId: string): Promise<Record> {
    const response = await apiClient.get<Record>(`/records/${recordId}`);
    return response.data;
  },

  /**
   * Get available categories
   */
  async getCategories(): Promise<string[]> {
    const response = await apiClient.get<string[]>('/records/meta/categories');
    return response.data;
  },

  /**
   * Get available sources
   */
  async getSources(): Promise<string[]> {
    const response = await apiClient.get<string[]>('/records/meta/sources');
    return response.data;
  }
};
