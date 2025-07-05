from abc import ABC, abstractmethod
from typing import List

from domain.entities.podcast import Episode


class EpisodeRepository(ABC):
    @abstractmethod
    def save(self, episodes: List[Episode]) -> None:
        pass

    @abstractmethod
    def find_all(self) -> List[Episode]:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> Episode:
        pass
