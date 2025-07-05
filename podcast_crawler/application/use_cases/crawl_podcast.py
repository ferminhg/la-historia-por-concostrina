from typing import List

from domain.entities.podcast import Episode
from domain.repositories.episode_repository import EpisodeRepository
from domain.repositories.rss_url_repository import RSSUrlRepository


class CrawlPodcastUseCase:
    def __init__(
        self,
        rss_url_repository: RSSUrlRepository,
        episode_repository: EpisodeRepository,
    ):
        self.rss_url_repository = rss_url_repository
        self.episode_repository = episode_repository

    def execute(self) -> List[Episode]:
        episodies = self.rss_url_repository.search()

        self.episode_repository.save(episodies)
        return episodies
