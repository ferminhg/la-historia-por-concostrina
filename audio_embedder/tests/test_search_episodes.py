from datetime import datetime
from unittest.mock import Mock

from app.application.use_cases.search_episodes import SearchEpisodesUseCase
from app.domain.entities.embedding import Embedding


class TestSearchEpisodesUseCase:
    def test_searches_episodes_with_query(self):
        query = "test query"
        query_vector = [0.1] * 384

        embedding = Embedding(
            episode_id="test-episode",
            transcription_id="test-transcription",
            vector=[0.2] * 384,
            model_name="test-model",
            created_at=datetime.now(),
            chunk_index=0,
            chunk_text="Test chunk text",
        )

        embedding_repository = Mock()
        embedding_repository.search_similar.return_value = [embedding]

        embedding_service = Mock()
        embedding_service.create_query_embedding.return_value = query_vector

        use_case = SearchEpisodesUseCase(embedding_repository, embedding_service)
        results = use_case.execute(query, top_k=5)

        embedding_service.create_query_embedding.assert_called_once_with(query)
        embedding_repository.search_similar.assert_called_once_with(query_vector, 5)
        assert len(results) == 1
        assert results[0] == embedding
