import os
import re
from datetime import datetime

from domain.entities.podcast import Episode
from domain.repositories.file_episode_repository import FileEpisodeRepository
from shared.logger import get_logger


class LocalFileEpisodeRepository(FileEpisodeRepository):
    
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        self.logger = get_logger(__name__)
        os.makedirs(storage_dir, exist_ok=True)
    
    def save(self, episode: Episode, audio_data: bytes) -> str:
        file_path = self.get_file_path(episode)
        
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        
        self.logger.info(f"Saved episode to {file_path}")
        return file_path
    
    def exists(self, episode: Episode) -> bool:
        file_path = self.get_file_path(episode)
        return os.path.exists(file_path)
    
    def get_file_path(self, episode: Episode) -> str:
        filename = self._format_filename(episode.published_date) + '.mp3'
        return os.path.join(self.storage_dir, filename)
    
    def _format_filename(self, published_date: datetime) -> str:
        try:
            return published_date.strftime('%Y_%m_%d_%H')
        except Exception as e:
            self.logger.warning(f'Error formatting filename: {published_date} -> {e}')
            return published_date.isoformat().replace(':', '_').replace('-', '_')