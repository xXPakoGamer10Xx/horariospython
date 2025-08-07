from .auth import router as auth_router
from .admin import router as admin_router  
from .schedules import router as schedules_router
from .registration import router as registration_router

__all__ = ["auth_router", "admin_router", "schedules_router", "registration_router"]
