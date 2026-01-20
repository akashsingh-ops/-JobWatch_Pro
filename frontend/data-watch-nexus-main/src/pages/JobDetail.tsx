import React from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { useJob, useSaveJob } from '@/hooks/useJobs';
import { useToast } from '@/hooks/use-toast';
import { 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  DollarSign, 
  ExternalLink, 
  Heart, 
  Briefcase,
  Building2,
  Users,
  Clock,
  CheckCircle,
  Share2
} from 'lucide-react';
import { motion } from 'framer-motion';

const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const { data: job, isLoading, error } = useJob(id!);
  const saveJobMutation = useSaveJob();

  const handleSaveJob = async () => {
    if (!job) return;
    
    try {
      await saveJobMutation.mutateAsync(job.id);
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

  const handleApply = () => {
    if (job?.applicationUrl) {
      window.open(job.applicationUrl, '_blank');
    } else if (job?.applyEmail) {
      window.open(`mailto:${job.applyEmail}?subject=Application for ${job.title}`, '_blank');
    }
  };

  const formatSalary = (salary: typeof job.salary) => {
    if (!salary) return null;
    const { min, max, currency } = salary;
    if (min && max) {
      return `${currency}${min.toLocaleString()} - ${currency}${max.toLocaleString()}`;
    }
    return min ? `From ${currency}${min.toLocaleString()}` : null;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffInDays === 0) return 'Today';
    if (diffInDays === 1) return 'Yesterday';
    if (diffInDays < 7) return `${diffInDays} days ago`;
    if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          <p className="text-muted-foreground">Loading job details...</p>
        </div>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold mb-4">Job Not Found</h2>
          <p className="text-muted-foreground mb-6">
            The job you're looking for doesn't exist or has been removed.
          </p>
          <Button onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Job Board
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="space-y-8"
      >
        {/* Back Button */}
        <Button
          variant="ghost"
          onClick={() => navigate('/dashboard')}
          className="mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Job Board
        </Button>

        {/* Job Header */}
        <Card className="border-0 shadow-lg bg-gradient-to-br from-card to-card/80">
          <CardHeader>
            <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
              <div className="flex items-start space-x-4 flex-1">
                <Avatar className="h-16 w-16">
                  <AvatarImage src={job.companyLogo} alt={job.company} />
                  <AvatarFallback>
                    <Building2 className="h-8 w-8" />
                  </AvatarFallback>
                </Avatar>
                
                <div className="flex-1">
                  <CardTitle className="text-2xl lg:text-3xl mb-2">{job.title}</CardTitle>
                  <p className="text-xl text-muted-foreground font-medium mb-4">{job.company}</p>
                  
                  <div className="flex flex-wrap items-center gap-4 text-muted-foreground">
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-2" />
                      <span>{job.location}</span>
                      {job.remote && (
                        <Badge variant="secondary" className="ml-2">
                          Remote
                        </Badge>
                      )}
                    </div>
                    
                    <div className="flex items-center">
                      <Briefcase className="h-4 w-4 mr-2" />
                      <span>{job.type}</span>
                    </div>
                    
                    {job.salary && (
                      <div className="flex items-center text-primary font-medium">
                        <DollarSign className="h-4 w-4 mr-2" />
                        <span>{formatSalary(job.salary)}</span>
                      </div>
                    )}
                    
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2" />
                      <span>Posted {formatDate(job.postedDate)}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3 lg:min-w-fit">
                <Button 
                  onClick={handleSaveJob}
                  variant="outline" 
                  className="flex items-center"
                  disabled={saveJobMutation.isPending}
                >
                  <Heart 
                    className={`mr-2 h-4 w-4 ${job.saved ? 'fill-primary text-primary' : ''}`} 
                  />
                  {job.saved ? 'Saved' : 'Save Job'}
                </Button>
                
                <Button 
                  onClick={handleApply}
                  className="btn-gradient flex items-center"
                  disabled={!job.applicationUrl && !job.applyEmail}
                >
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Apply Now
                </Button>
                
                <Button variant="ghost" size="sm">
                  <Share2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
        </Card>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Description */}
            <Card>
              <CardHeader>
                <CardTitle>Job Description</CardTitle>
              </CardHeader>
              <CardContent className="prose prose-sm max-w-none">
                <p className="text-muted-foreground leading-relaxed whitespace-pre-line">
                  {job.description}
                </p>
              </CardContent>
            </Card>

            {/* Requirements */}
            {job.requirements && job.requirements.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Requirements</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {job.requirements.map((requirement, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="h-4 w-4 text-primary mr-2 mt-1 flex-shrink-0" />
                        <span className="text-muted-foreground">{requirement}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Benefits */}
            {job.benefits && job.benefits.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Benefits & Perks</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {job.benefits.map((benefit, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="h-4 w-4 text-primary mr-2 mt-1 flex-shrink-0" />
                        <span className="text-muted-foreground">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Job Tags */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Skills & Technologies</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {job.tags.map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-sm">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Application Deadline */}
            {job.expiryDate && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg flex items-center">
                    <Clock className="h-5 w-5 mr-2" />
                    Application Deadline
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">
                    {new Date(job.expiryDate).toLocaleDateString('en-US', {
                      weekday: 'long',
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Similar Jobs */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Similar Jobs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-sm text-muted-foreground border-l-2 border-primary/20 pl-3">
                    <p className="font-medium">Frontend Developer</p>
                    <p className="text-xs">TechStart Inc.</p>
                  </div>
                  <div className="text-sm text-muted-foreground border-l-2 border-primary/20 pl-3">
                    <p className="font-medium">React Developer</p>
                    <p className="text-xs">WebFlow Co.</p>
                  </div>
                  <div className="text-sm text-muted-foreground border-l-2 border-primary/20 pl-3">
                    <p className="font-medium">Full Stack Engineer</p>
                    <p className="text-xs">DevCorp Ltd.</p>
                  </div>
                  <Button variant="ghost" size="sm" asChild className="w-full mt-4">
                    <Link to="/dashboard">View More Jobs</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Bottom Action Bar */}
        <Card className="sticky bottom-4 border-0 shadow-xl bg-card/95 backdrop-blur-md">
          <CardContent className="py-4">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                <Avatar className="h-12 w-12">
                  <AvatarImage src={job.companyLogo} alt={job.company} />
                  <AvatarFallback>
                    <Building2 className="h-6 w-6" />
                  </AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-semibold">{job.title}</p>
                  <p className="text-sm text-muted-foreground">{job.company}</p>
                </div>
              </div>
              
              <div className="flex gap-3">
                <Button 
                  onClick={handleSaveJob}
                  variant="outline"
                  disabled={saveJobMutation.isPending}
                >
                  <Heart className={`mr-2 h-4 w-4 ${job.saved ? 'fill-primary text-primary' : ''}`} />
                  {job.saved ? 'Saved' : 'Save'}
                </Button>
                <Button 
                  onClick={handleApply}
                  className="btn-gradient"
                  disabled={!job.applicationUrl && !job.applyEmail}
                >
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Apply Now
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default JobDetail;