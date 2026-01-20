"""
Record service for managing data records
"""

import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func
from fastapi import HTTPException

from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate, RecordFilters
from app.core.elasticsearch import index_record, search_records
from app.services.activity import create_activity


class RecordService:
    """Record service class"""

    @staticmethod
    async def create_record(db: AsyncSession, record_data: RecordCreate) -> Record:
        """
        Create a new data record
        """
        record_id = str(uuid.uuid4())

        record = Record(
            id=record_id,
            title=record_data.title,
            description=record_data.description,
            source=record_data.source,
            category=record_data.category,
            published_date=record_data.published_date,
            url=record_data.url
        )

        db.add(record)
        await db.commit()
        await db.refresh(record)

        # Index in Elasticsearch for search
        record_dict = {
            "id": record.id,
            "title": record.title,
            "description": record.description,
            "source": record.source,
            "category": record.category,
            "published_date": record.published_date.isoformat(),
            "url": record.url,
            "created_at": record.created_at.isoformat()
        }
        await index_record(record_dict)

        return record

    @staticmethod
    async def get_records(
        db: AsyncSession,
        filters: RecordFilters,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get records with filtering and pagination
        """
        # Use Elasticsearch for search if available
        try:
            search_filters = {}
            if filters.category:
                search_filters["category"] = filters.category

            search_result = await search_records(
                query=filters.search or "",
                filters=search_filters,
                page=filters.page,
                limit=filters.limit
            )

            return search_result

        except Exception as e:
            print(f"Elasticsearch search failed: {e}")
            # Fall back to database search
            return await RecordService._get_records_from_db(db, filters, user_id)

    @staticmethod
    async def _get_records_from_db(
        db: AsyncSession,
        filters: RecordFilters,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get records from database as fallback
        """
        query = select(Record).where(Record.is_active == "active")

        # Apply filters
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.where(
                or_(
                    Record.title.ilike(search_term),
                    Record.description.ilike(search_term),
                    Record.source.ilike(search_term)
                )
            )

        if filters.category:
            query = query.where(Record.category == filters.category)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        query = query.order_by(desc(Record.published_date))
        query = query.limit(filters.limit).offset((filters.page - 1) * filters.limit)

        result = await db.execute(query)
        records = result.scalars().all()

        # Convert to response format
        records_list = []
        for record in records:
            record_dict = {
                "id": record.id,
                "title": record.title,
                "description": record.description,
                "source": record.source,
                "category": record.category,
                "published_date": record.published_date.isoformat(),
                "url": record.url,
                "created_at": record.created_at.isoformat()
            }
            records_list.append(record_dict)

        total_pages = (total + filters.limit - 1) // filters.limit

        return {
            "records": records_list,
            "total": total,
            "page": filters.page,
            "total_pages": total_pages
        }

    @staticmethod
    async def get_record_by_id(db: AsyncSession, record_id: str, user_id: Optional[str] = None) -> Optional[Record]:
        """
        Get record by ID
        """
        result = await db.execute(select(Record).where(Record.id == record_id))
        record = result.scalar_one_or_none()

        if record and user_id:
            # Log view activity
            await create_activity(
                db=db,
                user_id=user_id,
                activity_type="view_record",
                entity_type="record",
                entity_id=record_id,
                description=f"Viewed record: {record.title}"
            )

        return record

    @staticmethod
    async def update_record(
        db: AsyncSession,
        record_id: str,
        record_data: RecordUpdate
    ) -> Record:
        """
        Update a record
        """
        result = await db.execute(select(Record).where(Record.id == record_id))
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        # Update fields
        update_data = record_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)

        await db.commit()
        await db.refresh(record)

        # Re-index in Elasticsearch
        record_dict = {
            "id": record.id,
            "title": record.title,
            "description": record.description,
            "source": record.source,
            "category": record.category,
            "published_date": record.published_date.isoformat(),
            "url": record.url,
            "created_at": record.created_at.isoformat()
        }
        await index_record(record_dict)

        return record

    @staticmethod
    async def delete_record(db: AsyncSession, record_id: str) -> bool:
        """
        Soft delete a record
        """
        result = await db.execute(select(Record).where(Record.id == record_id))
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Record not found")

        record.is_active = "deleted"
        await db.commit()

        return True

    @staticmethod
    async def get_categories(db: AsyncSession) -> List[str]:
        """
        Get unique record categories
        """
        result = await db.execute(
            select(Record.category)
            .where(Record.is_active == "active")
            .distinct()
        )

        return [row[0] for row in result.fetchall()]

    @staticmethod
    async def get_sources(db: AsyncSession) -> List[str]:
        """
        Get unique record sources
        """
        result = await db.execute(
            select(Record.source)
            .where(Record.is_active == "active")
            .distinct()
        )

        return [row[0] for row in result.fetchall()]
