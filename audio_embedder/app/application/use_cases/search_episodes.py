from ...domain.entities.embedding import Embedding
from ...domain.repositories.embedding_repository import EmbeddingRepository
from ..services.embedding_service import EmbeddingService


class SearchEpisodesUseCase:
    def __init__(
        self,
        embedding_repository: EmbeddingRepository,
        embedding_service: EmbeddingService,
    ):
        self.embedding_repository = embedding_repository
        self.embedding_service = embedding_service

    def execute(self, query: str, top_k: int = 10) -> list[Embedding]:
        query_vector = self.embedding_service.create_query_embedding(query)
        return self.embedding_repository.search_similar(query_vector, top_k)
