from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class Episode:
    title: str
    description: str
    url: str
    published_date: datetime
    duration: int
    file_size: int
    local_file_path: Optional[str] = None
    podcast: Optional[str] = None