import os
import sys
import unittest
from unittest.mock import Mock, call

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.use_cases.crawl_podcast import CrawlPodcastUseCase
from domain.entities.podcast import Episode
from domain.repositories.episode_repository import EpisodeRepository
from domain.repositories.rss_url_repository import RSSUrlRepository
from tests.helpers.podcast_mother import EpisodeMother


class TestCrawlPodcastUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_rss_url_repository = Mock(spec=RSSUrlRepository)
        self.mock_episode_repository = Mock(spec=EpisodeRepository)
        self.use_case = CrawlPodcastUseCase(
            rss_url_repository=self.mock_rss_url_repository,
            episode_repository=self.mock_episode_repository,
        )

    def test_execute_calls_rss_url_repository_search(self):
        episodes = [EpisodeMother.with_title("Test Episode")]
        self.mock_rss_url_repository.search.return_value = episodes

        self.use_case.execute()

        self.mock_rss_url_repository.search.assert_called_once()

    def test_execute_saves_episodes_to_repository(self):
        episodes = [
            EpisodeMother.with_title("Episode 1"),
            EpisodeMother.with_title("Episode 2"),
        ]
        self.mock_rss_url_repository.search.return_value = episodes

        self.use_case.execute()

        self.mock_episode_repository.save.assert_called_once_with(episodes)

    def test_execute_returns_episodes_from_rss_repository(self):
        episodes = [
            EpisodeMother.with_title("Episode 1"),
            EpisodeMother.with_title("Episode 2"),
        ]
        self.mock_rss_url_repository.search.return_value = episodes

        result = self.use_case.execute()

        self.assertEqual(result, episodes)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Episode 1")
        self.assertEqual(result[1].title, "Episode 2")

    def test_execute_saves_episodes_before_returning(self):
        episodes = [EpisodeMother.with_title("Test Episode")]
        self.mock_rss_url_repository.search.return_value = episodes

        result = self.use_case.execute()

        expected_calls = [call.search(), call.save(episodes)]

        actual_calls = (
            self.mock_rss_url_repository.method_calls
            + self.mock_episode_repository.method_calls
        )

        self.assertEqual(len(actual_calls), 2)
        self.mock_rss_url_repository.search.assert_called_once()
        self.mock_episode_repository.save.assert_called_once_with(episodes)

    def test_execute_handles_empty_episode_list(self):
        episodes = []
        self.mock_rss_url_repository.search.return_value = episodes

        result = self.use_case.execute()

        self.assertEqual(result, [])
        self.mock_episode_repository.save.assert_called_once_with([])

    def test_execute_propagates_repository_exceptions(self):
        self.mock_rss_url_repository.search.side_effect = Exception(
            "RSS repository error"
        )

        with self.assertRaises(Exception) as context:
            self.use_case.execute()

        self.assertEqual(str(context.exception), "RSS repository error")
        self.mock_episode_repository.save.assert_not_called()

    def test_execute_saves_even_when_episode_repository_fails(self):
        episodes = [EpisodeMother.with_title("Test Episode")]
        self.mock_rss_url_repository.search.return_value = episodes
        self.mock_episode_repository.save.side_effect = Exception("Save error")

        with self.assertRaises(Exception) as context:
            self.use_case.execute()

        self.assertEqual(str(context.exception), "Save error")
        self.mock_rss_url_repository.search.assert_called_once()
        self.mock_episode_repository.save.assert_called_once_with(episodes)

    def test_constructor_accepts_required_dependencies(self):
        rss_repository = Mock(spec=RSSUrlRepository)
        episode_repository = Mock(spec=EpisodeRepository)

        use_case = CrawlPodcastUseCase(
            rss_url_repository=rss_repository, episode_repository=episode_repository
        )

        self.assertEqual(use_case.rss_url_repository, rss_repository)
        self.assertEqual(use_case.episode_repository, episode_repository)


if __name__ == "__main__":
    unittest.main()
