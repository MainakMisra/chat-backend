from application.base_classes import APIRouter
from application.routes.health import router as health_router

main_router = APIRouter()

main_router.include_router(health_router)