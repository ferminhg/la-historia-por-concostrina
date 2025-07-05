import logging
from typing import Any

from .logger import Logger


class PythonLogger(Logger):
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            self._configure_logger()
    
    def _configure_logger(self) -> None:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
    
    def debug(self, message: str, *args: Any) -> None:
        self._logger.debug(message, *args)
    
    def info(self, message: str, *args: Any) -> None:
        self._logger.info(message, *args)
    
    def warning(self, message: str, *args: Any) -> None:
        self._logger.warning(message, *args)
    
    def error(self, message: str, *args: Any) -> None:
        self._logger.error(message, *args)
    
    def critical(self, message: str, *args: Any) -> None:
        self._logger.critical(message, *args)