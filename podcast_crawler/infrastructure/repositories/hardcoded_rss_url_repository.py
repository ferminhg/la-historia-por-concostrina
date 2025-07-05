import os
from datetime import datetime
from typing import List

import requests

from application.services.episode_downloader import EpisodeDownloader
from domain.entities.podcast import Episode
from domain.repositories.rss_url_repository import RSSUrlRepository
from infrastructure.xml.xml_processor import XMLProcessor
from shared.logger import get_logger


class HardcodedRSSUrlRepository(RSSUrlRepository):
    def __init__(self, data_dir: str, episode_downloader: EpisodeDownloader):
        self.rss_urls = [
            "https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml",
            "https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml",
        ]
        self.data_dir = data_dir
        self.logger = get_logger(__name__)
        self.xml_processor = XMLProcessor()

        self.episode_downloader = episode_downloader

    def search(self) -> List[Episode]:
        all_episodes = []

        for i, rss_url in enumerate(self.rss_urls):
            filepath = build_rss_filename(i, self.data_dir)
            self._save_rss_to_file(rss_url, filepath)
            episodes = self.xml_processor.run(filepath)
            all_episodes.extend(episodes)

        downloaded_episodes = self.episode_downloader.run(all_episodes)
        return downloaded_episodes

    def _save_rss_to_file(self, rss_url: str, filepath: str):
        response = requests.get(rss_url)
        response.raise_for_status()

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        self.logger.info(f"Saved {filepath} from {rss_url}")


def build_rss_filename(index: int, data_dir: str) -> str:
    filename = f"feed_{index + 1}.xml"
    return os.path.join(data_dir, filename)
