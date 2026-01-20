import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { JobCard } from '@/components/jobs/JobCard';
import { JobSkeleton } from '@/components/jobs/JobSkeleton';
import { useJobs, useJobTypes, useSaveJob } from '@/hooks/useJobs';
import { useToast } from '@/hooks/use-toast';
import { Search, Filter, FileText, AlertCircle, Briefcase, MapPin, DollarSign } from 'lucide-react';
import { motion } from 'framer-motion';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [filters, setFilters] = useState({
    search: '',
    location: '',
    type: '',
    remote: undefined as boolean | undefined,
    page: 1,
    limit: 12,
  });

  const [debouncedSearch, setDebouncedSearch] = useState('');
  const saveJobMutation = useSaveJob();

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(filters.search);
    }, 300);
    return () => clearTimeout(timer);
  }, [filters.search]);

  const { data: jobsData, isLoading, error } = useJobs({
    ...filters,
    search: debouncedSearch,
  });

  const { data: jobTypes } = useJobTypes();

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters(prev => ({ ...prev, search: e.target.value, page: 1 }));
  };

  const handleLocationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters(prev => ({ ...prev, location: e.target.value, page: 1 }));
  };

  const handleTypeChange = (type: string) => {
    setFilters(prev => ({ 
      ...prev, 
      type: type === 'all' ? '' : type, 
      page: 1 
    }));
  };

  const handleRemoteToggle = (checked: boolean) => {
    setFilters(prev => ({ ...prev, remote: checked ? true : undefined, page: 1 }));
  };

  const handleJobClick = (jobId: string) => {
    navigate(`/jobs/${jobId}`);
  };

  const handleSaveJob = async (jobId: string) => {
    try {
      await saveJobMutation.mutateAsync(jobId);
      toast({
        title: 'Job saved',
        description: 'Job has been added to your saved list.',
      });
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Failed to save job',
        description: 'Please try again later.',
      });
    }
  };

  const jobs = jobsData?.jobs || [];
  const totalPages = jobsData?.totalPages || 0;

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-4xl font-bold text-gradient">Job Board</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Discover your next opportunity from thousands of job postings tailored to your preferences.
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="space-y-6"
      >
        <div className="flex flex-col lg:flex-row gap-4 max-w-4xl mx-auto">
          <div className="flex-1 relative">
            <Briefcase className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <Input
              placeholder="Job title, company, keywords..."
              value={filters.search}
              onChange={handleSearchChange}
              className="pl-10 bg-card/50 border-0 shadow-md h-12"
            />
          </div>
          <div className="flex-1 relative">
            <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <Input
              placeholder="City, state, or remote..."
              value={filters.location}
              onChange={handleLocationChange}
              className="pl-10 bg-card/50 border-0 shadow-md h-12"
            />
          </div>
          <Button size="lg" className="btn-gradient px-8 h-12">
            <Search className="mr-2 h-4 w-4" />
            Search Jobs
          </Button>
        </div>

        <div className="flex flex-wrap gap-4 max-w-4xl mx-auto items-center">
          <Select value={filters.type || 'all'} onValueChange={handleTypeChange}>
            <SelectTrigger className="w-48 bg-card/50 border-0 shadow-md">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Job Type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              {jobTypes?.map((type) => (
                <SelectItem key={type} value={type}>{type}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          <div className="flex items-center space-x-2 bg-card/50 rounded-md px-4 py-2 shadow-md">
            <Switch
              id="remote"
              checked={filters.remote === true}
              onCheckedChange={handleRemoteToggle}
            />
            <Label htmlFor="remote" className="text-sm font-medium">Remote Only</Label>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="space-y-6"
      >
        {error ? (
          <div className="text-center py-12">
            <AlertCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Failed to load jobs</h3>
            <p className="text-muted-foreground">There was an error loading job listings. Please try again.</p>
            <Button onClick={() => window.location.reload()} className="mt-4">Retry</Button>
          </div>
        ) : isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 8 }).map((_, index) => (
              <JobSkeleton key={index} />
            ))}
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No jobs found</h3>
            <p className="text-muted-foreground">
              {filters.search || filters.location || filters.type 
                ? 'Try adjusting your search criteria or filters.'
                : 'No job postings are currently available.'}
            </p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                Showing {jobs.length} of {jobsData?.total || 0} jobs
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {jobs.map((job, index) => (
                <motion.div
                  key={job.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <JobCard
                    job={job}
                    onClick={() => handleJobClick(job.id)}
                    onSave={() => handleSaveJob(job.id)}
                  />
                </motion.div>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="flex justify-center space-x-2 pt-8">
                <Button
                  variant="outline"
                  onClick={() => setFilters(prev => ({ ...prev, page: Math.max(1, prev.page - 1) }))}
                  disabled={filters.page === 1}
                >
                  Previous
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setFilters(prev => ({ ...prev, page: Math.min(totalPages, prev.page + 1) }))}
                  disabled={filters.page === totalPages}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </motion.div>
    </div>
  );
};

export default Dashboard;