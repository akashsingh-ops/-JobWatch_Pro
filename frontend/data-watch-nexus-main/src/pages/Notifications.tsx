import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { useToast } from '@/hooks/use-toast';
import { notificationsService, Notification, NotificationsResponse } from '@/services/api/notifications';
import {
  Bell,
  Mail,
  Filter,
  CheckCircle2,
  Clock,
  AlertCircle,
  ExternalLink,
  MoreHorizontal,
  RefreshCw
} from 'lucide-react';
import { motion } from 'framer-motion';

const Notifications: React.FC = () => {
  const { toast } = useToast();
  const [notificationsData, setNotificationsData] = useState<NotificationsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');

  const notifications = notificationsData?.notifications ?? [];
  const unreadCount = notificationsData?.unread_count ?? 0;
  const filteredNotifications =
    filter === 'unread' ? notifications.filter((n) => !n.is_read) : notifications;

  // Load notifications
  const loadNotifications = async (includeRead: boolean = true) => {
    try {
      const data = await notificationsService.getNotifications(includeRead, 50);
      setNotificationsData(data);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to load notifications',
        variant: 'destructive'
      });
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadNotifications(filter === 'all');
  }, [filter]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadNotifications(filter === 'all');
  };

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await notificationsService.markAsRead(notificationId);
      // Update local state
      if (notificationsData) {
        setNotificationsData({
          ...notificationsData,
          notifications: notificationsData.notifications.map(n =>
            n.id === notificationId ? { ...n, is_read: true, read_at: new Date().toISOString() } : n
          ),
          unread_count: Math.max(0, notificationsData.unread_count - 1)
        });
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to mark notification as read',
        variant: 'destructive'
      });
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationsService.markAllAsRead();
      // Update local state
      if (notificationsData) {
        setNotificationsData({
          ...notificationsData,
          notifications: notificationsData.notifications.map(n => ({
            ...n,
            is_read: true,
            read_at: n.read_at || new Date().toISOString()
          })),
          unread_count: 0
        });
      }
      toast({
        title: 'Success',
        description: 'All notifications marked as read'
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to mark all notifications as read',
        variant: 'destructive'
      });
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'job_alert':
        return <Bell className="h-4 w-4" />;
      case 'application_update':
        return <Mail className="h-4 w-4" />;
      case 'system':
        return <AlertCircle className="h-4 w-4" />;
      default:
        return <Bell className="h-4 w-4" />;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'job_alert':
        return 'text-blue-600';
      case 'application_update':
        return 'text-green-600';
      case 'system':
        return 'text-orange-600';
      default:
        return 'text-gray-600';
    }
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));

    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center space-y-4">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto" />
            <p className="text-muted-foreground">Loading notifications...</p>
          </div>
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
              <Select value={filter} onValueChange={(value: 'all' | 'unread') => setFilter(value)}>
                <SelectTrigger className="w-[140px]">
                  <Filter className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All</SelectItem>
                  <SelectItem value="unread">Unread</SelectItem>
                </SelectContent>
              </Select>

              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="flex items-center gap-2"
              >
                <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
            </div>

            {unreadCount > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleMarkAllAsRead}
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
              
              return (
                <motion.div
                  key={notification.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card
                    className={`transition-all hover:shadow-md cursor-pointer ${
                      !notification.is_read ? 'bg-primary/5 border-primary/20' : ''
                    }`}
                    onClick={() => !notification.is_read && handleMarkAsRead(notification.id)}
                  >
                    <CardContent className="p-6">
                      <div className="flex items-start gap-4">
                        {/* Icon */}
                        <div className={`flex-shrink-0 mt-1 ${getNotificationColor(notification.notification_type)}`}>
                          {getNotificationIcon(notification.notification_type)}
                        </div>
                        
                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className={`font-semibold ${!notification.is_read ? 'text-foreground' : 'text-muted-foreground'}`}>
                              {notification.title}
                            </h3>
                            <div className="flex items-center gap-2">
                              <Badge variant="outline" className="text-xs">
                                {notification.notification_type}
                              </Badge>
                              {!notification.is_read && (
                                <Badge variant="secondary" className="text-xs">New</Badge>
                              )}
                            </div>
                          </div>
                          
                          <p className="text-muted-foreground mb-3">
                            {notification.message}
                          </p>

                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Clock className="h-3 w-3" />
                              {formatTimeAgo(notification.created_at)}
                            </div>
                            
                            {notification.action_url && (
                              <Button 
                                variant="ghost" 
                                size="sm" 
                                className="text-xs h-8"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  // Navigate to actionUrl in real implementation
                                  window.open(notification.action_url!, '_blank');
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