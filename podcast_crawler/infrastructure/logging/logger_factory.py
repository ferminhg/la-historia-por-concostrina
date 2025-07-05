from .logger import Logger
from .python_logger import PythonLogger


class LoggerFactory:
    @staticmethod
    def create(name: str) -> Logger:
        return PythonLogger(name)

    @staticmethod
    def get_logger(name: str) -> Logger:
        return LoggerFactory.create(name)
