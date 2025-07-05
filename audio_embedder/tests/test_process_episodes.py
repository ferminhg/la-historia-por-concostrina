import pytest
from unittest.mock import Mock
from app.application.use_cases.process_episodes import ProcessEpisodesUseCase
from app.domain.entities.episode import Episode
from app.domain.entities.transcription import Transcription
from app.domain.entities.embedding import Embedding
from datetime import datetime


class TestProcessEpisodesUseCase:
    def test_processes_episode_without_existing_transcription(self):
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000,
            local_file_path="/path/to/test.mp3"
        )
        
        transcription = Transcription(
            episode_id=episode.url,
            text="Test transcription",
            language="en",
            created_at=datetime.now(),
            duration=900
        )
        
        embedding = Embedding(
            episode_id=episode.url,
            transcription_id=episode.url,
            vector=[0.1] * 384,
            model_name="test-model",
            created_at=datetime.now(),
            chunk_index=0,
            chunk_text="Test text"
        )
        
        episode_repository = Mock()
        episode_repository.get_all.return_value = [episode]
        
        transcription_repository = Mock()
        transcription_repository.get_by_episode_id.return_value = None
        transcription_repository.save.return_value = transcription
        
        embedding_repository = Mock()
        embedding_repository.save_batch.return_value = [embedding]
        
        audio_transcriptor = Mock()
        audio_transcriptor.transcribe.return_value = transcription
        
        embedding_service = Mock()
        embedding_service.create_embeddings.return_value = [embedding]
        
        use_case = ProcessEpisodesUseCase(
            episode_repository,
            transcription_repository,
            embedding_repository,
            audio_transcriptor,
            embedding_service
        )
        
        use_case.execute()
        
        episode_repository.get_all.assert_called_once()
        transcription_repository.get_by_episode_id.assert_called_once_with(episode.url)
        audio_transcriptor.transcribe.assert_called_once_with(episode)
        transcription_repository.save.assert_called_once_with(transcription)
        embedding_service.create_embeddings.assert_called_once_with(transcription)
        embedding_repository.save_batch.assert_called_once_with([embedding])
    
    def test_skips_episode_with_existing_transcription(self):
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime.now(),
            duration=900,
            file_size=1000000
        )
        
        existing_transcription = Transcription(
            episode_id=episode.url,
            text="Existing transcription",
            language="en",
            created_at=datetime.now(),
            duration=900
        )
        
        episode_repository = Mock()
        episode_repository.get_all.return_value = [episode]
        
        transcription_repository = Mock()
        transcription_repository.get_by_episode_id.return_value = existing_transcription
        
        embedding_repository = Mock()
        audio_transcriptor = Mock()
        embedding_service = Mock()
        
        use_case = ProcessEpisodesUseCase(
            episode_repository,
            transcription_repository,
            embedding_repository,
            audio_transcriptor,
            embedding_service
        )
        
        use_case.execute()
        
        episode_repository.get_all.assert_called_once()
        transcription_repository.get_by_episode_id.assert_called_once_with(episode.url)
        audio_transcriptor.transcribe.assert_not_called()
        transcription_repository.save.assert_not_called()
        embedding_service.create_embeddings.assert_not_called()
        embedding_repository.save_batch.assert_not_called()