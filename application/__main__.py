import uvicorn

from application.app import init_app
from application.config import settings

if __name__ == "__main__":
    app = init_app()

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=settings.server_port,
        log_level=settings.logging_level.lower(),
        reload=settings.uvicorn_auto_reload,
    )

    server = uvicorn.Server(config)
    server.run()
