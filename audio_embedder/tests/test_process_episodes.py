from datetime import datetime
from unittest.mock import Mock

from app.application.use_cases.process_episodes import ProcessEpisodesUseCase
from app.domain.entities.embedding import Embedding
from app.domain.entities.episode import Episode
from app.domain.entities.transcription import Transcription
from tests.helpers.episode_mother import EpisodeMother


class TestProcessEpisodesUseCase:
    def test_processes_episode_without_existing_transcription(self):
        episode = EpisodeMother.create_episode(
            id="20250706_test1",
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            local_file_path="/path/to/test.mp3",
        )

        transcription = Transcription(
            episode_id=episode.id,
            text="Test transcription",
            language="en",
            created_at=datetime.now(),
            duration=900,
        )

        embedding = Embedding(
            episode_id=episode.id,
            transcription_id=episode.id,
            vector=[0.1] * 384,
            model_name="test-model",
            created_at=datetime.now(),
            chunk_index=0,
            chunk_text="Test text",
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
            embedding_service,
        )

        use_case.execute()

        episode_repository.get_all.assert_called_once()
        transcription_repository.get_by_episode_id.assert_called_once_with(episode.id)
        audio_transcriptor.transcribe.assert_called_once_with(episode)
        transcription_repository.save.assert_called_once_with(transcription)
        embedding_service.create_embeddings.assert_called_once_with(transcription)
        embedding_repository.save_batch.assert_called_once_with([embedding])

    def test_skips_episode_with_existing_transcription(self):
        episode = EpisodeMother.create_episode(
            id="20250706_test2",
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
        )

        existing_transcription = Transcription(
            episode_id=episode.id,
            text="Existing transcription",
            language="en",
            created_at=datetime.now(),
            duration=900,
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
            embedding_service,
        )

        use_case.execute()

        episode_repository.get_all.assert_called_once()
        transcription_repository.get_by_episode_id.assert_called_once_with(episode.id)
        audio_transcriptor.transcribe.assert_not_called()
        transcription_repository.save.assert_not_called()
        embedding_service.create_embeddings.assert_not_called()
        embedding_repository.save_batch.assert_not_called()

    def test_dry_run_processes_only_first_episode(self):
        episode1 = EpisodeMother.create_episode(
            id="20250706_test3",
            title="Test Episode 1",
            description="Test Description 1",
            url="https://example.com/test1.mp3",
            local_file_path="/path/to/test1.mp3",
        )

        episode2 = EpisodeMother.create_episode(
            id="20250706_test4",
            title="Test Episode 2",
            description="Test Description 2",
            url="https://example.com/test2.mp3",
            local_file_path="/path/to/test2.mp3",
        )

        transcription = Transcription(
            episode_id=episode1.id,
            text="Test transcription",
            language="en",
            created_at=datetime.now(),
            duration=900,
        )

        episode_repository = Mock()
        episode_repository.get_all.return_value = [episode1, episode2]

        transcription_repository = Mock()
        transcription_repository.get_by_episode_id.return_value = None

        embedding_repository = Mock()

        audio_transcriptor = Mock()
        audio_transcriptor.transcribe.return_value = transcription

        embedding_service = Mock()
        embedding_service.create_embeddings.return_value = []

        use_case = ProcessEpisodesUseCase(
            episode_repository,
            transcription_repository,
            embedding_repository,
            audio_transcriptor,
            embedding_service,
        )

        use_case.execute(dry_run=True)

        episode_repository.get_all.assert_called_once()
        assert transcription_repository.get_by_episode_id.call_count == 1
        assert audio_transcriptor.transcribe.call_count == 1
        assert transcription_repository.save.call_count == 1
        embedding_service.create_embeddings.assert_not_called()
        embedding_repository.save_batch.assert_not_called()

    def test_dry_run_with_no_episodes(self):
        episode_repository = Mock()
        episode_repository.get_all.return_value = []

        transcription_repository = Mock()
        embedding_repository = Mock()
        audio_transcriptor = Mock()
        embedding_service = Mock()

        use_case = ProcessEpisodesUseCase(
            episode_repository,
            transcription_repository,
            embedding_repository,
            audio_transcriptor,
            embedding_service,
        )

        use_case.execute(dry_run=True)

        episode_repository.get_all.assert_called_once()
        transcription_repository.get_by_episode_id.assert_not_called()
        audio_transcriptor.transcribe.assert_not_called()
