export interface Record {
  id: string;
  title: string;
  description: string;
  source: string;
  category: string;
  publishedDate: string;
  url: string;
  createdAt: string;
}

export interface RecordsResponse {
  records: Record[];
  total: number;
  page: number;
  totalPages: number;
}

export interface RecordFilters {
  search?: string;
  category?: string;
  page?: number;
  limit?: number;
}