import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Building2, 
  MapPin, 
  DollarSign, 
  Calendar, 
  Bookmark, 
  BookmarkCheck, 
  ExternalLink, 
  ArrowLeft, 
  CheckCircle2, 
  Share2,
  ShieldCheck
} from 'lucide-react';
import { useJob, useSaveJob, useUnsaveJob } from '@/hooks/useJobs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { Skeleton } from '@/components/ui/skeleton';

const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const { data: job, isLoading, error } = useJob(id || '');
  const saveJobMutation = useSaveJob();
  const unsaveJobMutation = useUnsaveJob();

  const handleToggleSave = async () => {
    if (!job) return;
    try {
      if (job.saved) {
        await unsaveJobMutation.mutateAsync(job.id);
        toast({ title: 'Removed from saved jobs' });
      } else {
        await saveJobMutation.mutateAsync(job.id);
        toast({ title: 'Job bookmarked successfully!' });
      }
    } catch {
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'Failed to update bookmark.',
      });
    }
  };

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    toast({
      title: 'Link copied to clipboard',
      description: 'You can now share this position with others.',
    });
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl space-y-6">
        <Skeleton className="h-8 w-32" />
        <Skeleton className="h-64 w-full rounded-xl" />
        <Skeleton className="h-96 w-full rounded-xl" />
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="container mx-auto px-4 py-16 text-center max-w-md space-y-4">
        <h2 className="text-2xl font-bold">Position Not Found</h2>
        <p className="text-muted-foreground text-sm">
          The job posting you are looking for does not exist or has expired.
        </p>
        <Button onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl space-y-6">
      {/* Back button */}
      <Button
        variant="ghost"
        size="sm"
        onClick={() => navigate(-1)}
        className="text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Listings
      </Button>

      {/* Header Banner Card */}
      <Card className="border shadow-sm overflow-hidden">
        <CardContent className="p-6 md:p-8 space-y-6">
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
            <div className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant="secondary">{job.category}</Badge>
                <Badge variant="outline">{job.type}</Badge>
                {job.experienceLevel && (
                  <Badge variant="outline">{job.experienceLevel}</Badge>
                )}
              </div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-foreground">
                {job.title}
              </h1>
              <div className="flex items-center gap-2 text-muted-foreground text-sm font-medium">
                <Building2 className="h-4 w-4" />
                <span className="text-foreground font-semibold">{job.company}</span>
              </div>
            </div>

            {/* Quick Action buttons */}
            <div className="flex items-center gap-2 shrink-0">
              <Button
                variant="outline"
                size="icon"
                onClick={handleShare}
                title="Share link"
              >
                <Share2 className="h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                onClick={handleToggleSave}
                title={job.saved ? 'Remove bookmark' : 'Bookmark job'}
              >
                {job.saved ? (
                  <BookmarkCheck className="h-4 w-4 text-primary fill-primary/20" />
                ) : (
                  <Bookmark className="h-4 w-4" />
                )}
              </Button>
              <Button
                className="btn-gradient px-6"
                onClick={() => window.open(job.applyUrl || '#', '_blank')}
              >
                Apply Now <ExternalLink className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Quick Metrics row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t text-sm">
            <div className="space-y-1">
              <div className="text-xs text-muted-foreground flex items-center gap-1">
                <MapPin className="h-3.5 w-3.5" /> Location
              </div>
              <div className="font-medium text-foreground">{job.location}</div>
            </div>

            <div className="space-y-1">
              <div className="text-xs text-muted-foreground flex items-center gap-1">
                <DollarSign className="h-3.5 w-3.5" /> Compensation
              </div>
              <div className="font-medium text-emerald-600 dark:text-emerald-400">
                {job.salary || 'Competitive'}
              </div>
            </div>

            <div className="space-y-1">
              <div className="text-xs text-muted-foreground flex items-center gap-1">
                <Calendar className="h-3.5 w-3.5" /> Date Posted
              </div>
              <div className="font-medium text-foreground">
                {new Date(job.postedDate).toLocaleDateString()}
              </div>
            </div>

            <div className="space-y-1">
              <div className="text-xs text-muted-foreground flex items-center gap-1">
                <ShieldCheck className="h-3.5 w-3.5 text-primary" /> Verification
              </div>
              <div className="font-medium text-foreground">Verified Direct</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Content Details */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left 2 Cols: Description & Requirements */}
        <div className="md:col-span-2 space-y-6">
          <Card className="border shadow-sm">
            <CardContent className="p-6 space-y-4">
              <h2 className="text-lg font-semibold border-b pb-2">Role Overview</h2>
              <p className="text-muted-foreground text-sm leading-relaxed whitespace-pre-line">
                {job.description}
              </p>
            </CardContent>
          </Card>

          {job.requirements && job.requirements.length > 0 && (
            <Card className="border shadow-sm">
              <CardContent className="p-6 space-y-4">
                <h2 className="text-lg font-semibold border-b pb-2">Key Requirements & Skills</h2>
                <ul className="space-y-2.5">
                  {job.requirements.map((req, i) => (
                    <li key={i} className="flex items-start gap-2.5 text-sm text-muted-foreground">
                      <CheckCircle2 className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                      <span>{req}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Right Col: Company Sidebar info */}
        <div className="space-y-6">
          <Card className="border shadow-sm">
            <CardContent className="p-6 space-y-4">
              <h3 className="font-semibold text-sm">About {job.company}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Leading organization innovating in telemetry systems, scalable software, and cloud intelligence.
              </p>
              <div className="pt-2 border-t space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Industry</span>
                  <span className="font-medium">{job.category}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Team Size</span>
                  <span className="font-medium">100 - 500</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Workplace</span>
                  <span className="font-medium">{job.type}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border border-primary/20 bg-primary/5 shadow-sm p-5 text-center space-y-3">
            <h4 className="font-semibold text-sm">Ready to take the next step?</h4>
            <p className="text-xs text-muted-foreground">
              Submit your profile directly through the official application portal.
            </p>
            <Button
              className="w-full btn-gradient"
              onClick={() => window.open(job.applyUrl || '#', '_blank')}
            >
              Apply on Company Site
            </Button>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default JobDetail;
