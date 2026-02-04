/**
 * API Constants and Configuration
 */

export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
    REFRESH: '/auth/refresh',
  },

  // Jobs
  JOBS: {
    LIST: '/jobs/',
    DETAIL: (id: string) => `/jobs/${id}`,
    SAVE: '/jobs/save',
    UNSAVE: (id: string) => `/jobs/${id}/save`,
    SAVED_LIST: '/jobs/saved/list',
    CATEGORIES: '/jobs/meta/categories',
    TYPES: '/jobs/meta/types',
    APPLY: (id: string) => `/jobs/${id}/apply`,
  },

  // Applications
  APPLICATIONS: {
    LIST: '/applications/',
    DETAIL: (id: string) => `/applications/${id}`,
    WITHDRAW: (id: string) => `/applications/${id}/withdraw`,
  },

  // Recommendations
  RECOMMENDATIONS: {
    JOBS: '/recommendations/jobs',
    TRENDING: '/recommendations/trending',
    FEEDBACK: '/recommendations/feedback',
  },

  // User Profile
  USERS: {
    PROFILE: '/users/profile',
    PREFERENCES: '/users/preferences',
    UPLOAD_RESUME: '/users/upload-resume',
  },

  // Notifications
  NOTIFICATIONS: {
    LIST: '/notifications/',
    MARK_READ: (id: string) => `/notifications/${id}/read`,
    UNREAD_COUNT: '/notifications/unread/count',
  },

  // Analytics
  ANALYTICS: {
    JOB_VIEW: '/analytics/job-view',
    SEARCH: '/analytics/search',
  },
} as const;

export const API_CONFIG = {
  TIMEOUT: 30000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
} as const;

export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_LIMIT: 12,
  MAX_LIMIT: 100,
} as const;
