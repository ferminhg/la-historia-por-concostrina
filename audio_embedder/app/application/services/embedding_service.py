from abc import ABC, abstractmethod

from ...domain.entities.embedding import Embedding
from ...domain.entities.transcription import Transcription


class EmbeddingService(ABC):
    @abstractmethod
    def create_embeddings(self, transcription: Transcription) -> list[Embedding]:
        pass

    @abstractmethod
    def create_query_embedding(self, query_text: str) -> list[float]:
        pass
