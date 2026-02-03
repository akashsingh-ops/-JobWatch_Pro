import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { usersService, UserProfile } from '@/services/api/users';
import { User, Activity, Settings } from 'lucide-react';
import { motion } from 'framer-motion';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const { toast } = useToast();

  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('personal');

  // Form states for different sections
  const [personalData, setPersonalData] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    bio: '',
    current_title: '',
    current_company: '',
    years_of_experience: '',
    industry: '',
    profile_visibility: 'public',
    email_notifications: true,
    sms_notifications: false,
    push_notifications: true
  });

  const [skillsData, setSkillsData] = useState<string[]>([]);
  const [preferencesData, setPreferencesData] = useState({
    locations: [] as string[],
    job_types: [] as string[],
    salary_min: '',
    salary_max: '',
    remote_ok: false
  });

  // Load profile data
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const profileData = await usersService.getProfile();
        setProfile(profileData);

        // Populate form data
        setPersonalData({
          first_name: profileData.first_name || '',
          last_name: profileData.last_name || '',
          phone: profileData.phone || '',
          date_of_birth: profileData.date_of_birth || '',
          gender: profileData.gender || '',
          bio: profileData.bio || '',
          current_title: profileData.current_title || '',
          current_company: profileData.current_company || '',
          years_of_experience: profileData.years_of_experience?.toString() || '',
          industry: profileData.industry || '',
          profile_visibility: profileData.profile_visibility,
          email_notifications: profileData.email_notifications,
          sms_notifications: profileData.sms_notifications,
          push_notifications: profileData.push_notifications
        });

        setSkillsData(profileData.skills);
        setPreferencesData({
          locations: profileData.job_preferences?.locations || [],
          job_types: profileData.job_preferences?.job_types || [],
          salary_min: profileData.job_preferences?.salary_min?.toString() || '',
          salary_max: profileData.job_preferences?.salary_max?.toString() || '',
          remote_ok: profileData.job_preferences?.remote_ok || false
        });

      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load profile data',
          variant: 'destructive'
        });
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      loadProfile();
    }
  }, [user, toast]);

  const handlePersonalSave = async () => {
    setIsSaving(true);
    try {
      const updateData = {
        first_name: personalData.first_name,
        last_name: personalData.last_name,
        phone: personalData.phone || undefined,
        date_of_birth: personalData.date_of_birth || undefined,
        gender: personalData.gender || undefined,
        bio: personalData.bio || undefined,
        current_title: personalData.current_title || undefined,
        current_company: personalData.current_company || undefined,
        years_of_experience: personalData.years_of_experience ? parseFloat(personalData.years_of_experience) : undefined,
        industry: personalData.industry || undefined,
        profile_visibility: personalData.profile_visibility,
        email_notifications: personalData.email_notifications,
        sms_notifications: personalData.sms_notifications,
        push_notifications: personalData.push_notifications
      };

      await usersService.updateProfile(updateData);
      toast({
        title: 'Success',
        description: 'Profile updated successfully'
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update profile',
        variant: 'destructive'
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handlePreferencesSave = async () => {
    setIsSaving(true);
    try {
      await usersService.updatePreferences({
        locations: preferencesData.locations,
        job_types: preferencesData.job_types,
        salary_min: preferencesData.salary_min ? parseInt(preferencesData.salary_min) : undefined,
        salary_max: preferencesData.salary_max ? parseInt(preferencesData.salary_max) : undefined,
        remote_ok: preferencesData.remote_ok
      });

      toast({
        title: 'Success',
        description: 'Job preferences updated successfully'
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update preferences',
        variant: 'destructive'
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center space-y-4">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto" />
            <p className="text-muted-foreground">Loading profile...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold mb-4">Failed to Load Profile</h2>
          <p className="text-muted-foreground">Unable to load your profile information.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <User className="h-8 w-8 text-primary" />
            Profile Settings
          </h1>
          <p className="text-muted-foreground mt-2">
            Manage your account settings and job preferences
          </p>

          {/* Profile Completeness Indicator */}
          <div className="mt-4 p-4 bg-gradient-to-r from-primary/5 to-primary/10 rounded-lg border">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">Profile Completeness</span>
              <span className="text-sm text-muted-foreground">{profile.profile_completeness_score}%</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-primary h-2 rounded-full transition-all duration-300"
                style={{ width: `${profile.profile_completeness_score}%` }}
              />
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              Complete your profile to get better job recommendations
            </p>
          </div>
        </div>

        {/* Profile Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="personal">Personal</TabsTrigger>
            <TabsTrigger value="professional">Professional</TabsTrigger>
            <TabsTrigger value="preferences">Job Preferences</TabsTrigger>
            <TabsTrigger value="account">Account</TabsTrigger>
          </TabsList>

          {/* Personal Information Tab */}
          <TabsContent value="personal" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>
                  Update your basic personal details and contact information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="first_name">First Name</Label>
                    <Input
                      id="first_name"
                      value={personalData.first_name}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, first_name: e.target.value }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last_name">Last Name</Label>
                    <Input
                      id="last_name"
                      value={personalData.last_name}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, last_name: e.target.value }))}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone</Label>
                    <Input
                      id="phone"
                      value={personalData.phone}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, phone: e.target.value }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="date_of_birth">Date of Birth</Label>
                    <Input
                      id="date_of_birth"
                      type="date"
                      value={personalData.date_of_birth}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, date_of_birth: e.target.value }))}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="gender">Gender</Label>
                  <Select value={personalData.gender} onValueChange={(value) => setPersonalData(prev => ({ ...prev, gender: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select gender" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                      <SelectItem value="prefer_not_to_say">Prefer not to say</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea
                    id="bio"
                    placeholder="Tell us about yourself..."
                    value={personalData.bio}
                    onChange={(e) => setPersonalData(prev => ({ ...prev, bio: e.target.value }))}
                    rows={3}
                  />
                </div>

                <Button onClick={handlePersonalSave} disabled={isSaving} className="w-full md:w-auto">
                  {isSaving ? 'Saving...' : 'Save Personal Information'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Professional Information Tab */}
          <TabsContent value="professional" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Professional Information</CardTitle>
                <CardDescription>
                  Your current role and work experience
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="current_title">Current Job Title</Label>
                    <Input
                      id="current_title"
                      value={personalData.current_title}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, current_title: e.target.value }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="current_company">Current Company</Label>
                    <Input
                      id="current_company"
                      value={personalData.current_company}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, current_company: e.target.value }))}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="years_experience">Years of Experience</Label>
                    <Input
                      id="years_experience"
                      type="number"
                      step="0.5"
                      value={personalData.years_of_experience}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, years_of_experience: e.target.value }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="industry">Industry</Label>
                    <Input
                      id="industry"
                      value={personalData.industry}
                      onChange={(e) => setPersonalData(prev => ({ ...prev, industry: e.target.value }))}
                    />
                  </div>
                </div>

                <Button onClick={handlePersonalSave} disabled={isSaving} className="w-full md:w-auto">
                  {isSaving ? 'Saving...' : 'Save Professional Information'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Job Preferences Tab */}
          <TabsContent value="preferences" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Job Preferences</CardTitle>
                <CardDescription>
                  Set your preferences to get better job recommendations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Preferred Job Types</Label>
                  <div className="flex flex-wrap gap-2">
                    {['Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship'].map((type) => (
                      <Button
                        key={type}
                        variant={preferencesData.job_types.includes(type) ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => {
                          setPreferencesData(prev => ({
                            ...prev,
                            job_types: prev.job_types.includes(type)
                              ? prev.job_types.filter(t => t !== type)
                              : [...prev.job_types, type]
                          }));
                        }}
                      >
                        {type}
                      </Button>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Preferred Locations</Label>
                  <Input
                    placeholder="Add locations (comma separated)"
                    value={preferencesData.locations.join(', ')}
                    onChange={(e) => {
                      const locations = e.target.value.split(',').map(loc => loc.trim()).filter(loc => loc);
                      setPreferencesData(prev => ({ ...prev, locations }));
                    }}
                  />
                  {preferencesData.locations.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {preferencesData.locations.map((location) => (
                        <Badge key={location} variant="secondary">
                          {location}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="salary_min">Minimum Salary (₹)</Label>
                    <Input
                      id="salary_min"
                      type="number"
                      value={preferencesData.salary_min}
                      onChange={(e) => setPreferencesData(prev => ({ ...prev, salary_min: e.target.value }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="salary_max">Maximum Salary (₹)</Label>
                    <Input
                      id="salary_max"
                      type="number"
                      value={preferencesData.salary_max}
                      onChange={(e) => setPreferencesData(prev => ({ ...prev, salary_max: e.target.value }))}
                    />
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Switch
                    id="remote_ok"
                    checked={preferencesData.remote_ok}
                    onCheckedChange={(checked) => setPreferencesData(prev => ({ ...prev, remote_ok: checked }))}
                  />
                  <Label htmlFor="remote_ok">Open to remote work opportunities</Label>
                </div>

                <Button onClick={handlePreferencesSave} disabled={isSaving} className="w-full md:w-auto">
                  {isSaving ? 'Saving...' : 'Save Job Preferences'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Account Settings Tab */}
          <TabsContent value="account" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Account Settings</CardTitle>
                <CardDescription>
                  Manage your account preferences and notifications
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <h4 className="font-medium">Notification Preferences</h4>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Email Notifications</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive job alerts and updates via email
                        </p>
                      </div>
                      <Switch
                        checked={personalData.email_notifications}
                        onCheckedChange={(checked) => setPersonalData(prev => ({ ...prev, email_notifications: checked }))}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>SMS Notifications</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive important updates via SMS
                        </p>
                      </div>
                      <Switch
                        checked={personalData.sms_notifications}
                        onCheckedChange={(checked) => setPersonalData(prev => ({ ...prev, sms_notifications: checked }))}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Push Notifications</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive in-app notifications
                        </p>
                      </div>
                      <Switch
                        checked={personalData.push_notifications}
                        onCheckedChange={(checked) => setPersonalData(prev => ({ ...prev, push_notifications: checked }))}
                      />
                    </div>
                  </div>
                </div>

                <Separator />

                <div className="space-y-4">
                  <h4 className="font-medium">Privacy Settings</h4>

                  <div className="space-y-2">
                    <Label htmlFor="profile_visibility">Profile Visibility</Label>
                    <Select
                      value={personalData.profile_visibility}
                      onValueChange={(value) => setPersonalData(prev => ({ ...prev, profile_visibility: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="public">Public</SelectItem>
                        <SelectItem value="private">Private</SelectItem>
                        <SelectItem value="connections_only">Connections Only</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <Button onClick={handlePersonalSave} disabled={isSaving} className="w-full md:w-auto">
                  {isSaving ? 'Saving...' : 'Save Account Settings'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </motion.div>
    </div>
  );
};

export default Profile;
