from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.episode import Episode


class EpisodeRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Episode]:
        pass
    
    @abstractmethod
    def get_by_id(self, episode_id: str) -> Optional[Episode]:
        pass
    
    @abstractmethod
    def save(self, episode: Episode) -> Episode:
        pass