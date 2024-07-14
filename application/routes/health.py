import logging

from fastapi import status

from application.base_classes import APIRouter
from application.core.serializers.response import ApiResponse

# from application.routes.dependencies.database import get_db_session

logger = logging.getLogger(__name__)

HEALTH_RESOURCE = "health"

router = APIRouter(
    prefix=f"/{HEALTH_RESOURCE}",
    tags=[HEALTH_RESOURCE],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[int],
)
async def health() -> ApiResponse[int]:
    # # Check that the database connection is correctly established
    # session.execute(select(1))

    logger.info('Inside health route')

    return ApiResponse[int](data=200)
