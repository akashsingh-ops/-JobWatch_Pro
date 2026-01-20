"""
Activity and notification service
"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from fastapi import HTTPException

from app.models.activity import UserActivity, Notification
from app.schemas.activity import UserActivityCreate, NotificationCreate, NotificationUpdate


class ActivityService:
    """Activity and notification service"""

    @staticmethod
    async def create_activity(
        db: AsyncSession,
        user_id: str,
        activity_type: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[str] = None
    ) -> UserActivity:
        """
        Create a user activity record
        """
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            metadata=metadata
        )

        db.add(activity)
        await db.commit()
        await db.refresh(activity)

        return activity

    @staticmethod
    async def get_user_activities(
        db: AsyncSession,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[UserActivity]:
        """
        Get user activities
        """
        result = await db.execute(
            select(UserActivity)
            .where(UserActivity.user_id == user_id)
            .order_by(desc(UserActivity.created_at))
            .limit(limit)
            .offset(offset)
        )

        return result.scalars().all()

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        notification_data: NotificationCreate
    ) -> Notification:
        """
        Create a notification
        """
        notification = Notification(**notification_data.dict())
        db.add(notification)
        await db.commit()
        await db.refresh(notification)

        return notification

    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id: str,
        include_read: bool = True,
        limit: int = 50
    ) -> List[Notification]:
        """
        Get user notifications
        """
        query = select(Notification).where(Notification.user_id == user_id)

        if not include_read:
            query = query.where(Notification.is_read == False)

        # Filter out expired notifications
        now = datetime.utcnow()
        query = query.where(
            and_(
                Notification.expires_at.is_(None),
                Notification.expires_at > now
            )
        )

        result = await db.execute(
            query.order_by(desc(Notification.created_at)).limit(limit)
        )

        return result.scalars().all()

    @staticmethod
    async def mark_notification_read(
        db: AsyncSession,
        notification_id: int,
        user_id: str
    ) -> Notification:
        """
        Mark notification as read
        """
        result = await db.execute(
            select(Notification).where(
                and_(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
            )
        )

        notification = result.scalar_one_or_none()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        notification.is_read = True
        notification.read_at = datetime.utcnow()

        await db.commit()
        await db.refresh(notification)

        return notification

    @staticmethod
    async def get_unread_count(db: AsyncSession, user_id: str) -> int:
        """
        Get count of unread notifications
        """
        now = datetime.utcnow()
        result = await db.execute(
            select(Notification).where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False,
                    and_(
                        Notification.expires_at.is_(None),
                        Notification.expires_at > now
                    )
                )
            )
        )

        notifications = result.scalars().all()
        return len(notifications)

    @staticmethod
    async def cleanup_expired_notifications(db: AsyncSession) -> int:
        """
        Clean up expired notifications
        """
        now = datetime.utcnow()
        result = await db.execute(
            select(Notification).where(
                and_(
                    Notification.expires_at.isnot(None),
                    Notification.expires_at <= now
                )
            )
        )

        expired_notifications = result.scalars().all()
        count = len(expired_notifications)

        for notification in expired_notifications:
            await db.delete(notification)

        await db.commit()
        return count
