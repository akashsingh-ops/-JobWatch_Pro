import React from 'react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { AlertTriangle, RefreshCw, Wifi, WifiOff } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ErrorMessageProps {
  title?: string;
  message: string;
  type?: 'error' | 'warning' | 'network' | 'auth';
  action?: {
    label: string;
    onClick: () => void;
  };
  retry?: () => void;
  className?: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  title,
  message,
  type = 'error',
  action,
  retry,
  className
}) => {
  const getIcon = () => {
    switch (type) {
      case 'network':
        return <WifiOff className="h-4 w-4" />;
      case 'auth':
        return <AlertTriangle className="h-4 w-4" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return <AlertTriangle className="h-4 w-4" />;
    }
  };

  const getVariant = () => {
    switch (type) {
      case 'warning':
        return 'default';
      default:
        return 'destructive';
    }
  };

  return (
    <Alert variant={getVariant()} className={cn('mb-4', className)}>
      {getIcon()}
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {title && <AlertTitle>{title}</AlertTitle>}
          <AlertDescription>{message}</AlertDescription>
        </div>
        <div className="flex gap-2 ml-4">
          {retry && (
            <Button
              variant="outline"
              size="sm"
              onClick={retry}
              className="shrink-0"
            >
              <RefreshCw className="h-3 w-3 mr-1" />
              Retry
            </Button>
          )}
          {action && (
            <Button
              variant="outline"
              size="sm"
              onClick={action.onClick}
              className="shrink-0"
            >
              {action.label}
            </Button>
          )}
        </div>
      </div>
    </Alert>
  );
};

// Specific error components for common scenarios
export const NetworkError: React.FC<{ retry?: () => void }> = ({ retry }) => (
  <ErrorMessage
    title="Connection Error"
    message="Unable to connect to our servers. Please check your internet connection and try again."
    type="network"
    retry={retry}
  />
);

export const AuthError: React.FC<{ onLogin?: () => void }> = ({ onLogin }) => (
  <ErrorMessage
    title="Authentication Required"
    message="You need to be logged in to access this feature."
    type="auth"
    action={onLogin ? { label: 'Sign In', onClick: onLogin } : undefined}
  />
);

export const ServerError: React.FC<{ retry?: () => void }> = ({ retry }) => (
  <ErrorMessage
    title="Server Error"
    message="Something went wrong on our end. Please try again later."
    type="error"
    retry={retry}
  />
);

export const NotFoundError: React.FC = () => (
  <ErrorMessage
    title="Not Found"
    message="The requested resource could not be found."
    type="warning"
  />
);

export const PermissionError: React.FC = () => (
  <ErrorMessage
    title="Access Denied"
    message="You don't have permission to access this resource."
    type="warning"
  />
);

// Toast-style error (for use with toast notifications)
export const ToastError: React.FC<{
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
}> = ({ title, description, action }) => (
  <div className="space-y-2">
    <div className="font-medium">{title}</div>
    {description && <div className="text-sm opacity-90">{description}</div>}
    {action && (
      <Button
        variant="outline"
        size="sm"
        onClick={action.onClick}
        className="h-6 px-2 text-xs"
      >
        {action.label}
      </Button>
    )}
  </div>
);
