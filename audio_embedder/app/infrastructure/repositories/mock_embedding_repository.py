import json
import os
from typing import List, Optional
from ...domain.repositories.embedding_repository import EmbeddingRepository
from ...domain.entities.embedding import Embedding


class MockEmbeddingRepository(EmbeddingRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.embeddings = []
        os.makedirs(base_path, exist_ok=True)
    
    def get_by_episode_id(self, episode_id: str) -> List[Embedding]:
        return [emb for emb in self.embeddings if emb.episode_id == episode_id]
    
    def save(self, embedding: Embedding) -> Embedding:
        self.embeddings.append(embedding)
        return embedding
    
    def save_batch(self, embeddings: List[Embedding]) -> List[Embedding]:
        self.embeddings.extend(embeddings)
        return embeddings
    
    def search_similar(self, query_vector: List[float], top_k: int = 10) -> List[Embedding]:
        return self.embeddings[:top_k]