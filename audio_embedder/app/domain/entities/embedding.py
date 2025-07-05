from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass(frozen=True)
class Embedding:
    episode_id: str
    transcription_id: str
    vector: List[float]
    model_name: str
    created_at: datetime
    chunk_index: int
    chunk_text: str
    metadata: Optional[dict] = None