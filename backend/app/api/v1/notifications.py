"""
Notifications API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.activity import Notification, NotificationsResponse
from app.services.activity import ActivityService


router = APIRouter()


@router.get("/", response_model=NotificationsResponse)
async def get_notifications(
    include_read: bool = Query(True, description="Include read notifications"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of notifications"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user notifications
    """
    try:
        notifications = await ActivityService.get_user_notifications(
            db, current_user.id, include_read, limit
        )
        unread_count = await ActivityService.get_unread_count(db, current_user.id)

        return NotificationsResponse(
            notifications=[Notification.from_orm(n) for n in notifications],
            total=len(notifications),
            unread_count=unread_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch notifications: {str(e)}")


@router.put("/{notification_id}/read", response_model=Notification)
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark notification as read
    """
    try:
        notification = await ActivityService.mark_notification_read(
            db, notification_id, current_user.id
        )
        return Notification.from_orm(notification)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark notification as read: {str(e)}")


@router.get("/unread/count", response_model=dict)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get count of unread notifications
    """
    try:
        count = await ActivityService.get_unread_count(db, current_user.id)
        return {"unread_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get unread count: {str(e)}")
