import unittest
from abc import ABC
from typing import List

from domain.entities.podcast import Episode
from domain.repositories.episode_repository import EpisodeRepository
from tests.helpers.podcast_mother import EpisodeMother


class TestEpisodeRepository(unittest.TestCase):
    def test_episode_repository_is_abstract_base_class(self):
        self.assertTrue(issubclass(EpisodeRepository, ABC))

    def test_episode_repository_has_save_method(self):
        self.assertTrue(hasattr(EpisodeRepository, "save"))
        self.assertTrue(callable(getattr(EpisodeRepository, "save")))

    def test_episode_repository_has_find_all_method(self):
        self.assertTrue(hasattr(EpisodeRepository, "find_all"))
        self.assertTrue(callable(getattr(EpisodeRepository, "find_all")))

    def test_episode_repository_has_find_by_title_method(self):
        self.assertTrue(hasattr(EpisodeRepository, "find_by_title"))
        self.assertTrue(callable(getattr(EpisodeRepository, "find_by_title")))

    def test_cannot_instantiate_abstract_repository(self):
        with self.assertRaises(TypeError):
            EpisodeRepository()

    def test_concrete_implementation_must_implement_all_methods(self):
        class IncompleteRepository(EpisodeRepository):
            pass

        with self.assertRaises(TypeError):
            IncompleteRepository()

    def test_concrete_implementation_with_all_methods_can_be_instantiated(self):
        class CompleteRepository(EpisodeRepository):
            def save(self, episodes: List[Episode]) -> None:
                pass

            def find_all(self) -> List[Episode]:
                return []

            def find_by_title(self, title: str) -> Episode:
                return EpisodeMother.with_title(title)

        repository = CompleteRepository()
        self.assertIsInstance(repository, EpisodeRepository)

    def test_save_method_signature(self):
        class TestRepository(EpisodeRepository):
            def save(self, episodes: List[Episode]) -> None:
                self.saved_episodes = episodes

            def find_all(self) -> List[Episode]:
                return getattr(self, "saved_episodes", [])

            def find_by_title(self, title: str) -> Episode:
                return EpisodeMother.with_title(title)

        repository = TestRepository()
        episodes = [EpisodeMother.with_title("Test Episode")]

        repository.save(episodes)

        self.assertEqual(repository.saved_episodes, episodes)

    def test_find_all_method_signature(self):
        class TestRepository(EpisodeRepository):
            def __init__(self):
                self.episodes = [EpisodeMother.with_title("Test Episode")]

            def save(self, episodes: List[Episode]) -> None:
                pass

            def find_all(self) -> List[Episode]:
                return self.episodes

            def find_by_title(self, title: str) -> Episode:
                return EpisodeMother.with_title(title)

        repository = TestRepository()

        result = repository.find_all()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Test Episode")

    def test_find_by_title_method_signature(self):
        class TestRepository(EpisodeRepository):
            def save(self, episodes: List[Episode]) -> None:
                pass

            def find_all(self) -> List[Episode]:
                return []

            def find_by_title(self, title: str) -> Episode:
                return EpisodeMother.with_title(title)

        repository = TestRepository()

        result = repository.find_by_title("Test Title")

        self.assertIsInstance(result, Episode)
        self.assertEqual(result.title, "Test Title")


if __name__ == "__main__":
    unittest.main()
