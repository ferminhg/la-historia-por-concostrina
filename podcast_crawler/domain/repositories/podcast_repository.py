"""
Interfaz del repositorio de podcasts
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.podcast import Podcast


class PodcastRepository(ABC):
    """Interfaz para el repositorio de podcasts"""
    
    @abstractmethod
    def save(self, podcast: Podcast) -> None:
        """Guarda un podcast"""
        pass
    
    @abstractmethod
    def get_by_feed_url(self, feed_url: str) -> Optional[Podcast]:
        """Obtiene un podcast por su URL de feed"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Podcast]:
        """Obtiene todos los podcasts"""
        pass 