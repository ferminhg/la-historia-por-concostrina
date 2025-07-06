from abc import ABC, abstractmethod
from typing import Optional

from ..entities.episode import Episode


class EpisodeRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Episode]:
        pass

    @abstractmethod
    def get_by_id(self, episode_id: str) -> Optional[Episode]:
        pass

    @abstractmethod
    def save(self, episode: Episode) -> Episode:
        pass
