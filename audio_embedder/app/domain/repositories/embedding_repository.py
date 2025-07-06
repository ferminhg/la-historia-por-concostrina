from abc import ABC, abstractmethod

from ..entities.embedding import Embedding


class EmbeddingRepository(ABC):
    @abstractmethod
    def get_by_episode_id(self, episode_id: str) -> list[Embedding]:
        pass

    @abstractmethod
    def save(self, embedding: Embedding) -> Embedding:
        pass

    @abstractmethod
    def save_batch(self, embeddings: list[Embedding]) -> list[Embedding]:
        pass

    @abstractmethod
    def search_similar(
        self, query_vector: list[float], top_k: int = 10
    ) -> list[Embedding]:
        pass
