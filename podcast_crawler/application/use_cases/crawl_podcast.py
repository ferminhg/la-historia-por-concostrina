from typing import List

from domain.entities.podcast import Podcast
from domain.repositories.rss_url_repository import RSSUrlRepository


class CrawlPodcastUseCase:

    def __init__(self, rss_url_repository: RSSUrlRepository):
        self.rss_url_repository = rss_url_repository

    def execute(self) -> List[Podcast]:
        podcasts = self.rss_url_repository.search()
        
        for podcast in podcasts:
            print(podcast)

        return podcasts
                
    def get_podcasts(self) -> List[Podcast]:
        return self.rss_url_repository.search()