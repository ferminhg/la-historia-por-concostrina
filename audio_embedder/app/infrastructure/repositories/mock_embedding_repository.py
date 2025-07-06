import os

from ...domain.entities.embedding import Embedding
from ...domain.repositories.embedding_repository import EmbeddingRepository


class MockEmbeddingRepository(EmbeddingRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.embeddings = []
        os.makedirs(base_path, exist_ok=True)

    def get_by_episode_id(self, episode_id: str) -> list[Embedding]:
        return [emb for emb in self.embeddings if emb.episode_id == episode_id]

    def save(self, embedding: Embedding) -> Embedding:
        self.embeddings.append(embedding)
        return embedding

    def save_batch(self, embeddings: list[Embedding]) -> list[Embedding]:
        self.embeddings.extend(embeddings)
        return embeddings

    def search_similar(
        self, query_vector: list[float], top_k: int = 10
    ) -> list[Embedding]:
        return self.embeddings[:top_k]
