"""
Record Pydantic schemas
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class RecordBase(BaseModel):
    """Base record schema"""
    title: str
    description: str
    source: str
    category: str
    published_date: datetime
    url: Optional[str] = None


class RecordCreate(RecordBase):
    """Schema for record creation"""
    pass


class RecordUpdate(BaseModel):
    """Schema for record updates"""
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    published_date: Optional[datetime] = None
    url: Optional[str] = None


class RecordInDBBase(RecordBase):
    """Base schema for record in database"""
    id: str
    is_active: str = "active"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Record(RecordInDBBase):
    """Record schema for responses"""
    pass


class RecordInDB(RecordInDBBase):
    """Record schema for database operations"""
    pass


class RecordsResponse(BaseModel):
    """Response schema for records list"""
    records: List[Record]
    total: int
    page: int
    total_pages: int


class RecordFilters(BaseModel):
    """Record filtering schema"""
    search: Optional[str] = None
    category: Optional[str] = None
    page: int = 1
    limit: int = 12
