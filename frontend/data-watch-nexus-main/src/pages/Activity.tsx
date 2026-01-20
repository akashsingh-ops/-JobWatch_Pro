import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Activity as ActivityIcon, 
  User, 
  Bell, 
  Settings, 
  Mail, 
  Filter,
  Database,
  Eye,
  Download,
  Calendar,
  Clock
} from 'lucide-react';
import { motion } from 'framer-motion';

interface ActivityEvent {
  id: string;
  type: 'profile' | 'alerts' | 'data' | 'settings' | 'security';
  action: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

// Mock activity data
const mockActivity: ActivityEvent[] = [
  {
    id: '1',
    type: 'data',
    action: 'Viewed Records',
    description: 'Viewed 12 new technology records from the dashboard',
    timestamp: '2024-01-15T10:30:00Z',
    metadata: { count: 12, category: 'Technology' }
  },
  {
    id: '2',
    type: 'alerts',
    action: 'Email Alert Received',
    description: 'Received alert for new AI & Machine Learning records',
    timestamp: '2024-01-15T09:15:00Z',
    metadata: { alertType: 'category', category: 'AI & Machine Learning' }
  },
  {
    id: '3',
    type: 'profile',
    action: 'Profile Updated',
    description: 'Updated email notification preferences',
    timestamp: '2024-01-15T08:45:00Z'
  },
  {
    id: '4',
    type: 'data',
    action: 'Search Performed',
    description: 'Searched for "blockchain technology" in records',
    timestamp: '2024-01-14T16:20:00Z',
    metadata: { query: 'blockchain technology', results: 8 }
  },
  {
    id: '5',
    type: 'settings',
    action: 'Alert Preferences Updated',
    description: 'Modified category filters for Healthcare and Finance',
    timestamp: '2024-01-14T14:30:00Z',
    metadata: { categories: ['Healthcare', 'Finance'] }
  },
  {
    id: '6',
    type: 'security',
    action: 'Login Session',
    description: 'Logged in from new device (Chrome on Windows)',
    timestamp: '2024-01-14T09:00:00Z',
    metadata: { device: 'Chrome on Windows', ip: '192.168.1.1' }
  },
  {
    id: '7',
    type: 'data',
    action: 'Record Exported',
    description: 'Exported 25 finance records to CSV format',
    timestamp: '2024-01-13T15:45:00Z',
    metadata: { format: 'CSV', count: 25, category: 'Finance' }
  },
  {
    id: '8',
    type: 'alerts',
    action: 'Alert Subscription',
    description: 'Subscribed to alerts for Biotechnology category',
    timestamp: '2024-01-13T11:20:00Z',
    metadata: { category: 'Biotechnology' }
  }
];

const Activity: React.FC = () => {
  const [activities, setActivities] = useState<ActivityEvent[]>(mockActivity);
  const [filter, setFilter] = useState<'all' | 'profile' | 'alerts' | 'data' | 'settings' | 'security'>('all');

  const filteredActivities = activities.filter(activity => 
    filter === 'all' || activity.type === filter
  );

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'profile':
        return User;
      case 'alerts':
        return Bell;
      case 'data':
        return Database;
      case 'settings':
        return Settings;
      case 'security':
        return Eye;
      default:
        return ActivityIcon;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'profile':
        return 'text-blue-500';
      case 'alerts':
        return 'text-yellow-500';
      case 'data':
        return 'text-green-500';
      case 'settings':
        return 'text-purple-500';
      case 'security':
        return 'text-red-500';
      default:
        return 'text-muted-foreground';
    }
  };

  const getActivityBadgeVariant = (type: string) => {
    switch (type) {
      case 'profile':
        return 'default';
      case 'alerts':
        return 'secondary';
      case 'data':
        return 'outline';
      case 'settings':
        return 'secondary';
      case 'security':
        return 'destructive';
      default:
        return 'outline';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInHours < 48) return 'Yesterday';
    return date.toLocaleDateString();
  };

  const formatFullDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const activityTypeLabels = {
    all: 'All Activity',
    profile: 'Profile',
    alerts: 'Alerts',
    data: 'Data Access',
    settings: 'Settings',
    security: 'Security'
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                <ActivityIcon className="h-8 w-8 text-primary" />
                Activity Log
              </h1>
              <p className="text-muted-foreground mt-2">
                Track your account activity and system interactions
              </p>
            </div>
          </div>
          
          {/* Filter Controls */}
          <div className="flex items-center gap-4">
            <Select value={filter} onValueChange={(value: any) => setFilter(value)}>
              <SelectTrigger className="w-[180px]">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(activityTypeLabels).map(([key, label]) => (
                  <SelectItem key={key} value={key}>
                    {label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Badge variant="outline" className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              {filteredActivities.length} events
            </Badge>
          </div>
        </div>

        {/* Activity Timeline */}
        <div className="space-y-4">
          {filteredActivities.length === 0 ? (
            <Card className="text-center py-12">
              <CardContent>
                <ActivityIcon className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <CardTitle className="text-muted-foreground mb-2">No activity found</CardTitle>
                <CardDescription>
                  No activities match your current filter selection.
                </CardDescription>
              </CardContent>
            </Card>
          ) : (
            filteredActivities.map((activity, index) => {
              const Icon = getActivityIcon(activity.type);
              const iconColor = getActivityColor(activity.type);
              const badgeVariant = getActivityBadgeVariant(activity.type);
              
              return (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex items-start gap-4">
                        {/* Icon */}
                        <div className={`flex-shrink-0 mt-1 ${iconColor}`}>
                          <Icon className="h-5 w-5" />
                        </div>
                        
                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-2">
                              <h3 className="font-semibold text-foreground">
                                {activity.action}
                              </h3>
                              <Badge variant={badgeVariant as any} className="text-xs">
                                {activity.type}
                              </Badge>
                            </div>
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Clock className="h-3 w-3" />
                              {formatTimestamp(activity.timestamp)}
                            </div>
                          </div>
                          
                          <p className="text-muted-foreground mb-3">
                            {activity.description}
                          </p>
                          
                          {/* Metadata */}
                          {activity.metadata && (
                            <div className="flex flex-wrap gap-2">
                              {Object.entries(activity.metadata).map(([key, value]) => (
                                <Badge key={key} variant="outline" className="text-xs">
                                  {key}: {String(value)}
                                </Badge>
                              ))}
                            </div>
                          )}
                          
                          {/* Full timestamp on hover/click */}
                          <div className="mt-3 text-xs text-muted-foreground">
                            {formatFullDate(activity.timestamp)}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })
          )}
        </div>
        
        {/* Load More Button */}
        {filteredActivities.length > 0 && (
          <div className="text-center mt-8">
            <Button variant="outline" disabled>
              <Download className="h-4 w-4 mr-2" />
              Export Activity Log
            </Button>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Activity;