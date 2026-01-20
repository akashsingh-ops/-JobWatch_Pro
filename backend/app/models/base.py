"""
Base database models and mixins
"""

from datetime import datetime
from typing import Any, Dict
from sqlalchemy import Column, DateTime, Integer, String, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """
    Base class for all database models
    """

    # Disable MappedAsDataclass to allow for custom __init__ methods
    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower() + "s"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs) -> None:
        """Update model attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Base":
        """Create model instance from dictionary"""
        return cls(**data)


class TimestampMixin:
    """Mixin for timestamp fields"""
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    deleted_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(default=False, nullable=False)

    def soft_delete(self) -> None:
        """Mark record as deleted"""
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True

    def restore(self) -> None:
        """Restore soft deleted record"""
        self.deleted_at = None
        self.is_deleted = False

    @classmethod
    def not_deleted(cls):
        """Query filter for non-deleted records"""
        return cls.is_deleted == False


# Event listeners for automatic timestamp updates
@event.listens_for(Base, 'before_update')
def receive_before_update(mapper, connection, target):
    """Automatically update updated_at timestamp"""
    target.updated_at = datetime.utcnow()
