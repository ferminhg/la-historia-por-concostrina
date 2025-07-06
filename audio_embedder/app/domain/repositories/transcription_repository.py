from abc import ABC, abstractmethod
from typing import Optional

from ..entities.transcription import Transcription


class TranscriptionRepository(ABC):
    @abstractmethod
    def get_by_episode_id(self, episode_id: str) -> Optional[Transcription]:
        pass

    @abstractmethod
    def save(self, transcription: Transcription) -> Transcription:
        pass

    @abstractmethod
    def get_all(self) -> list[Transcription]:
        pass
