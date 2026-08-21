import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Briefcase, 
  TrendingUp, 
  Sparkles, 
  CheckCircle2, 
  Building2, 
  Search,
  BellRing
} from 'lucide-react';
import { useJobs, useSaveJob, useUnsaveJob } from '@/hooks/useJobs';
import { JobFilters } from '@/components/jobs/JobFilters';
import { JobCard } from '@/components/jobs/JobCard';
import { JobSkeleton } from '@/components/jobs/JobSkeleton';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { JobFilters as FiltersType } from '@/types/jobs';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [filters, setFilters] = useState<FiltersType>({
    page: 1,
    limit: 12,
  });

  const { data, isLoading, error } = useJobs(filters);
  const saveJobMutation = useSaveJob();
  const unsaveJobMutation = useUnsaveJob();

  const categories = [
    'Engineering',
    'AI & Data Science',
    'Design',
    'DevOps',
    'Product',
    'Security',
  ];

  const handleFilterChange = (key: keyof FiltersType, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value === 'all' ? undefined : value,
      page: 1,
    }));
  };

  const handleResetFilters = () => {
    setFilters({ page: 1, limit: 12 });
  };

  const handleToggleSave = async (jobId: string, currentSaved?: boolean) => {
    try {
      if (currentSaved) {
        await unsaveJobMutation.mutateAsync(jobId);
        toast({
          title: 'Removed from saved jobs',
          description: 'Job bookmark removed.',
        });
      } else {
        await saveJobMutation.mutateAsync(jobId);
        toast({
          title: 'Job bookmarked!',
          description: 'You can access this anytime in your Saved Jobs tab.',
        });
      }
    } catch {
      toast({
        variant: 'destructive',
        title: 'Action failed',
        description: 'Unable to update bookmark status.',
      });
    }
  };

  const jobs = data?.jobs || [];
  const total = data?.total || 0;

  return (
    <div className="container mx-auto px-4 py-8 space-y-8 max-w-7xl">
      {/* Hero Header */}
      <div className="relative rounded-2xl bg-gradient-to-br from-primary/10 via-card to-secondary/30 border p-6 md:p-10 shadow-sm overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-semibold border border-primary/20">
            <Sparkles className="h-3.5 w-3.5" />
            <span>Real-time Job Telemetry & Market Alerts</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
            Find High-Impact Opportunities with{' '}
            <span className="text-gradient">Precision Monitoring</span>
          </h1>
          <p className="text-muted-foreground text-sm md:text-base leading-relaxed">
            Monitor curated engineering, AI, design, and infrastructure roles. Set intelligent alerts and track your career pipeline effortlessly.
          </p>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <Button 
              className="btn-gradient shadow-md"
              onClick={() => navigate('/notifications')}
            >
              <BellRing className="mr-2 h-4 w-4" /> Configure Job Alerts
            </Button>
            <Button 
              variant="outline"
              onClick={() => navigate('/saved')}
            >
              View Saved Jobs
            </Button>
          </div>
        </div>

        {/* Decorative stats */}
        <div className="hidden lg:grid grid-cols-2 gap-3 absolute right-10 top-1/2 -translate-y-1/2 w-72">
          <div className="bg-card/90 backdrop-blur border p-4 rounded-xl shadow-sm">
            <div className="text-2xl font-bold text-primary">2,400+</div>
            <div className="text-xs text-muted-foreground">Active Telemetry Postings</div>
          </div>
          <div className="bg-card/90 backdrop-blur border p-4 rounded-xl shadow-sm">
            <div className="text-2xl font-bold text-emerald-500">99.8%</div>
            <div className="text-xs text-muted-foreground">Alert Delivery Rate</div>
          </div>
          <div className="bg-card/90 backdrop-blur border p-4 rounded-xl shadow-sm col-span-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-foreground">
              <CheckCircle2 className="h-4 w-4 text-primary" /> Verified Salaries & Locations
            </div>
          </div>
        </div>
      </div>

      {/* Filter bar */}
      <JobFilters
        filters={filters}
        onFilterChange={handleFilterChange}
        onReset={handleResetFilters}
        categories={categories}
      />

      {/* Quick Category Chips */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
        <span className="text-xs font-medium text-muted-foreground shrink-0">Popular:</span>
        {categories.map((cat) => {
          const isSelected = filters.category === cat;
          return (
            <button
              key={cat}
              onClick={() => handleFilterChange('category', isSelected ? 'all' : cat)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-all shrink-0 ${
                isSelected
                  ? 'bg-primary text-primary-foreground border-primary font-medium'
                  : 'bg-card text-muted-foreground hover:text-foreground hover:border-foreground/30'
              }`}
            >
              {cat}
            </button>
          );
        })}
      </div>

      {/* Results Header */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          Showing <span className="font-semibold text-foreground">{jobs.length}</span> of{' '}
          <span className="font-semibold text-foreground">{total}</span> positions
        </div>
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, idx) => (
            <JobSkeleton key={idx} />
          ))}
        </div>
      ) : error ? (
        <div className="text-center py-16 bg-card border rounded-xl space-y-4">
          <p className="text-destructive font-medium">Failed to load jobs list.</p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-16 bg-card border rounded-xl space-y-4">
          <div className="flex justify-center">
            <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center text-muted-foreground">
              <Search className="h-6 w-6" />
            </div>
          </div>
          <div className="space-y-1">
            <h3 className="text-lg font-semibold">No positions found</h3>
            <p className="text-sm text-muted-foreground max-w-sm mx-auto">
              We could not find any jobs matching your current filter criteria.
            </p>
          </div>
          <Button variant="outline" onClick={handleResetFilters}>
            Clear all filters
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onClick={() => navigate(`/jobs/${job.id}`)}
              onSave={() => handleToggleSave(job.id, job.saved)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
