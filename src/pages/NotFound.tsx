import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Briefcase } from 'lucide-react';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="container mx-auto px-4 py-24 text-center max-w-md space-y-4">
      <div className="flex justify-center">
        <div className="h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
          <Briefcase className="h-8 w-8" />
        </div>
      </div>
      <h1 className="text-4xl font-extrabold tracking-tight">404</h1>
      <h2 className="text-lg font-semibold">Page Not Found</h2>
      <p className="text-sm text-muted-foreground">
        The page you requested could not be found or has moved.
      </p>
      <Button className="btn-gradient" onClick={() => navigate('/dashboard')}>
        Back to Dashboard
      </Button>
    </div>
  );
};

export default NotFound;
