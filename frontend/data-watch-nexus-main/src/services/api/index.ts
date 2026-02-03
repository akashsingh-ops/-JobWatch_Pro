/**
 * API Services Index
 * Centralized export of all API services
 */

export { authService } from './auth';
export type { LoginRequest, RegisterRequest, User, AuthResponse } from './auth';

export { jobsService } from './jobs';
export type {
  JobFilters,
  Job,
  JobsResponse,
  JobApplication,
  JobApplicationRequest,
  Salary
} from './jobs';

export { usersService } from './users';
export type { UserProfile, UpdateProfileRequest, UpdatePreferencesRequest } from './users';

export { notificationsService } from './notifications';
export type { Notification, NotificationsResponse } from './notifications';

export { recordsService } from './records';
export type { Record, RecordsFilters, RecordsResponse } from './records';

// Re-export API client utilities
export { apiClient, apiUtils } from '@/api/client';
export type { ApiResponse, ApiError } from '@/api/client';
