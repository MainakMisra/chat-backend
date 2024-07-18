import logging

from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from application.base_classes import APIRouter
from application.core.serializers.response import ApiResponse
from application.routes.dependencies.db import get_db_session

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
async def health(session: Session = Depends(get_db_session),) -> ApiResponse[int]:

    session.execute(select(1))

    return ApiResponse[int](data=200)
