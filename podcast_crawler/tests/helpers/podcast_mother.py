import random
import string
from datetime import datetime, timedelta
from typing import List, Optional

from domain.entities.podcast import Episode, Podcast


class EpisodeBuilder:
    def __init__(self):
        self._title = self._random_string()
        self._description = self._random_string(50)
        self._url = f"https://example.com/{self._random_string()}.mp3"
        self._published_date = self._random_date()
        self._duration = random.randint(600, 7200)
        self._file_size = random.randint(10000000, 100000000)

    def with_title(self, title: str) -> "EpisodeBuilder":
        self._title = title
        return self

    def with_description(self, description: str) -> "EpisodeBuilder":
        self._description = description
        return self

    def with_url(self, url: str) -> "EpisodeBuilder":
        self._url = url
        return self

    def with_published_date(self, published_date: datetime) -> "EpisodeBuilder":
        self._published_date = published_date
        return self

    def with_duration(self, duration: Optional[int]) -> "EpisodeBuilder":
        self._duration = duration
        return self

    def with_file_size(self, file_size: Optional[int]) -> "EpisodeBuilder":
        self._file_size = file_size
        return self

    def build(self) -> Episode:
        return Episode(
            title=self._title,
            description=self._description,
            url=self._url,
            published_date=self._published_date,
            duration=self._duration,
            file_size=self._file_size,
        )

    @staticmethod
    def _random_string(length: int = 10) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def _random_date() -> datetime:
        start_date = datetime.now() - timedelta(days=365)
        random_days = random.randint(0, 365)
        return start_date + timedelta(days=random_days)


class PodcastBuilder:
    def __init__(self):
        self._title = self._random_string()
        self._description = self._random_string(100)
        self._feed_url = f"https://example.com/{self._random_string()}/podcast.xml"
        self._episodes = [EpisodeBuilder().build()]
        self._last_updated = datetime.now()

    def with_title(self, title: str) -> "PodcastBuilder":
        self._title = title
        return self

    def with_description(self, description: str) -> "PodcastBuilder":
        self._description = description
        return self

    def with_feed_url(self, feed_url: str) -> "PodcastBuilder":
        self._feed_url = feed_url
        return self

    def with_episodes(self, episodes: List[Episode]) -> "PodcastBuilder":
        self._episodes = episodes
        return self

    def with_episode_count(self, count: int) -> "PodcastBuilder":
        self._episodes = [EpisodeBuilder().build() for _ in range(count)]
        return self

    def with_last_updated(self, last_updated: datetime) -> "PodcastBuilder":
        self._last_updated = last_updated
        return self

    def build(self) -> Podcast:
        return Podcast(
            title=self._title,
            description=self._description,
            feed_url=self._feed_url,
            episodes=self._episodes,
            last_updated=self._last_updated,
        )

    @staticmethod
    def _random_string(length: int = 10) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class PodcastMother:
    @staticmethod
    def random() -> Podcast:
        return PodcastBuilder().build()

    @staticmethod
    def with_title(title: str) -> Podcast:
        return PodcastBuilder().with_title(title).build()

    @staticmethod
    def with_episodes(episodes: List[Episode]) -> Podcast:
        return PodcastBuilder().with_episodes(episodes).build()

    @staticmethod
    def with_episode_count(count: int) -> Podcast:
        return PodcastBuilder().with_episode_count(count).build()

    @staticmethod
    def empty() -> Podcast:
        return PodcastBuilder().with_episodes([]).build()

    @staticmethod
    def history_podcast() -> Podcast:
        return (
            PodcastBuilder()
            .with_title("Any Past Time Was Earlier")
            .with_description("Historical podcast by Nieves Concostrina")
            .with_feed_url(
                "https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml"
            )
            .build()
        )

    @staticmethod
    def concostrina_podcast() -> Podcast:
        return (
            PodcastBuilder()
            .with_title("All Concostrina")
            .with_description("Main podcast by Nieves Concostrina")
            .with_feed_url(
                "https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml"
            )
            .build()
        )


class EpisodeMother:
    @staticmethod
    def random() -> Episode:
        return EpisodeBuilder().build()

    @staticmethod
    def with_title(title: str) -> Episode:
        return EpisodeBuilder().with_title(title).build()

    @staticmethod
    def with_duration(duration: int) -> Episode:
        return EpisodeBuilder().with_duration(duration).build()

    @staticmethod
    def long_episode() -> Episode:
        return EpisodeBuilder().with_duration(7200).build()

    @staticmethod
    def short_episode() -> Episode:
        return EpisodeBuilder().with_duration(600).build()