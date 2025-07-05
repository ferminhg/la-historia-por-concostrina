from datetime import datetime
from typing import Optional

from domain.entities.podcast import Episode, Podcast


class EpisodeBuilder:
    
    def __init__(self, episode: Episode):
        self._title = episode.title
        self._description = episode.description
        self._url = episode.url
        self._published_date = episode.published_date
        self._duration = episode.duration
        self._file_size = episode.file_size
        self._podcast = episode.podcast
        self._local_file_path = episode.local_file_path
    
    def with_title(self, title: str) -> "EpisodeBuilder":
        self._title = title
        return self
    
    def with_description(self, description: str) -> "EpisodeBuilder":
        self._description = description
        return self
    
    def with_url(self, url: str) -> "EpisodeBuilder":
        self._url = url
        return self
    
    def with_published_date(self, published_date: datetime) -> "EpisodeBuilder":
        self._published_date = published_date
        return self
    
    def with_duration(self, duration: Optional[int]) -> "EpisodeBuilder":
        self._duration = duration
        return self
    
    def with_file_size(self, file_size: Optional[int]) -> "EpisodeBuilder":
        self._file_size = file_size
        return self
    
    def with_podcast(self, podcast: Optional[Podcast]) -> "EpisodeBuilder":
        self._podcast = podcast
        return self
    
    def with_local_file_path(self, local_file_path: Optional[str]) -> "EpisodeBuilder":
        self._local_file_path = local_file_path
        return self
    
    def build(self) -> Episode:
        return Episode(
            title=self._title,
            description=self._description,
            url=self._url,
            published_date=self._published_date,
            duration=self._duration,
            file_size=self._file_size,
            podcast=self._podcast,
            local_file_path=self._local_file_path
        )