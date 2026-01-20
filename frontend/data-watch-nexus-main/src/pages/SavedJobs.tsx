import React from 'react';
import { JobCard } from '@/components/jobs/JobCard';
import { JobSkeleton } from '@/components/jobs/JobSkeleton';
import { useSavedJobs, useUnsaveJob } from '@/hooks/useJobs';
import { useNavigate } from 'react-router-dom';
import { useToast } from '@/hooks/use-toast';
import { Heart, Bookmark, FileText } from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';

const SavedJobs: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { data: savedJobs, isLoading, error } = useSavedJobs();
  const unsaveJobMutation = useUnsaveJob();

  const handleJobClick = (jobId: string) => {
    navigate(`/jobs/${jobId}`);
  };

  const handleUnsaveJob = async (jobId: string) => {
    try {
      await unsaveJobMutation.mutateAsync(jobId);
      toast({
        title: 'Job removed',
        description: 'Job has been removed from your saved list.',
      });
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Failed to remove job',
        description: 'Please try again later.',
      });
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <div className="flex justify-center mb-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary shadow-lg">
            <Heart className="h-6 w-6 text-primary-foreground" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gradient">Saved Jobs</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Keep track of interesting opportunities and apply when you're ready.
        </p>
      </motion.div>

      {/* Jobs Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="space-y-6"
      >
        {error ? (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 text-destructive mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Failed to load saved jobs</h3>
            <p className="text-muted-foreground">
              There was an error loading your saved jobs. Please try again.
            </p>
            <Button 
              onClick={() => window.location.reload()} 
              className="mt-4"
            >
              Retry
            </Button>
          </div>
        ) : isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 6 }).map((_, index) => (
              <JobSkeleton key={index} />
            ))}
          </div>
        ) : !savedJobs || savedJobs.length === 0 ? (
          <div className="text-center py-12">
            <Bookmark className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No saved jobs yet</h3>
            <p className="text-muted-foreground mb-6">
              Save interesting job opportunities to apply later and keep track of your favorites.
            </p>
            <Button 
              onClick={() => navigate('/dashboard')}
              className="btn-gradient"
            >
              Browse Jobs
            </Button>
          </div>
        ) : (
          <>
            {/* Results info */}
            <div className="flex items-center justify-between">
              <p className="text-sm text-muted-foreground">
                You have {savedJobs.length} saved job{savedJobs.length !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Jobs grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {savedJobs.map((job, index) => (
                <motion.div
                  key={job.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <JobCard
                    job={{ ...job, saved: true }}
                    onClick={() => handleJobClick(job.id)}
                    onSave={() => handleUnsaveJob(job.id)}
                  />
                </motion.div>
              ))}
            </div>
          </>
        )}
      </motion.div>
    </div>
  );
};

export default SavedJobs;