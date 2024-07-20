from application.base_classes import APIRouter
from application.config import settings
from application.routes.api.auth import router as auth_router
from application.routes.api.health import router as health_router
from application.routes.api.users import router as user_router

main_router = APIRouter(prefix=settings.api_prefix)

main_router.include_router(health_router)
main_router.include_router(auth_router)
main_router.include_router(user_router)
