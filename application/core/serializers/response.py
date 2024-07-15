from typing import Generic, TypeVar

from pydantic import BaseModel

DataType = TypeVar("DataType")


class ApiResponse(BaseModel, Generic[DataType]):
    data: DataType | None

