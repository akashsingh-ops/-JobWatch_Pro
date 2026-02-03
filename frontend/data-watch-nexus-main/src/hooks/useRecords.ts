import { useQuery } from '@tanstack/react-query';
import { recordsService, RecordsFilters } from '@/services/api/records';

export const useRecords = (filters: RecordsFilters = {}) => {
  return useQuery({
    queryKey: ['records', filters],
    queryFn: () => recordsService.getRecords(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useRecord = (id: string) => {
  return useQuery({
    queryKey: ['record', id],
    queryFn: () => recordsService.getRecord(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: recordsService.getCategories,
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useRecordSources = () => {
  return useQuery({
    queryKey: ['record-sources'],
    queryFn: recordsService.getSources,
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};