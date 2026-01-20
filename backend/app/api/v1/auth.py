"""
Authentication API endpoints
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.core.database import get_db
from app.schemas.user import User, Token, LoginRequest, RegisterRequest
from app.services.auth import AuthService


router = APIRouter()


@router.post("/register", response_model=User)
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    try:
        user = await AuthService.register_user(user_data, db)
        return User.from_orm(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    """
    try:
        user = await AuthService.authenticate_user(login_data, db)
        access_token = create_access_token(data={"sub": user.id})
        return Token(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/login/form", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible login endpoint
    """
    login_request = LoginRequest(email=form_data.username, password=form_data.password)
    return await login(login_request, db)


@router.get("/me", response_model=User)
async def get_current_user(
    current_user: User = Depends(AuthService.get_user_by_id)
):
    """
    Get current authenticated user information
    """
    return current_user
