import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { 
  Bell, 
  Mail, 
  Filter, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  ExternalLink,
  MoreHorizontal
} from 'lucide-react';
import { motion } from 'framer-motion';

interface Notification {
  id: string;
  title: string;
  description: string;
  type: 'alert' | 'digest' | 'system';
  date: string;
  read: boolean;
  category?: string;
  actionUrl?: string;
}

// Mock notifications data
const mockNotifications: Notification[] = [
  {
    id: '1',
    title: 'New Technology Records Available',
    description: '15 new records matching your "AI & Machine Learning" category have been added.',
    type: 'alert',
    date: '2024-01-15T10:30:00Z',
    read: false,
    category: 'Technology',
    actionUrl: '/dashboard?category=technology'
  },
  {
    id: '2',
    title: 'Daily Digest - Market Analysis',
    description: 'Your daily digest contains 8 new market analysis reports and industry insights.',
    type: 'digest',
    date: '2024-01-15T08:00:00Z',
    read: false,
    category: 'Finance'
  },
  {
    id: '3',
    title: 'Profile Settings Updated',
    description: 'Your email notification preferences have been successfully updated.',
    type: 'system',
    date: '2024-01-14T16:45:00Z',
    read: true
  },
  {
    id: '4',
    title: 'Healthcare Research Alert',
    description: '3 new research papers on biotechnology have been published in your monitored journals.',
    type: 'alert',
    date: '2024-01-14T14:20:00Z',
    read: true,
    category: 'Healthcare',
    actionUrl: '/dashboard?category=healthcare'
  },
  {
    id: '5',
    title: 'Weekly Summary Available',
    description: 'Your weekly analytics summary for data consumption and trending categories is ready.',
    type: 'digest',
    date: '2024-01-14T09:00:00Z',
    read: true
  }
];

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications);
  const [filter, setFilter] = useState<'all' | 'unread' | 'read'>('all');

  const filteredNotifications = notifications.filter(notification => {
    if (filter === 'unread') return !notification.read;
    if (filter === 'read') return notification.read;
    return true;
  });

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })));
  };

  const markAsRead = (id: string) => {
    setNotifications(notifications.map(n => 
      n.id === id ? { ...n, read: true } : n
    ));
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'alert':
        return AlertCircle;
      case 'digest':
        return Mail;
      case 'system':
        return Bell;
      default:
        return Bell;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'alert':
        return 'text-destructive';
      case 'digest':
        return 'text-primary';
      case 'system':
        return 'text-muted-foreground';
      default:
        return 'text-muted-foreground';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInHours < 48) return 'Yesterday';
    return date.toLocaleDateString();
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
                <Bell className="h-8 w-8 text-primary" />
                Notifications
              </h1>
              <p className="text-muted-foreground mt-2">
                Stay updated with your latest data alerts and system updates
              </p>
            </div>
            <div className="flex items-center gap-3">
              {unreadCount > 0 && (
                <Badge variant="secondary" className="flex items-center gap-1">
                  {unreadCount} unread
                </Badge>
              )}
            </div>
          </div>
          
          {/* Controls */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Select value={filter} onValueChange={(value: 'all' | 'unread' | 'read') => setFilter(value)}>
                <SelectTrigger className="w-[140px]">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All</SelectItem>
                  <SelectItem value="unread">Unread</SelectItem>
                  <SelectItem value="read">Read</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            {unreadCount > 0 && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={markAllAsRead}
                className="flex items-center gap-2"
              >
                <CheckCircle2 className="h-4 w-4" />
                Mark all as read
              </Button>
            )}
          </div>
        </div>

        {/* Notifications List */}
        <div className="space-y-4">
          {filteredNotifications.length === 0 ? (
            <Card className="text-center py-12">
              <CardContent>
                <Bell className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <CardTitle className="text-muted-foreground mb-2">No notifications</CardTitle>
                <CardDescription>
                  {filter === 'unread' 
                    ? "You're all caught up! No unread notifications." 
                    : "You don't have any notifications yet."}
                </CardDescription>
              </CardContent>
            </Card>
          ) : (
            filteredNotifications.map((notification, index) => {
              const Icon = getNotificationIcon(notification.type);
              const iconColor = getNotificationColor(notification.type);
              
              return (
                <motion.div
                  key={notification.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card 
                    className={`transition-all hover:shadow-md cursor-pointer ${
                      !notification.read ? 'bg-primary/5 border-primary/20' : ''
                    }`}
                    onClick={() => !notification.read && markAsRead(notification.id)}
                  >
                    <CardContent className="p-6">
                      <div className="flex items-start gap-4">
                        {/* Icon */}
                        <div className={`flex-shrink-0 mt-1 ${iconColor}`}>
                          <Icon className="h-5 w-5" />
                        </div>
                        
                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className={`font-semibold ${!notification.read ? 'text-foreground' : 'text-muted-foreground'}`}>
                              {notification.title}
                            </h3>
                            <div className="flex items-center gap-2">
                              {notification.category && (
                                <Badge variant="outline" className="text-xs">
                                  {notification.category}
                                </Badge>
                              )}
                              {!notification.read && (
                                <div className="w-2 h-2 bg-primary rounded-full flex-shrink-0" />
                              )}
                            </div>
                          </div>
                          
                          <p className="text-muted-foreground mb-3">
                            {notification.description}
                          </p>
                          
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Clock className="h-3 w-3" />
                              {formatDate(notification.date)}
                            </div>
                            
                            {notification.actionUrl && (
                              <Button 
                                variant="ghost" 
                                size="sm" 
                                className="text-xs h-8"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  // Navigate to actionUrl in real implementation
                                  console.log('Navigate to:', notification.actionUrl);
                                }}
                              >
                                View Details
                                <ExternalLink className="h-3 w-3 ml-1" />
                              </Button>
                            )}
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
        
        {/* Load More Button (placeholder for pagination) */}
        {filteredNotifications.length > 0 && (
          <div className="text-center mt-8">
            <Button variant="outline" disabled>
              Load More Notifications
            </Button>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Notifications;