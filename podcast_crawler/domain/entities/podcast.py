from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class Episode:
    title: str
    description: str
    url: str
    published_date: datetime
    duration: Optional[int] = None
    file_size: Optional[int] = None


@dataclass(frozen=True)
class Podcast:
    title: str
    description: str
    feed_url: str
    episodes: List[Episode]
    last_updated: datetime

    def __str__(self):
        return f"Pmodcast(title={self.title}, description={self.description}, feed_url={self.feed_url}, episodes={self.episodes}, last_updated={self.last_updated})"
