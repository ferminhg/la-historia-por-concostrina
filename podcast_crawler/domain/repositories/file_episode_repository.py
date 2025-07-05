from abc import ABC, abstractmethod

from domain.entities.podcast import Episode


class FileEpisodeRepository(ABC):
    
    @abstractmethod
    def save(self, episode: Episode, audio_data: bytes) -> str:
        pass
    
    @abstractmethod
    def exists(self, episode: Episode) -> bool:
        pass
    
    @abstractmethod
    def get_file_path(self, episode: Episode) -> str:
        pass