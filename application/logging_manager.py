import logging
import sys

from loguru import logger


def setup_logging(
        logging_level: str,
        logging_json_format: bool,
        sqlalchemy_log_level: str,
) -> None:
    """Method used for configuring and handling the server's logging system."""
    logging.root.setLevel(logging_level)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Suppress excessive log from some libraries
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_log_level)

    logger_handler = {"sink": sys.stdout, "serialize": logging_json_format, "diagnose": True, "backtrace": False,
                      "format": (
                          "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
                          "| <level>{level}</level> "
                          "| [<cyan>{name}</cyan>"
                          ":<cyan>{function}</cyan>"
                          ":<cyan>{line}</cyan>] "
                          "| <level>{message}</level> "
                      )}

    logger.configure(handlers=[logger_handler])
