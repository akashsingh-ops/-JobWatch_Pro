import React, { useState } from 'react';
import { 
  Bell, 
  CheckCheck, 
  Sparkles, 
  Trash2, 
  ExternalLink,
  Briefcase,
  Layers,
  SlidersHorizontal
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/hooks/use-toast';

interface NotificationItem {
  id: string;
  title: string;
  message: string;
  date: string;
  read: boolean;
  category: string;
  type: 'job_alert' | 'system' | 'digest';
}

const initialNotifications: NotificationItem[] = [
  {
    id: 'n-1',
    title: 'New Senior Full Stack Role',
    message: 'Nexus Technologies posted a Senior Full Stack Engineer role matching your engineering preferences.',
    date: '10 minutes ago',
    read: false,
    category: 'Engineering',
    type: 'job_alert',
  },
  {
    id: 'n-2',
    title: 'AI / ML Engineer Alert',
    message: 'Cortex Data Labs published a high-salary remote opening in AI & Machine Learning.',
    date: '2 hours ago',
    read: false,
    category: 'AI & Data Science',
    type: 'job_alert',
  },
  {
    id: 'n-3',
    title: 'Daily Telemetry Digest',
    message: '14 new tech positions were cataloged in your monitored categories over the last 24 hours.',
    date: '1 day ago',
    read: true,
    category: 'Digest',
    type: 'digest',
  },
];

const Notifications: React.FC = () => {
  const { toast } = useToast();
  const [notifications, setNotifications] = useState<NotificationItem[]>(initialNotifications);
  const [instantAlerts, setInstantAlerts] = useState(true);
  const [dailyDigest, setDailyDigest] = useState(true);

  const markAllRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
    toast({ title: 'All notifications marked as read' });
  };

  const clearAll = () => {
    setNotifications([]);
    toast({ title: 'Notifications cleared' });
  };

  const markOne = (id: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
  };

  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <div className="container mx-auto px-4 py-8 space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-6">
        <div>
          <div className="flex items-center gap-2">
            <Bell className="h-6 w-6 text-primary" />
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight">Telemetry & Job Alerts</h1>
            {unreadCount > 0 && (
              <Badge variant="default" className="ml-2">
                {unreadCount} New
              </Badge>
            )}
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            Real-time notifications for roles matching your search filters and skill profile.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {unreadCount > 0 && (
            <Button variant="outline" size="sm" onClick={markAllRead}>
              <CheckCheck className="mr-1.5 h-4 w-4" /> Mark all read
            </Button>
          )}
          {notifications.length > 0 && (
            <Button variant="ghost" size="sm" onClick={clearAll} className="text-muted-foreground hover:text-destructive">
              <Trash2 className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left 2 Cols: Notifications Feed */}
        <div className="md:col-span-2 space-y-3">
          {notifications.length === 0 ? (
            <Card className="text-center py-16 p-6">
              <div className="flex justify-center mb-3">
                <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center text-muted-foreground">
                  <Bell className="h-6 w-6" />
                </div>
              </div>
              <h3 className="font-semibold text-base">You're all caught up!</h3>
              <p className="text-xs text-muted-foreground mt-1">
                No active notifications. When new matching jobs are published, they will appear here.
              </p>
            </Card>
          ) : (
            notifications.map((item) => (
              <Card
                key={item.id}
                onClick={() => markOne(item.id)}
                className={`cursor-pointer transition-all hover:border-primary/40 ${
                  !item.read ? 'border-primary/30 bg-primary/[0.02]' : 'bg-card'
                }`}
              >
                <CardContent className="p-4 flex items-start gap-3.5">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary mt-0.5">
                    {item.type === 'job_alert' ? (
                      <Briefcase className="h-4 w-4" />
                    ) : (
                      <Layers className="h-4 w-4" />
                    )}
                  </div>

                  <div className="flex-1 space-y-1">
                    <div className="flex items-center justify-between gap-2">
                      <h4 className={`text-sm leading-none ${!item.read ? 'font-semibold text-foreground' : 'font-medium text-muted-foreground'}`}>
                        {item.title}
                      </h4>
                      <span className="text-[11px] text-muted-foreground whitespace-nowrap">
                        {item.date}
                      </span>
                    </div>

                    <p className="text-xs text-muted-foreground leading-relaxed">
                      {item.message}
                    </p>

                    <div className="flex items-center gap-2 pt-1">
                      <Badge variant="secondary" className="text-[10px] py-0">
                        {item.category}
                      </Badge>
                      {!item.read && (
                        <span className="inline-block h-2 w-2 rounded-full bg-primary" />
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Right Col: Preferences */}
        <div className="space-y-6">
          <Card className="border shadow-sm">
            <CardContent className="p-5 space-y-4">
              <div className="flex items-center gap-2 font-semibold text-sm">
                <SlidersHorizontal className="h-4 w-4 text-primary" /> Alert Preferences
              </div>

              <div className="space-y-4 pt-2">
                <div className="flex items-center justify-between gap-2">
                  <div className="space-y-0.5">
                    <div className="text-xs font-medium">Instant Notifications</div>
                    <div className="text-[11px] text-muted-foreground">Alert when high-match jobs go live</div>
                  </div>
                  <Switch
                    checked={instantAlerts}
                    onCheckedChange={(checked) => {
                      setInstantAlerts(checked);
                      toast({ title: `Instant alerts ${checked ? 'enabled' : 'disabled'}` });
                    }}
                  />
                </div>

                <div className="flex items-center justify-between gap-2">
                  <div className="space-y-0.5">
                    <div className="text-xs font-medium">Daily Telemetry Digest</div>
                    <div className="text-[11px] text-muted-foreground">Summary email every morning</div>
                  </div>
                  <Switch
                    checked={dailyDigest}
                    onCheckedChange={(checked) => {
                      setDailyDigest(checked);
                      toast({ title: `Daily digest ${checked ? 'enabled' : 'disabled'}` });
                    }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Notifications;
