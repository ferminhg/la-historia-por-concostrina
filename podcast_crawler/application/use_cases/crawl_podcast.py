from typing import List

from domain.entities.podcast import Episode, Podcast
from domain.repositories.rss_url_repository import RSSUrlRepository


class CrawlPodcastUseCase:
    def __init__(self, rss_url_repository: RSSUrlRepository):
        self.rss_url_repository = rss_url_repository

    def execute(self) -> List[Episode]:
        episodies = self.rss_url_repository.search()

        for episody in episodies:
            print(episody)

        return []
