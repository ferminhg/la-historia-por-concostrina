from abc import ABC, abstractmethod
from typing import List
from ...domain.entities.transcription import Transcription
from ...domain.entities.embedding import Embedding


class EmbeddingService(ABC):
    @abstractmethod
    def create_embeddings(self, transcription: Transcription) -> List[Embedding]:
        pass
    
    @abstractmethod
    def create_query_embedding(self, query_text: str) -> List[float]:
        pass