from datetime import datetime
from app.domain.entities.episode import Episode
from app.domain.entities.transcription import Transcription
from app.domain.entities.embedding import Embedding


class EpisodeMother:
    @staticmethod
    def create_episode(
        title: str = "Test Episode",
        description: str = "Test Description",
        url: str = "https://example.com/test.mp3",
        published_date: datetime = None,
        duration: int = 900,
        file_size: int = 1000000,
        local_file_path: str = None,
        podcast: str = None
    ) -> Episode:
        if published_date is None:
            published_date = datetime.now()
        
        return Episode(
            title=title,
            description=description,
            url=url,
            published_date=published_date,
            duration=duration,
            file_size=file_size,
            local_file_path=local_file_path,
            podcast=podcast
        )
    
    @staticmethod
    def create_transcription(
        episode_id: str = "test-episode",
        text: str = "Test transcription text",
        language: str = "en",
        created_at: datetime = None,
        duration: int = 900,
        file_path: str = None,
        confidence_score: float = 0.95
    ) -> Transcription:
        if created_at is None:
            created_at = datetime.now()
        
        return Transcription(
            episode_id=episode_id,
            text=text,
            language=language,
            created_at=created_at,
            duration=duration,
            file_path=file_path,
            confidence_score=confidence_score
        )
    
    @staticmethod
    def create_embedding(
        episode_id: str = "test-episode",
        transcription_id: str = "test-transcription",
        vector: list = None,
        model_name: str = "test-model",
        created_at: datetime = None,
        chunk_index: int = 0,
        chunk_text: str = "Test chunk text",
        metadata: dict = None
    ) -> Embedding:
        if vector is None:
            vector = [0.1] * 384
        if created_at is None:
            created_at = datetime.now()
        
        return Embedding(
            episode_id=episode_id,
            transcription_id=transcription_id,
            vector=vector,
            model_name=model_name,
            created_at=created_at,
            chunk_index=chunk_index,
            chunk_text=chunk_text,
            metadata=metadata
        )