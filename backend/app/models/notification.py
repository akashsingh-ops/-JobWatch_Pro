"""
Notification system models
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base


class Notification(Base):
    """
    User notification model
    """

    __tablename__ = "notifications"

    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Notification content
    title: str = Column(String(255), nullable=False)
    message: str = Column(Text, nullable=False)
    notification_type: str = Column(String(50), nullable=False, index=True)  # job_alert, application_update, system, marketing

    # Status and delivery
    is_read: bool = Column(Boolean, default=False, index=True)
    read_at: Optional[datetime] = Column(DateTime)

    # Delivery channels
    email_sent: bool = Column(Boolean, default=False)
    push_sent: bool = Column(Boolean, default=False)
    sms_sent: bool = Column(Boolean, default=False)

    # Action and metadata
    action_url: Optional[str] = Column(String(500))  # URL to redirect when clicked
    action_text: Optional[str] = Column(String(100))  # Text for action button
    metadata: Dict[str, Any] = Column(Text, default="{}")  # Additional data as JSON

    # Scheduling
    scheduled_at: Optional[datetime] = Column(DateTime)
    expires_at: Optional[datetime] = Column(DateTime)

    # Priority and categorization
    priority: str = Column(String(20), default="normal")  # low, normal, high, urgent
    category: str = Column(String(100), default="general")  # jobs, applications, system, etc.

    # Relationships
    user = relationship("User", back_populates="notifications")

    # Indexes
    __table_args__ = (
        Index('idx_notification_user_read', 'user_id', 'is_read'),
        Index('idx_notification_type', 'notification_type'),
        Index('idx_notification_created', 'created_at'),
        Index('idx_notification_expires', 'expires_at'),
    )

    @property
    def is_expired(self) -> bool:
        """Check if notification has expired"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False

    @property
    def time_since_created(self) -> str:
        """Get human-readable time since notification was created"""
        now = datetime.utcnow()
        diff = now - self.created_at

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"

    def mark_as_read(self) -> None:
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()

    def should_send_email(self) -> bool:
        """Check if email should be sent for this notification"""
        return not self.email_sent and self.user.email_notifications

    def should_send_push(self) -> bool:
        """Check if push notification should be sent"""
        return not self.push_sent and self.user.push_notifications

    def should_send_sms(self) -> bool:
        """Check if SMS should be sent"""
        return not self.sms_sent and self.user.sms_notifications


class NotificationTemplate(Base):
    """
    Notification template model for reusable templates
    """

    __tablename__ = "notification_templates"

    name: str = Column(String(100), unique=True, nullable=False, index=True)
    subject_template: str = Column(Text, nullable=False)  # For email subjects
    message_template: str = Column(Text, nullable=False)  # For notification messages
    email_template: Optional[str] = Column(Text)  # HTML template for emails

    # Template variables (JSON)
    required_variables: Dict[str, str] = Column(Text, default="{}")  # {"job_title": "string", "company": "string"}

    # Usage tracking
    usage_count: int = Column(Integer, default=0)
    last_used: Optional[datetime] = Column(DateTime)

    # Metadata
    description: Optional[str] = Column(Text)
    created_by: Optional[int] = Column(Integer, ForeignKey("users.id"))

    def increment_usage(self) -> None:
        """Increment usage count"""
        self.usage_count += 1
        self.last_used = datetime.utcnow()

    def render_subject(self, variables: Dict[str, Any]) -> str:
        """Render subject template with variables"""
        return self.subject_template.format(**variables)

    def render_message(self, variables: Dict[str, Any]) -> str:
        """Render message template with variables"""
        return self.message_template.format(**variables)

    def render_email(self, variables: Dict[str, Any]) -> Optional[str]:
        """Render email template with variables"""
        if self.email_template:
            return self.email_template.format(**variables)
        return None


class EmailLog(Base):
    """
    Email delivery tracking
    """

    __tablename__ = "email_logs"

    recipient_email: str = Column(String(255), nullable=False, index=True)
    recipient_user_id: Optional[int] = Column(Integer, ForeignKey("users.id"), index=True)

    # Email content
    subject: str = Column(String(500), nullable=False)
    body: Text = Column(Text, nullable=False)
    content_type: str = Column(String(50), default="html")  # html, text

    # Delivery status
    status: str = Column(String(50), default="pending", index=True)  # pending, sent, delivered, bounced, failed
    sent_at: Optional[datetime] = Column(DateTime)
    delivered_at: Optional[datetime] = Column(DateTime)
    bounced_at: Optional[datetime] = Column(DateTime)

    # Error tracking
    error_message: Optional[str] = Column(Text)
    retry_count: int = Column(Integer, default=0)

    # Metadata
    template_used: Optional[str] = Column(String(100))
    notification_id: Optional[int] = Column(Integer, ForeignKey("notifications.id"))

    # Provider information
    smtp_provider: str = Column(String(50), default="default")
    message_id: Optional[str] = Column(String(255))  # SMTP message ID

    # Indexes
    __table_args__ = (
        Index('idx_email_status_sent', 'status', 'sent_at'),
        Index('idx_email_recipient', 'recipient_email', 'status'),
    )

    @property
    def delivery_time(self) -> Optional[float]:
        """Get delivery time in seconds"""
        if self.sent_at and self.delivered_at:
            return (self.delivered_at - self.sent_at).total_seconds()
        return None

    def mark_sent(self) -> None:
        """Mark email as sent"""
        self.status = "sent"
        self.sent_at = datetime.utcnow()

    def mark_delivered(self) -> None:
        """Mark email as delivered"""
        self.status = "delivered"
        self.delivered_at = datetime.utcnow()

    def mark_bounced(self, error_message: str = None) -> None:
        """Mark email as bounced"""
        self.status = "bounced"
        self.bounced_at = datetime.utcnow()
        if error_message:
            self.error_message = error_message

    def mark_failed(self, error_message: str = None) -> None:
        """Mark email as failed"""
        self.status = "failed"
        if error_message:
            self.error_message = error_message
        self.retry_count += 1
