"""
Implementación de repositorio de podcasts usando archivos
"""
import json
import os
from typing import List, Optional
from datetime import datetime
from ...domain.entities.podcast import Podcast
from ...domain.repositories.podcast_repository import PodcastRepository


class FilePodcastRepository(PodcastRepository):
    """Implementación de repositorio usando archivos JSON"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save(self, podcast: Podcast) -> None:
        """Guarda un podcast en archivo JSON"""
        filename = f"{self._sanitize_filename(podcast.title)}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        podcast_data = {
            "title": podcast.title,
            "description": podcast.description,
            "feed_url": podcast.feed_url,
            "last_updated": podcast.last_updated.isoformat(),
            "episodes": [
                {
                    "title": episode.title,
                    "description": episode.description,
                    "url": episode.url,
                    "published_date": episode.published_date.isoformat(),
                    "duration": episode.duration,
                    "file_size": episode.file_size
                }
                for episode in podcast.episodes
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(podcast_data, f, indent=2, ensure_ascii=False)
    
    def get_by_feed_url(self, feed_url: str) -> Optional[Podcast]:
        """Obtiene un podcast por su URL de feed"""
        # TODO: Implementar búsqueda por feed_url
        return None
    
    def get_all(self) -> List[Podcast]:
        """Obtiene todos los podcasts"""
        podcasts = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # TODO: Convertir data a objeto Podcast
                        pass
                except Exception as e:
                    print(f"Error leyendo {filepath}: {e}")
        return podcasts
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitiza un nombre de archivo"""
        import re
        return re.sub(r'[^\w\-_\.]', '_', filename) 