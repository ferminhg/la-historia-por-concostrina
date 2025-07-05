import os
import sys
import tempfile
from datetime import datetime
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.services.episode_downloader import EpisodeDownloader
from infrastructure.repositories.local_file_episode_repository import (
    LocalFileEpisodeRepository,
)
from tests.helpers.podcast_mother import EpisodeMother


class TestEpisodeDownloader:
    def test_downloads_episode_successfully(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)
            downloader = EpisodeDownloader(repository)

            episode = EpisodeMother.with_title("Test Episode")

            with patch("requests.get") as mock_get:
                mock_response = Mock()
                mock_response.raise_for_status.return_value = None
                mock_response.iter_content.return_value = [
                    b"audio_chunk_1",
                    b"audio_chunk_2",
                ]
                mock_get.return_value.__enter__.return_value = mock_response

                episodes = downloader.run([episode])

                assert len(episodes) == 1
                downloaded_episode = episodes[0]
                assert downloaded_episode.local_file_path is not None
                assert os.path.exists(downloaded_episode.local_file_path)

                with open(downloaded_episode.local_file_path, "rb") as f:
                    content = f.read()
                    assert content == b"audio_chunk_1audio_chunk_2"

    def test_skips_download_if_episode_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)
            downloader = EpisodeDownloader(repository)

            episode = EpisodeMother.with_title("Existing Episode")
            file_path = repository.get_file_path(episode)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(b"existing_content")

            episodes = downloader.run([episode])

            assert len(episodes) == 1
            downloaded_episode = episodes[0]
            assert downloaded_episode.local_file_path == file_path

            with open(downloaded_episode.local_file_path, "rb") as f:
                content = f.read()
                assert content == b"existing_content"

    def test_handles_episode_without_url(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)
            downloader = EpisodeDownloader(repository)

            from domain.builders.episode_builder import EpisodeBuilder

            episode = EpisodeMother.with_title("No URL Episode")
            episode_no_url = EpisodeBuilder(episode).with_url("").build()

            episodes = downloader.run([episode_no_url])

            assert len(episodes) == 1
            assert episodes[0].local_file_path is None

    def test_handles_download_error_gracefully(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)
            downloader = EpisodeDownloader(repository)

            episode = EpisodeMother.with_title("Error Episode")

            with patch("requests.get") as mock_get:
                mock_get.side_effect = Exception("Network error")

                episodes = downloader.run([episode])

                assert len(episodes) == 1
                assert episodes[0].local_file_path is None


class TestLocalFileEpisodeRepository:
    def test_saves_episode_audio_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)
            episode = EpisodeMother.random()
            audio_data = b"test_audio_data"

            file_path = repository.save(episode, audio_data)

            assert os.path.exists(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
                assert content == audio_data

    def test_checks_if_episode_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)
            episode = EpisodeMother.random()

            assert not repository.exists(episode)

            repository.save(episode, b"test_data")

            assert repository.exists(episode)

    def test_generates_correct_file_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = LocalFileEpisodeRepository(temp_dir)

            from domain.builders.episode_builder import EpisodeBuilder

            published_date = datetime(2024, 1, 15, 14, 30)
            episode = EpisodeMother.random()
            episode_with_date = (
                EpisodeBuilder(episode).with_published_date(published_date).build()
            )

            file_path = repository.get_file_path(episode_with_date)

            assert file_path.endswith("2024_01_15_14.mp3")
            assert temp_dir in file_path
