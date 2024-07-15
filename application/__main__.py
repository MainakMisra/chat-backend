import uvicorn

from application.app import init_app
from application.config import settings

# from application.logging_manager import setup_logging

if __name__ == "__main__":
    app = init_app()

    config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=settings.server_port,
            log_level=settings.logging_level.lower(),
            reload=settings.uvicorn_auto_reload

    )

    # setup_logging(
    #     logging_level=settings.logging_level,
    #     logging_json_format=settings.logging_json_format,
    #     sqlalchemy_log_level=settings.sqlalchemy_log_level,
    # )

    server = uvicorn.Server(config)
    server.run()
