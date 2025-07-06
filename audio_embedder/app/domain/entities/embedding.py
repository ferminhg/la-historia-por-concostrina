from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Embedding:
    episode_id: str
    transcription_id: str
    vector: list[float]
    model_name: str
    created_at: datetime
    chunk_index: int
    chunk_text: str
    metadata: Optional[dict] = None
