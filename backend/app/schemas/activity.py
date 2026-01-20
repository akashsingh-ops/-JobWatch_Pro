"""
Activity and notification Pydantic schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class UserActivityBase(BaseModel):
    """Base user activity schema"""
    activity_type: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[str] = None


class UserActivityCreate(UserActivityBase):
    """Schema for creating user activity"""
    user_id: str


class UserActivity(UserActivityBase):
    """User activity response schema"""
    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    """Base notification schema"""
    title: str
    message: str
    type: str  # info, warning, success, job_alert, system
    action_url: Optional[str] = None
    expires_at: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    """Schema for creating notification"""
    user_id: str


class NotificationUpdate(BaseModel):
    """Schema for updating notification"""
    is_read: Optional[bool] = None


class Notification(NotificationBase):
    """Notification response schema"""
    id: int
    user_id: str
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationsResponse(BaseModel):
    """Response schema for notifications list"""
    notifications: List[Notification]
    total: int
    unread_count: int
