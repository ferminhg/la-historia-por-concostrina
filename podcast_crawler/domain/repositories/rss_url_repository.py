from abc import ABC, abstractmethod
from typing import List

from domain.entities.podcast import Episode


class RSSUrlRepository(ABC):
    @abstractmethod
    def search(self) -> List[Episode]:
        pass
