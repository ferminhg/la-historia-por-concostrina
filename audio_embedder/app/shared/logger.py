from ..infrastructure.logging.logger import Logger


def get_logger(name: str) -> Logger:
    return Logger(name)
