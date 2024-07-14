from collections.abc import Callable, Mapping
from contextlib import AbstractAsyncContextManager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.config import settings

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
#     from application.core.common.adapters.mapping_parser import MappingParser
#     from application.core.employees.extractors.form_extractor import FormEmployeeExtractor
#     from application.core.matching.resource_projector import ResourceProjector
#     from application.core.matching.searcher import Searcher
#     from application.core.offers.extractor import OfferExtractor
#     from application.core.orb.service import OrbService
#     from application.core.trainings.extractor import TrainingExtractor
#     from application.database import Database
#
#     # Store all objects that should persist throughout server's lifecycle
#     app.state.db = Database(db_uri=settings.db_uri, enable_tracing=settings.enable_tracing)
#     app.state.orb_service = OrbService(db_uri=settings.orb_db_uri, enable_tracing=settings.enable_tracing)
#
#     # Load data science classes
#     app.state.searcher = Searcher(orb=app.state.orb_service)
#     app.state.resource_projector = ResourceProjector(orb=app.state.orb_service)
#     app.state.mapping_parser = MappingParser(orb=app.state.orb_service)
#
#     # Load and save extractors
#     app.state.form_employee_extractor = FormEmployeeExtractor(mapping_parser=app.state.mapping_parser)
#     app.state.offer_extractor = OfferExtractor(mapping_parser=app.state.mapping_parser)
#     app.state.training_extractor = TrainingExtractor(mapping_parser=app.state.mapping_parser)
#
#     # Run server
#     yield
#
#     # Clean up and release the resources
#     app.state.db.engine.dispose()


def init_app(
        custom_lifespan: (
                Callable[[FastAPI], AbstractAsyncContextManager[None]]
                | Callable[[FastAPI], AbstractAsyncContextManager[Mapping[str, Any]]] | None
        ) = None,
) -> FastAPI:
    # Allow the passage of a custom lifespan method that will be used to
    # initialize all the server's shared resources
    # Note: now it's possible to customize the tests by either using FastAPI
    # dependency injection feature and updating the get_() methods, or by
    # changing the "global" shared resource using the custom_lifespan. This is
    # temporary and will be removed once we refactor the whole project
    # architecture and tests

    # Store db object on each request in order to use it on middlewares
    app = FastAPI(lifespan=custom_lifespan)
    # if custom_lifespan:
    #     app = FastAPI(lifespan=custom_lifespan)
    # else:
    #     app = FastAPI(lifespan=lifespan)

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

    app.include_router(main_router)

    return app
