from datetime import datetime

from ...application.services.embedding_service import EmbeddingService
from ...domain.entities.embedding import Embedding
from ...domain.entities.transcription import Transcription


class MockEmbeddingService(EmbeddingService):
    def create_embeddings(self, transcription: Transcription) -> list[Embedding]:
        chunks = self._chunk_text(transcription.text)
        embeddings = []

        for i, chunk in enumerate(chunks):
            embedding = Embedding(
                episode_id=transcription.episode_id,
                transcription_id=transcription.episode_id,
                vector=[0.1] * 384,
                model_name="mock-model",
                created_at=datetime.now(),
                chunk_index=i,
                chunk_text=chunk,
                metadata={"mock": True},
            )
            embeddings.append(embedding)

        return embeddings

    def create_query_embedding(self, query_text: str) -> list[float]:
        return [0.1] * 384

    def _chunk_text(self, text: str, chunk_size: int = 1000) -> list[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
