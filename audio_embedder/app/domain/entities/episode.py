from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Episode:
    id: str
    title: str
    description: str
    url: str
    published_date: datetime
    duration: int
    file_size: int
    local_file_path: Optional[str] = None
    podcast: Optional[str] = None
