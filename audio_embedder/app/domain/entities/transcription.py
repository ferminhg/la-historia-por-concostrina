from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class Transcription:
    episode_id: str
    text: str
    language: str
    created_at: datetime
    duration: int
    file_path: Optional[str] = None
    confidence_score: Optional[float] = None