import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { recordsApi } from '@/api/records';
import { RecordFilters } from '@/types/records';

export const useRecords = (filters: RecordFilters = {}) => {
  return useQuery({
    queryKey: ['records', filters],
    queryFn: () => recordsApi.getRecords(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useRecord = (id: string) => {
  return useQuery({
    queryKey: ['record', id],
    queryFn: () => recordsApi.getRecord(id),
    enabled: !!id,
  });
};

export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: recordsApi.getCategories,
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};