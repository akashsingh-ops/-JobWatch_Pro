"""
Authentication service
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.core.auth import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB, LoginRequest
from app.services.activity import create_activity


class AuthService:
    """Authentication service class"""

    @staticmethod
    async def register_user(user_data: UserCreate, db: AsyncSession) -> UserInDB:
        """
        Register a new user
        """
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)

        new_user = User(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            preferences=user_data.preferences or {}
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        # Log registration activity
        await create_activity(
            db=db,
            user_id=user_id,
            activity_type="user_registered",
            description=f"User {user_data.name} registered with email {user_data.email}"
        )

        return UserInDB.from_orm(new_user)

    @staticmethod
    async def authenticate_user(login_data: LoginRequest, db: AsyncSession) -> UserInDB:
        """
        Authenticate user with email and password
        """
        # Find user by email
        result = await db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        await db.commit()

        # Log login activity
        await create_activity(
            db=db,
            user_id=user.id,
            activity_type="user_login",
            description=f"User {user.name} logged in"
        )

        return UserInDB.from_orm(user)

    @staticmethod
    async def get_user_by_id(user_id: str, db: AsyncSession) -> UserInDB:
        """
        Get user by ID
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserInDB.from_orm(user)

    @staticmethod
    async def update_user_preferences(
        user_id: str,
        preferences: dict,
        db: AsyncSession
    ) -> UserInDB:
        """
        Update user preferences
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.preferences = preferences
        await db.commit()
        await db.refresh(user)

        return UserInDB.from_orm(user)
