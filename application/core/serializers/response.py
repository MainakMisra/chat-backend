from typing import Generic, TypeVar

from pydantic.generics import GenericModel

DataType = TypeVar("DataType")


class ApiResponse(GenericModel, Generic[DataType]):
    data: DataType | None

