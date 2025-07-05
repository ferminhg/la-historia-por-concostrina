import json
import os
import tempfile
import unittest
from datetime import datetime
from typing import List

from domain.entities.podcast import Episode, Podcast
from infrastructure.repositories.json_episode_repository import JSONEpisodeRepository
from tests.helpers.podcast_mother import EpisodeMother, PodcastMother


class TestJSONEpisodeRepository(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        self.temp_file.close()
        self.file_path = self.temp_file.name
        self.repository = JSONEpisodeRepository(self.file_path)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.unlink(self.file_path)

    def test_saves_episodes_to_json_file(self):
        episodes = [
            EpisodeMother.with_title("Episode 1"),
            EpisodeMother.with_title("Episode 2"),
        ]

        self.repository.save(episodes)

        self.assertTrue(os.path.exists(self.file_path))
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Episode 1")
        self.assertEqual(data[1]["title"], "Episode 2")

    def test_saves_episode_with_podcast_data(self):
        podcast = PodcastMother.with_title("Test Podcast")
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime(2023, 1, 1, 12, 0, 0),
            duration=1800,
            file_size=50000000,
            podcast=podcast,
            local_file_path="/path/to/local/file.mp3",
        )

        self.repository.save([episode])

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(len(data), 1)
        episode_data = data[0]
        self.assertEqual(episode_data["title"], "Test Episode")
        self.assertEqual(episode_data["description"], "Test Description")
        self.assertEqual(episode_data["url"], "https://example.com/test.mp3")
        self.assertEqual(episode_data["published_date"], "2023-01-01T12:00:00")
        self.assertEqual(episode_data["duration"], 1800)
        self.assertEqual(episode_data["file_size"], 50000000)
        self.assertEqual(episode_data["local_file_path"], "/path/to/local/file.mp3")

        self.assertIsNotNone(episode_data["podcast"])
        self.assertEqual(episode_data["podcast"]["title"], "Test Podcast")

    def test_saves_episode_without_podcast_data(self):
        episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime(2023, 1, 1, 12, 0, 0),
            duration=1800,
            file_size=50000000,
            podcast=None,
            local_file_path=None,
        )

        self.repository.save([episode])

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        episode_data = data[0]
        self.assertIsNone(episode_data["podcast"])
        self.assertIsNone(episode_data["local_file_path"])

    def test_find_all_returns_empty_list_when_file_not_exists(self):
        os.unlink(self.file_path)

        episodes = self.repository.find_all()

        self.assertEqual(len(episodes), 0)

    def test_find_all_returns_saved_episodes(self):
        original_episodes = [
            EpisodeMother.with_title("Episode 1"),
            EpisodeMother.with_title("Episode 2"),
        ]

        self.repository.save(original_episodes)

        loaded_episodes = self.repository.find_all()

        self.assertEqual(len(loaded_episodes), 2)
        self.assertEqual(loaded_episodes[0].title, "Episode 1")
        self.assertEqual(loaded_episodes[1].title, "Episode 2")

    def test_find_all_preserves_episode_properties(self):
        podcast = Podcast(
            title="Test Podcast",
            description="Test Description",
            feed_url="https://example.com/feed.xml",
            last_updated=datetime(2023, 1, 1, 10, 0, 0),
        )

        original_episode = Episode(
            title="Test Episode",
            description="Test Description",
            url="https://example.com/test.mp3",
            published_date=datetime(2023, 1, 1, 12, 0, 0),
            duration=1800,
            file_size=50000000,
            podcast=podcast,
            local_file_path="/path/to/local/file.mp3",
        )

        self.repository.save([original_episode])

        loaded_episodes = self.repository.find_all()
        loaded_episode = loaded_episodes[0]

        self.assertEqual(loaded_episode.title, original_episode.title)
        self.assertEqual(loaded_episode.description, original_episode.description)
        self.assertEqual(loaded_episode.url, original_episode.url)
        self.assertEqual(loaded_episode.published_date, original_episode.published_date)
        self.assertEqual(loaded_episode.duration, original_episode.duration)
        self.assertEqual(loaded_episode.file_size, original_episode.file_size)
        self.assertEqual(
            loaded_episode.local_file_path, original_episode.local_file_path
        )

        self.assertIsNotNone(loaded_episode.podcast)
        self.assertEqual(loaded_episode.podcast.title, podcast.title)
        self.assertEqual(loaded_episode.podcast.description, podcast.description)
        self.assertEqual(loaded_episode.podcast.feed_url, podcast.feed_url)
        self.assertEqual(loaded_episode.podcast.last_updated, podcast.last_updated)

    def test_find_by_title_returns_matching_episode(self):
        episodes = [
            EpisodeMother.with_title("Episode 1"),
            EpisodeMother.with_title("Episode 2"),
            EpisodeMother.with_title("Episode 3"),
        ]

        self.repository.save(episodes)

        found_episode = self.repository.find_by_title("Episode 2")

        self.assertEqual(found_episode.title, "Episode 2")

    def test_find_by_title_raises_error_when_not_found(self):
        episodes = [EpisodeMother.with_title("Episode 1")]

        self.repository.save(episodes)

        with self.assertRaises(ValueError) as context:
            self.repository.find_by_title("Non-existent Episode")

        self.assertIn(
            "Episode with title 'Non-existent Episode' not found",
            str(context.exception),
        )

    def test_overwrites_existing_file_on_save(self):
        initial_episodes = [EpisodeMother.with_title("Initial Episode")]
        self.repository.save(initial_episodes)

        new_episodes = [
            EpisodeMother.with_title("New Episode 1"),
            EpisodeMother.with_title("New Episode 2"),
        ]
        self.repository.save(new_episodes)

        loaded_episodes = self.repository.find_all()

        self.assertEqual(len(loaded_episodes), 2)
        self.assertEqual(loaded_episodes[0].title, "New Episode 1")
        self.assertEqual(loaded_episodes[1].title, "New Episode 2")

    def test_handles_utf8_characters_correctly(self):
        episode = Episode(
            title="Episodio con caracteres especiales: ñáéíóú",
            description="Descripción con tildes y eñes",
            url="https://example.com/test.mp3",
            published_date=datetime(2023, 1, 1, 12, 0, 0),
        )

        self.repository.save([episode])

        loaded_episodes = self.repository.find_all()
        loaded_episode = loaded_episodes[0]

        self.assertEqual(
            loaded_episode.title, "Episodio con caracteres especiales: ñáéíóú"
        )
        self.assertEqual(loaded_episode.description, "Descripción con tildes y eñes")


if __name__ == "__main__":
    unittest.main()
