from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.embedding import Embedding


class EmbeddingRepository(ABC):
    @abstractmethod
    def get_by_episode_id(self, episode_id: str) -> List[Embedding]:
        pass
    
    @abstractmethod
    def save(self, embedding: Embedding) -> Embedding:
        pass
    
    @abstractmethod
    def save_batch(self, embeddings: List[Embedding]) -> List[Embedding]:
        pass
    
    @abstractmethod
    def search_similar(self, query_vector: List[float], top_k: int = 10) -> List[Embedding]:
        pass