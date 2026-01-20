"""
Records API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.record import Record, RecordsResponse, RecordFilters
from app.services.record import RecordService


router = APIRouter()


@router.get("/", response_model=RecordsResponse)
async def get_records(
    search: str = Query(None, description="Search query"),
    category: str = Query(None, description="Record category"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(12, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get records with filtering and pagination
    """
    try:
        filters = RecordFilters(
            search=search,
            category=category,
            page=page,
            limit=limit
        )

        result = await RecordService.get_records(db, filters, current_user.id)
        return RecordsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch records: {str(e)}")


@router.get("/{record_id}", response_model=Record)
async def get_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get record by ID
    """
    try:
        record = await RecordService.get_record_by_id(db, record_id, current_user.id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        return Record.from_orm(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch record: {str(e)}")


@router.get("/meta/categories", response_model=List[str])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    Get available record categories
    """
    try:
        return await RecordService.get_categories(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")


@router.get("/meta/sources", response_model=List[str])
async def get_sources(
    db: AsyncSession = Depends(get_db)
):
    """
    Get available record sources
    """
    try:
        return await RecordService.get_sources(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sources: {str(e)}")
