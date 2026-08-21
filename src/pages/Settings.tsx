import React, { useState } from 'react';
import { Settings as SettingsIcon, Bell, Shield, Database, Trash2, CheckCircle2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/hooks/use-toast';

const Settings: React.FC = () => {
  const { toast } = useToast();
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [salaryFilter, setSalaryFilter] = useState(true);
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [telemetryLogs, setTelemetryLogs] = useState(true);

  const handleClearCache = () => {
    localStorage.removeItem('jobwatch_jobs');
    toast({
      title: 'Local data cache reset',
      description: 'Mock catalog refreshed with latest seed data.',
    });
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-6 max-w-4xl">
      <div className="border-b pb-6">
        <div className="flex items-center gap-2">
          <SettingsIcon className="h-6 w-6 text-primary" />
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">System Settings</h1>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          Customize telemetry scanning, alert frequencies, and storage settings.
        </p>
      </div>

      <div className="space-y-6">
        {/* Filtering rules */}
        <Card className="border shadow-sm">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-base font-semibold border-b pb-2 flex items-center gap-2">
              <Bell className="h-4 w-4 text-primary" /> Notification & Scanning Rules
            </h2>

            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium">Auto-send Email Alerts</div>
                  <div className="text-xs text-muted-foreground">Receive instant notices when 90%+ match postings occur</div>
                </div>
                <Switch checked={emailAlerts} onCheckedChange={setEmailAlerts} />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium">Require Verified Salary Ranges</div>
                  <div className="text-xs text-muted-foreground">Filter out postings without explicit compensation disclosures</div>
                </div>
                <Switch checked={salaryFilter} onCheckedChange={setSalaryFilter} />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium">Remote-first Priority</div>
                  <div className="text-xs text-muted-foreground">Boost distributed/remote postings at the top of feeds</div>
                </div>
                <Switch checked={remoteOnly} onCheckedChange={setRemoteOnly} />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Data storage */}
        <Card className="border shadow-sm">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-base font-semibold border-b pb-2 flex items-center gap-2">
              <Database className="h-4 w-4 text-primary" /> Data & Local Persistence
            </h2>

            <div className="flex items-center justify-between pt-2">
              <div>
                <div className="text-sm font-medium">Reset Mock Catalog Data</div>
                <div className="text-xs text-muted-foreground">Restore initial state and sample roles in preview</div>
              </div>
              <Button variant="outline" size="sm" onClick={handleClearCache}>
                <Trash2 className="mr-2 h-4 w-4 text-destructive" /> Reset Cache
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Settings;
