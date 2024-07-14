from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable


class CallableInstance(object):
    def __call__(self) -> CallableInstance:
        return self


class APIRouter(FastAPIRouter):
    """Custom FastAPI 'APIRouter' class used to allow routes to be accessed
    with or without a trailing slash ("/api/route/" for example) without
    causing the server to redirect the request.

    The motivation behind this is that when making a request with a
    trailing slash, FasAPI would redirect the route to the one without
    trailing slash, but would also replace https by http, causing a
    "Mixed Content" error on some frontend calls to the backend.
    """
    def api_route(self,
                  path: str,
                  *,
                  include_in_schema: bool = True,
                  **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        add_path = super().api_route(path, include_in_schema=include_in_schema, **kwargs)

        alternate_path = path + "/"
        add_alternate_path = super().api_route(alternate_path, include_in_schema=False, **kwargs)

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator
