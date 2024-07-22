from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from application.database import Database

    # Store all objects that should persist throughout server's lifecycle
    app.state.db = Database(db_uri=settings.db_uri)

    yield

    # Clean up and release the resources
    app.state.db.engine.dispose()


def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Set all CORS enabled origins
    if settings.backend_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.backend_cors_origins],
            allow_origin_regex=settings.backend_cors_origin_regex,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    from application.routes.router import main_router
    from application.routes.websocket.chat import router as chat_router

    app.include_router(main_router)
    app.include_router(chat_router)

    return app
