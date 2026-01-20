import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Users, 
  Database, 
  Bell, 
  TrendingUp, 
  Activity,
  Calendar,
  ArrowUpRight,
  ArrowDownRight,
  BarChart3,
  PieChart
} from 'lucide-react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, PieChart as RechartsPieChart, Cell } from 'recharts';

// Mock data for charts
const dailyStats = [
  { day: 'Mon', users: 45, records: 120, alerts: 89 },
  { day: 'Tue', users: 52, records: 135, alerts: 94 },
  { day: 'Wed', users: 48, records: 110, alerts: 76 },
  { day: 'Thu', users: 61, records: 145, alerts: 103 },
  { day: 'Fri', users: 55, records: 132, alerts: 87 },
  { day: 'Sat', users: 38, records: 98, alerts: 65 },
  { day: 'Sun', users: 42, records: 105, alerts: 71 }
];

const categoryData = [
  { name: 'Technology', value: 35, color: 'hsl(var(--primary))' },
  { name: 'Finance', value: 25, color: 'hsl(var(--secondary))' },
  { name: 'Healthcare', value: 20, color: 'hsl(var(--accent))' },
  { name: 'Education', value: 12, color: 'hsl(var(--muted-foreground))' },
  { name: 'Other', value: 8, color: 'hsl(var(--border))' }
];

const AdminDashboard: React.FC = () => {
  const metrics = [
    {
      title: 'Total Users',
      value: '2,847',
      change: '+12.5%',
      changeType: 'positive',
      icon: Users,
      description: 'Active users this month'
    },
    {
      title: 'Records Fetched',
      value: '18,294',
      change: '+8.2%',
      changeType: 'positive', 
      icon: Database,
      description: 'Total records processed today'
    },
    {
      title: 'Notifications Sent',
      value: '5,672',
      change: '-3.1%',
      changeType: 'negative',
      icon: Bell,
      description: 'Alerts delivered today'
    },
    {
      title: 'System Health',
      value: '99.9%',
      change: '+0.1%',
      changeType: 'positive',
      icon: Activity,
      description: 'Uptime last 30 days'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
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
                <BarChart3 className="h-8 w-8 text-primary" />
                Admin Dashboard
              </h1>
              <p className="text-muted-foreground mt-2">
                Monitor system performance and user analytics
              </p>
            </div>
            <Button className="btn-gradient">
              <Calendar className="h-4 w-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metrics.map((metric, index) => {
            const Icon = metric.icon;
            return (
              <motion.div
                key={metric.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Card className="border-0 shadow-lg bg-gradient-to-br from-card to-card/80 hover:shadow-xl transition-all duration-300">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <Icon className="h-5 w-5 text-muted-foreground" />
                      <Badge 
                        variant={metric.changeType === 'positive' ? 'default' : 'destructive'}
                        className="flex items-center gap-1"
                      >
                        {metric.changeType === 'positive' ? (
                          <ArrowUpRight className="h-3 w-3" />
                        ) : (
                          <ArrowDownRight className="h-3 w-3" />
                        )}
                        {metric.change}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <h3 className="text-2xl font-bold">{metric.value}</h3>
                      <p className="text-sm text-muted-foreground">{metric.title}</p>
                      <p className="text-xs text-muted-foreground">{metric.description}</p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Daily Activity Chart */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg bg-gradient-to-br from-card to-card/80">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Weekly Activity
                </CardTitle>
                <CardDescription>
                  User activity, records processed, and alerts sent
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={dailyStats}>
                      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                      <XAxis 
                        dataKey="day" 
                        className="text-muted-foreground"
                      />
                      <YAxis className="text-muted-foreground" />
                      <Bar 
                        dataKey="users" 
                        fill="hsl(var(--primary))" 
                        radius={[4, 4, 0, 0]}
                        name="Users"
                      />
                      <Bar 
                        dataKey="records" 
                        fill="hsl(var(--secondary))" 
                        radius={[4, 4, 0, 0]}
                        name="Records"
                      />
                      <Bar 
                        dataKey="alerts" 
                        fill="hsl(var(--accent))" 
                        radius={[4, 4, 0, 0]}
                        name="Alerts"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Category Distribution */}
          <div>
            <Card className="border-0 shadow-lg bg-gradient-to-br from-card to-card/80">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <PieChart className="h-5 w-5 mr-2" />
                  Categories
                </CardTitle>
                <CardDescription>
                  Record distribution by category
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsPieChart>
                      <RechartsPieChart data={categoryData}>
                        {categoryData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </RechartsPieChart>
                    </RechartsPieChart>
                  </ResponsiveContainer>
                </div>
                <div className="space-y-2 mt-4">
                  {categoryData.map((category, index) => (
                    <div key={category.name} className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: category.color }}
                        />
                        <span>{category.name}</span>
                      </div>
                      <span className="font-medium">{category.value}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Recent Activity */}
        <Card className="border-0 shadow-lg bg-gradient-to-br from-card to-card/80">
          <CardHeader>
            <CardTitle>Recent System Activity</CardTitle>
            <CardDescription>
              Latest events and system operations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { action: 'Data sync completed', time: '2 minutes ago', status: 'success' },
                { action: 'New user registered', time: '5 minutes ago', status: 'info' },
                { action: 'Alert batch sent (1,234 emails)', time: '15 minutes ago', status: 'success' },
                { action: 'Database backup completed', time: '1 hour ago', status: 'success' },
                { action: 'System maintenance scheduled', time: '2 hours ago', status: 'warning' }
              ].map((activity, index) => (
                <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/20">
                  <div className="flex items-center gap-3">
                    <div className={`w-2 h-2 rounded-full ${
                      activity.status === 'success' ? 'bg-green-500' :
                      activity.status === 'warning' ? 'bg-yellow-500' :
                      'bg-blue-500'
                    }`} />
                    <span className="font-medium">{activity.action}</span>
                  </div>
                  <span className="text-sm text-muted-foreground">{activity.time}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default AdminDashboard;