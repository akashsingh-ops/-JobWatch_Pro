/**
 * Notifications API service
 */

import { apiClient } from '@/api/client';

export interface Notification {
  id: number;
  user_id: string;
  title: string;
  message: string;
  notification_type: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
  action_url?: string;
  action_text?: string;
  expires_at?: string;
}

export interface NotificationsResponse {
  notifications: Notification[];
  total: number;
  unread_count: number;
}

export const notificationsService = {
  /**
   * Get user notifications
   */
  async getNotifications(
    includeRead: boolean = true,
    limit: number = 50
  ): Promise<NotificationsResponse> {
    const params = new URLSearchParams();
    params.append('include_read', includeRead.toString());
    params.append('limit', limit.toString());

    const response = await apiClient.get<NotificationsResponse>(`/notifications/?${params.toString()}`);
    return response.data;
  },

  /**
   * Mark notification as read
   */
  async markAsRead(notificationId: number): Promise<Notification> {
    const response = await apiClient.put<Notification>(`/notifications/${notificationId}/read`);
    return response.data;
  },

  /**
   * Mark all notifications as read
   */
  async markAllAsRead(): Promise<{ message: string }> {
    const response = await apiClient.put<{ message: string }>('/notifications/mark-all-read');
    return response.data;
  },

  /**
   * Get unread notification count
   */
  async getUnreadCount(): Promise<{ unread_count: number }> {
    const response = await apiClient.get<{ unread_count: number }>('/notifications/unread/count');
    return response.data;
  },

  /**
   * Delete notification
   */
  async deleteNotification(notificationId: number): Promise<{ message: string }> {
    const response = await apiClient.delete<{ message: string }>(`/notifications/${notificationId}`);
    return response.data;
  },

  /**
   * Get notification preferences
   */
  async getPreferences(): Promise<{
    email_notifications: boolean;
    sms_notifications: boolean;
    push_notifications: boolean;
  }> {
    const response = await apiClient.get('/notifications/preferences');
    return response.data;
  },

  /**
   * Update notification preferences
   */
  async updatePreferences(preferences: {
    email_notifications?: boolean;
    sms_notifications?: boolean;
    push_notifications?: boolean;
  }): Promise<{ message: string }> {
    const response = await apiClient.put<{ message: string }>('/notifications/preferences', preferences);
    return response.data;
  }
};
