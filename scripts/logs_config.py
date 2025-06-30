import logging
from logging import FileHandler, Logger
from typing import Any


def configureLogs() -> None:
    logger: Logger = logging.getLogger("botLogs")
    logger.setLevel(logging.DEBUG)

    logger.handlers.clear()

    fileHandler: FileHandler = logging.FileHandler("logs.log")
    consoleHandler: Any = logging.StreamHandler()

    fileHandler.setLevel(logging.INFO)
    consoleHandler.setLevel(logging.DEBUG)

    fileFormat: Any = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    consoleFormat: Any = logging.Formatter("%(levelname)s - %(message)s")

    fileHandler.setFormatter(fileFormat)
    consoleHandler.setFormatter(consoleFormat)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
