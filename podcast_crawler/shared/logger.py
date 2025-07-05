from infrastructure.logging.logger_factory import LoggerFactory


def get_logger(name: str):
    return LoggerFactory.get_logger(name)