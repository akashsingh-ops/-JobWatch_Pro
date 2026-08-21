import React, { useState } from 'react';
import { ShieldCheck, Plus, Briefcase, Trash2, CheckCircle2 } from 'lucide-react';
import { useJobs, useCreateJob, useDeleteJob } from '@/hooks/useJobs';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import { Job } from '@/types/jobs';

const AdminDashboard: React.FC = () => {
  const { toast } = useToast();
  const { data } = useJobs();
  const createJobMutation = useCreateJob();
  const deleteJobMutation = useDeleteJob();

  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    category: 'Engineering',
    type: 'Full-time' as Job['type'],
    experienceLevel: 'Mid' as Job['experienceLevel'],
    salary: '$140,000 - $175,000',
    description: '',
    applyUrl: 'https://example.com/apply',
  });

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || !formData.company) {
      toast({
        variant: 'destructive',
        title: 'Validation Error',
        description: 'Role title and company are required.',
      });
      return;
    }

    try {
      await createJobMutation.mutateAsync(formData);
      toast({
        title: 'Job Published',
        description: `${formData.title} at ${formData.company} has been added to the public board.`,
      });
      setFormData({
        title: '',
        company: '',
        location: '',
        category: 'Engineering',
        type: 'Full-time',
        experienceLevel: 'Mid',
        salary: '$140,000 - $175,000',
        description: '',
        applyUrl: 'https://example.com/apply',
      });
    } catch {
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'Failed to create job posting.',
      });
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteJobMutation.mutateAsync(id);
      toast({ title: 'Job posting deleted' });
    } catch {
      toast({ variant: 'destructive', title: 'Error deleting job' });
    }
  };

  const jobs = data?.jobs || [];

  return (
    <div className="container mx-auto px-4 py-8 space-y-8 max-w-6xl">
      <div className="border-b pb-6">
        <div className="flex items-center gap-2">
          <ShieldCheck className="h-6 w-6 text-primary" />
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Admin & Employer Console</h1>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          Post new job openings directly into the system or manage active listings.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Create form */}
        <Card className="lg:col-span-1 border shadow-sm">
          <CardContent className="p-6">
            <h2 className="text-base font-semibold border-b pb-2 mb-4 flex items-center gap-2">
              <Plus className="h-4 w-4 text-primary" /> Add New Job Posting
            </h2>

            <form onSubmit={handleCreate} className="space-y-4">
              <div className="space-y-1.5">
                <Label htmlFor="job-title">Job Title</Label>
                <Input
                  id="job-title"
                  placeholder="e.g. Lead Platform Engineer"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="company-name">Company Name</Label>
                <Input
                  id="company-name"
                  placeholder="e.g. Stripe, OpenAI"
                  value={formData.company}
                  onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div className="space-y-1.5">
                  <Label>Category</Label>
                  <Select
                    value={formData.category}
                    onValueChange={(val) => setFormData({ ...formData, category: val })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Engineering">Engineering</SelectItem>
                      <SelectItem value="AI & Data Science">AI & Data Science</SelectItem>
                      <SelectItem value="Design">Design</SelectItem>
                      <SelectItem value="DevOps">DevOps</SelectItem>
                      <SelectItem value="Product">Product</SelectItem>
                      <SelectItem value="Security">Security</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-1.5">
                  <Label>Type</Label>
                  <Select
                    value={formData.type}
                    onValueChange={(val) => setFormData({ ...formData, type: val as Job['type'] })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Full-time">Full-time</SelectItem>
                      <SelectItem value="Remote">Remote</SelectItem>
                      <SelectItem value="Contract">Contract</SelectItem>
                      <SelectItem value="Part-time">Part-time</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="location-val">Location</Label>
                <Input
                  id="location-val"
                  placeholder="e.g. Remote / New York, NY"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="salary-val">Salary Range</Label>
                <Input
                  id="salary-val"
                  placeholder="e.g. $150,000 - $185,000"
                  value={formData.salary}
                  onChange={(e) => setFormData({ ...formData, salary: e.target.value })}
                />
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="desc-val">Job Description</Label>
                <Textarea
                  id="desc-val"
                  rows={3}
                  placeholder="Role responsibilities and qualifications..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <Button type="submit" className="w-full btn-gradient">
                Publish Opportunity
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Existing jobs table/list */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold">Active Listings ({jobs.length})</h2>
          </div>

          <div className="space-y-3">
            {jobs.map((job) => (
              <Card key={job.id} className="border p-4">
                <div className="flex items-center justify-between gap-4">
                  <div className="space-y-1">
                    <h3 className="font-semibold text-sm">{job.title}</h3>
                    <div className="text-xs text-muted-foreground flex items-center gap-2">
                      <span>{job.company}</span>
                      <span>•</span>
                      <span>{job.category}</span>
                      <span>•</span>
                      <span>{job.location}</span>
                    </div>
                  </div>

                  <Button
                    variant="ghost"
                    size="icon"
                    className="text-muted-foreground hover:text-destructive shrink-0"
                    onClick={() => handleDelete(job.id)}
                    title="Delete listing"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
