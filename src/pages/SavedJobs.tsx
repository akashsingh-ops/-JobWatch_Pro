import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bookmark, Briefcase, Trash2 } from 'lucide-react';
import { useSavedJobs, useUnsaveJob } from '@/hooks/useJobs';
import { JobCard } from '@/components/jobs/JobCard';
import { JobSkeleton } from '@/components/jobs/JobSkeleton';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';

const SavedJobs: React.FC = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { data: savedJobs, isLoading } = useSavedJobs();
  const unsaveJobMutation = useUnsaveJob();

  const handleUnsave = async (e: React.MouseEvent, jobId: string) => {
    e.stopPropagation();
    try {
      await unsaveJobMutation.mutateAsync(jobId);
      toast({
        title: 'Removed from bookmarks',
        description: 'The job was removed from your saved list.',
      });
    } catch {
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'Failed to update bookmark.',
      });
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-6 max-w-7xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-6">
        <div>
          <div className="flex items-center gap-2">
            <Bookmark className="h-6 w-6 text-primary" />
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Saved Jobs</h1>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Track and manage your bookmarked opportunities.
          </p>
        </div>

        <Button variant="outline" onClick={() => navigate('/dashboard')}>
          <Briefcase className="mr-2 h-4 w-4" /> Browse More Jobs
        </Button>
      </div>

      {/* Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 3 }).map((_, i) => (
            <JobSkeleton key={i} />
          ))}
        </div>
      ) : !savedJobs || savedJobs.length === 0 ? (
        <div className="text-center py-20 bg-card border rounded-2xl p-8 space-y-4">
          <div className="flex justify-center">
            <div className="h-14 w-14 rounded-full bg-primary/10 flex items-center justify-center text-primary">
              <Bookmark className="h-7 w-7" />
            </div>
          </div>
          <div className="space-y-1">
            <h3 className="text-lg font-semibold">No saved jobs yet</h3>
            <p className="text-sm text-muted-foreground max-w-md mx-auto">
              Click the bookmark icon on any job card to save it here for easy access and tracking.
            </p>
          </div>
          <Button className="btn-gradient" onClick={() => navigate('/dashboard')}>
            Explore Available Positions
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {savedJobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onClick={() => navigate(`/jobs/${job.id}`)}
              onSave={(e) => handleUnsave(e, job.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default SavedJobs;
