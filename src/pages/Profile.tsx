import React, { useState } from 'react';
import { User, Mail, Shield, Save, Briefcase, MapPin } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [name, setName] = useState(user?.name || 'Engineer');
  const [title, setTitle] = useState('Senior Software Engineer');
  const [location, setLocation] = useState('San Francisco, CA');
  const [skills, setSkills] = useState(['React', 'TypeScript', 'Node.js', 'PostgreSQL', 'Docker', 'AWS']);
  const [newSkill, setNewSkill] = useState('');

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: 'Profile Updated',
      description: 'Your career profile and notification tags have been saved.',
    });
  };

  const addSkill = () => {
    if (newSkill.trim() && !skills.includes(newSkill.trim())) {
      setSkills([...skills, newSkill.trim()]);
      setNewSkill('');
    }
  };

  const removeSkill = (skillToRemove: string) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-6 max-w-4xl">
      <div className="border-b pb-6">
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Candidate Profile</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Manage your job-matching telemetry profile and target skills.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        <Card className="border shadow-sm">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-base font-semibold border-b pb-2">Basic Information</h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  disabled
                  value={user?.email || 'user@jobwatch.pro'}
                  className="bg-muted/50 text-muted-foreground"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="title">Professional Headline</Label>
                <Input
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="location">Target Location / Preference</Label>
                <Input
                  id="location"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Skills Card */}
        <Card className="border shadow-sm">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-base font-semibold border-b pb-2">Monitored Target Skills</h2>
            <p className="text-xs text-muted-foreground">
              Our automated crawlers match new postings with these keywords to prioritize your alerts.
            </p>

            <div className="flex flex-wrap gap-2 pt-2">
              {skills.map((skill) => (
                <Badge
                  key={skill}
                  variant="secondary"
                  className="px-3 py-1 text-xs cursor-pointer hover:bg-destructive/10 hover:text-destructive transition-colors"
                  onClick={() => removeSkill(skill)}
                  title="Click to remove"
                >
                  {skill} ✕
                </Badge>
              ))}
            </div>

            <div className="flex gap-2 max-w-sm pt-2">
              <Input
                placeholder="Add skill (e.g. Kubernetes)..."
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    addSkill();
                  }
                }}
              />
              <Button type="button" variant="outline" onClick={addSkill}>
                Add
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end">
          <Button type="submit" className="btn-gradient">
            <Save className="mr-2 h-4 w-4" /> Save Profile Settings
          </Button>
        </div>
      </form>
    </div>
  );
};

export default Profile;
