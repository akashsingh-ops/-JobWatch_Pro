"""
Main API router
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.records import router as records_router
from app.api.v1.users import router as users_router
from app.api.v1.notifications import router as notifications_router


api_router = APIRouter()

# Include all API routers
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
api_router.include_router(records_router, prefix="/records", tags=["records"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
