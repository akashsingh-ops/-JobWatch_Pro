import React from 'react';
import { Briefcase, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t bg-muted/30 py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
              <Briefcase className="h-4 w-4" />
            </div>
            <span className="font-semibold text-sm">JobWatch Pro</span>
            <span className="text-xs text-muted-foreground">© {new Date().getFullYear()} All rights reserved.</span>
          </div>

          <div className="flex items-center gap-6 text-xs text-muted-foreground">
            <Link to="/dashboard" className="hover:text-foreground transition-colors">
              Explore Jobs
            </Link>
            <Link to="/notifications" className="hover:text-foreground transition-colors">
              Alerts
            </Link>
            <Link to="/help" className="hover:text-foreground transition-colors">
              Help Center
            </Link>
            <span className="flex items-center gap-1 text-primary">
              <Shield className="h-3.5 w-3.5" /> Verified Telemetry
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
