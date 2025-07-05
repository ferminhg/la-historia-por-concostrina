"""
Caso de uso para hacer crawling de un podcast
"""
from typing import Optional
from ...domain.entities.podcast import Podcast
from ...domain.repositories.podcast_repository import PodcastRepository


class CrawlPodcastUseCase:
    """Caso de uso para hacer crawling de un podcast"""
    
    def __init__(self, repository: PodcastRepository):
        self.repository = repository
    
    def execute(self, feed_url: str) -> Optional[Podcast]:
        """
        Ejecuta el crawling de un podcast
        
        Args:
            feed_url: URL del feed RSS del podcast
            
        Returns:
            Podcast crawleado o None si hay error
        """
        # TODO: Implementar lógica de crawling
        print(f"Crawling podcast desde: {feed_url}")
        return None 