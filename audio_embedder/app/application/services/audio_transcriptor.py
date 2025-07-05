from abc import ABC, abstractmethod
from typing import Optional
from ...domain.entities.episode import Episode
from ...domain.entities.transcription import Transcription


class AudioTranscriptor(ABC):
    @abstractmethod
    def transcribe(self, episode: Episode) -> Optional[Transcription]:
        pass