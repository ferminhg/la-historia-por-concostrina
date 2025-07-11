from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class Podcast:
    title: str
    description: str
    feed_url: str
    last_updated: datetime

    def __str__(self):
        return f"Podcast(title={self.title}"


@dataclass(frozen=True)
class Episode:
    title: str
    description: str
    url: str
    published_date: datetime
    duration: Optional[int] = None
    file_size: Optional[int] = None
    podcast: Optional[Podcast] = None
    local_file_path: Optional[str] = None
    id: str = None

    def __post_init__(self):
        if self.id is None:
            formatted_id = self.published_date.strftime("%Y%m%d_%H%M%S")
            object.__setattr__(self, 'id', formatted_id)

    def __str__(self):
        return f"Episode(title={self.title}, description={self.description}, url={self.url}, published_date={self.published_date}, duration={self.duration}, local_file_path={self.local_file_path})"
