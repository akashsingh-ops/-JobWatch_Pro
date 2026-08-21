import React from 'react';
import { Search, Filter, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { JobFilters as FiltersType } from '@/types/jobs';

interface JobFiltersProps {
  filters: FiltersType;
  onFilterChange: (key: keyof FiltersType, value: string) => void;
  onReset: () => void;
  categories: string[];
}

export const JobFilters: React.FC<JobFiltersProps> = ({
  filters,
  onFilterChange,
  onReset,
  categories,
}) => {
  const hasActiveFilters = 
    Boolean(filters.search) || 
    (filters.category && filters.category !== 'all') || 
    (filters.type && filters.type !== 'all') ||
    (filters.experienceLevel && filters.experienceLevel !== 'all');

  return (
    <div className="bg-card border rounded-xl p-4 shadow-sm space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
        {/* Search input */}
        <div className="relative md:col-span-5">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search by job title, company, or skills..."
            value={filters.search || ''}
            onChange={(e) => onFilterChange('search', e.target.value)}
            className="pl-9 h-10"
          />
        </div>

        {/* Category select */}
        <div className="md:col-span-3">
          <Select
            value={filters.category || 'all'}
            onValueChange={(val) => onFilterChange('category', val)}
          >
            <SelectTrigger className="h-10">
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              {categories.map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {cat}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Job Type select */}
        <div className="md:col-span-2">
          <Select
            value={filters.type || 'all'}
            onValueChange={(val) => onFilterChange('type', val)}
          >
            <SelectTrigger className="h-10">
              <SelectValue placeholder="Job Type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="Full-time">Full-time</SelectItem>
              <SelectItem value="Remote">Remote</SelectItem>
              <SelectItem value="Contract">Contract</SelectItem>
              <SelectItem value="Part-time">Part-time</SelectItem>
              <SelectItem value="Internship">Internship</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Experience select */}
        <div className="md:col-span-2 flex items-center gap-2">
          <Select
            value={filters.experienceLevel || 'all'}
            onValueChange={(val) => onFilterChange('experienceLevel', val)}
          >
            <SelectTrigger className="h-10">
              <SelectValue placeholder="Level" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Levels</SelectItem>
              <SelectItem value="Entry">Entry Level</SelectItem>
              <SelectItem value="Mid">Mid Level</SelectItem>
              <SelectItem value="Senior">Senior Level</SelectItem>
              <SelectItem value="Lead">Lead / Staff</SelectItem>
            </SelectContent>
          </Select>

          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="icon"
              onClick={onReset}
              title="Reset filters"
              className="h-10 w-10 shrink-0 text-muted-foreground hover:text-foreground"
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
