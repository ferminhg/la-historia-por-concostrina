from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC):
    
    @abstractmethod
    def debug(self, message: str, *args: Any) -> None:
        pass
    
    @abstractmethod
    def info(self, message: str, *args: Any) -> None:
        pass
    
    @abstractmethod
    def warning(self, message: str, *args: Any) -> None:
        pass
    
    @abstractmethod
    def error(self, message: str, *args: Any) -> None:
        pass
    
    @abstractmethod
    def critical(self, message: str, *args: Any) -> None:
        pass