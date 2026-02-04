import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { useJob, useSaveJob, useApplyForJob } from '@/hooks/useJobs';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';
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
  const { user } = useAuth();
  const { data: job, isLoading, error } = useJob(id!);
  const saveJobMutation = useSaveJob();
  const applyJobMutation = useApplyForJob();

  // Application form state
  const [applicationData, setApplicationData] = useState({
    cover_letter: '',
    expected_salary: '',
  });
  const [isApplicationDialogOpen, setIsApplicationDialogOpen] = useState(false);

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

  const handleApply = async () => {
    if (!job || !user) {
      toast({
        variant: 'destructive',
        title: 'Authentication required',
        description: 'Please log in to apply for jobs.',
      });
      navigate('/login');
      return;
    }

    try {
      const result = await applyJobMutation.mutateAsync({
        jobId: job.id,
        applicationData: {
          cover_letter: applicationData.cover_letter || undefined,
          expected_salary: applicationData.expected_salary ? parseFloat(applicationData.expected_salary) : undefined,
        }
      });

      toast({
        title: 'Application submitted!',
        description: 'Your job application has been submitted successfully.',
      });

      setIsApplicationDialogOpen(false);
      setApplicationData({ cover_letter: '', expected_salary: '' });

    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Application failed',
        description: error?.message || 'Failed to submit application. Please try again.',
      });
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
                  {saveJobMutation.isPending ? 'Saving...' : job.saved ? 'Saved' : 'Save Job'}
                </Button>

                {/* Job Application Dialog */}
                <Dialog open={isApplicationDialogOpen} onOpenChange={setIsApplicationDialogOpen}>
                  <DialogTrigger asChild>
                    <Button
                      className="btn-gradient flex items-center"
                      disabled={applyJobMutation.isPending}
                    >
                      <ExternalLink className="mr-2 h-4 w-4" />
                      {applyJobMutation.isPending ? 'Applying...' : 'Apply Now'}
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[500px]">
                    <DialogHeader>
                      <DialogTitle>Apply for {job.title}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                      <div className="space-y-2">
                        <Label htmlFor="cover-letter">Cover Letter (Optional)</Label>
                        <Textarea
                          id="cover-letter"
                          placeholder="Tell us why you're interested in this position..."
                          value={applicationData.cover_letter}
                          onChange={(e) => setApplicationData(prev => ({
                            ...prev,
                            cover_letter: e.target.value
                          }))}
                          rows={4}
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="expected-salary">Expected Salary (Optional)</Label>
                        <Input
                          id="expected-salary"
                          type="number"
                          placeholder="Enter your expected salary"
                          value={applicationData.expected_salary}
                          onChange={(e) => setApplicationData(prev => ({
                            ...prev,
                            expected_salary: e.target.value
                          }))}
                        />
                      </div>

                      <div className="bg-muted p-3 rounded-lg text-sm text-muted-foreground">
                        <p>Your application will be submitted directly to {job.company}. They will review your profile and get back to you.</p>
                      </div>
                    </div>

                    <div className="flex justify-end gap-3">
                      <Button
                        variant="outline"
                        onClick={() => setIsApplicationDialogOpen(false)}
                      >
                        Cancel
                      </Button>
                      <Button
                        onClick={handleApply}
                        disabled={applyJobMutation.isPending}
                        className="btn-gradient"
                      >
                        {applyJobMutation.isPending ? 'Submitting...' : 'Submit Application'}
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>

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
                  {saveJobMutation.isPending ? 'Saving...' : job.saved ? 'Saved' : 'Save'}
                </Button>

                <Dialog open={isApplicationDialogOpen} onOpenChange={setIsApplicationDialogOpen}>
                  <DialogTrigger asChild>
                    <Button
                      className="btn-gradient"
                      disabled={applyJobMutation.isPending}
                    >
                      <ExternalLink className="mr-2 h-4 w-4" />
                      {applyJobMutation.isPending ? 'Applying...' : 'Apply Now'}
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[500px]">
                    <DialogHeader>
                      <DialogTitle>Apply for {job.title}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                      <div className="space-y-2">
                        <Label htmlFor="cover-letter-mobile">Cover Letter (Optional)</Label>
                        <Textarea
                          id="cover-letter-mobile"
                          placeholder="Tell us why you're interested in this position..."
                          value={applicationData.cover_letter}
                          onChange={(e) => setApplicationData(prev => ({
                            ...prev,
                            cover_letter: e.target.value
                          }))}
                          rows={3}
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="expected-salary-mobile">Expected Salary (Optional)</Label>
                        <Input
                          id="expected-salary-mobile"
                          type="number"
                          placeholder="Enter your expected salary"
                          value={applicationData.expected_salary}
                          onChange={(e) => setApplicationData(prev => ({
                            ...prev,
                            expected_salary: e.target.value
                          }))}
                        />
                      </div>
                    </div>

                    <div className="flex justify-end gap-3">
                      <Button
                        variant="outline"
                        onClick={() => setIsApplicationDialogOpen(false)}
                      >
                        Cancel
                      </Button>
                      <Button
                        onClick={handleApply}
                        disabled={applyJobMutation.isPending}
                        className="btn-gradient"
                      >
                        {applyJobMutation.isPending ? 'Submitting...' : 'Submit Application'}
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default JobDetail;