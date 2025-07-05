from datetime import datetime
import os
from typing import List

import requests

from domain.entities.podcast import Episode, Podcast
from domain.repositories.rss_url_repository import RSSUrlRepository


class HardcodedRSSUrlRepository(RSSUrlRepository):
    def __init__(self, data_dir: str):
        self.rss_urls = [
            "https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml",
            "https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml",
        ]
        self.data_dir = data_dir

    def search(self) -> List[Episode]:
        for i, rss_url in enumerate(self.rss_urls):
            filename = f'feed_{i+1}.xml'
            filepath = os.path.join(self.data_dir, filename)
            response = requests.get(rss_url)
            response.raise_for_status()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved {filepath} from {rss_url}")

        return []
