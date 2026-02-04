/**
 * Environment configuration for the frontend application
 * Uses Vite environment variables for proper build-time replacement
 */

interface AppConfig {
  // API Configuration
  api: {
    baseUrl: string;
    timeout: number;
  };

  // Application Settings
  app: {
    name: string;
    version: string;
    environment: string;
  };

  // Feature Flags
  features: {
    analytics: boolean;
    errorReporting: boolean;
    pwa: boolean;
  };

  // UI Configuration
  ui: {
    defaultPageSize: number;
    maxFileSize: number;
    supportedFileTypes: string[];
  };

  // External Services
  services: {
    sentryDsn?: string;
    googleAnalyticsId?: string;
  };
}

const getEnvVar = (key: string, defaultValue?: string): string => {
  // Vite prefixes environment variables with VITE_
  const envKey = key.startsWith('VITE_') ? key : `VITE_${key}`;
  const value = import.meta.env[envKey] || defaultValue;

  if (!value && !defaultValue) {
    console.warn(`Environment variable ${envKey} is not set and has no default value`);
  }

  return value || '';
};

const getEnvBool = (key: string, defaultValue: boolean = false): boolean => {
  const value = getEnvVar(key);
  if (!value) return defaultValue;

  return value.toLowerCase() === 'true' || value === '1';
};

const getEnvNumber = (key: string, defaultValue: number = 0): number => {
  const value = getEnvVar(key);
  const parsed = parseInt(value, 10);
  return isNaN(parsed) ? defaultValue : parsed;
};

const getEnvArray = (key: string, defaultValue: string[] = []): string[] => {
  const value = getEnvVar(key);
  if (!value) return defaultValue;

  return value.split(',').map(item => item.trim());
};

// Application configuration
export const config: AppConfig = {
  api: {
    baseUrl: getEnvVar('API_BASE_URL', 'http://localhost:8000/api/v1'),
    timeout: getEnvNumber('API_TIMEOUT', 10000),
  },

  app: {
    name: getEnvVar('APP_NAME', 'Data Watch Nexus'),
    version: getEnvVar('APP_VERSION', '1.0.0'),
    environment: getEnvVar('ENVIRONMENT', 'development'),
  },

  features: {
    analytics: getEnvBool('ENABLE_ANALYTICS', false),
    errorReporting: getEnvBool('ENABLE_ERROR_REPORTING', false),
    pwa: getEnvBool('ENABLE_PWA', false),
  },

  ui: {
    defaultPageSize: getEnvNumber('DEFAULT_PAGE_SIZE', 12),
    maxFileSize: getEnvNumber('MAX_FILE_SIZE', 10485760), // 10MB
    supportedFileTypes: getEnvArray('SUPPORTED_FILE_TYPES', ['pdf', 'doc', 'docx', 'txt']),
  },

  services: {
    sentryDsn: getEnvVar('SENTRY_DSN') || undefined,
    googleAnalyticsId: getEnvVar('GOOGLE_ANALYTICS_ID') || undefined,
  },
};

// Validation
if (!config.api.baseUrl) {
  throw new Error('API_BASE_URL is required. Please set VITE_API_BASE_URL in your environment.');
}

// Development helpers
export const isDevelopment = config.app.environment === 'development';
export const isProduction = config.app.environment === 'production';
export const isStaging = config.app.environment === 'staging';

// Logging configuration based on environment
export const logLevel = isDevelopment ? 'debug' : 'warn';

// Export individual config values for convenience
export const {
  api: { baseUrl: API_BASE_URL, timeout: API_TIMEOUT },
  app: { name: APP_NAME, version: APP_VERSION },
  ui: { defaultPageSize: DEFAULT_PAGE_SIZE, maxFileSize: MAX_FILE_SIZE, supportedFileTypes: SUPPORTED_FILE_TYPES },
} = config;
