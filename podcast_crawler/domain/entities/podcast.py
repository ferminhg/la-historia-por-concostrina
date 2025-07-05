"""
Entidad Podcast del dominio
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass(frozen=True)
class Episode:
    """Entidad que representa un episodio de podcast"""
    title: str
    description: str
    url: str
    published_date: datetime
    duration: Optional[int] = None
    file_size: Optional[int] = None


@dataclass(frozen=True)
class Podcast:
    """Entidad que representa un podcast"""
    title: str
    description: str
    feed_url: str
    episodes: List[Episode]
    last_updated: datetime 