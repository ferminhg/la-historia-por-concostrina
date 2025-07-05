from typing import List

import requests

from domain.builders.episode_builder import EpisodeBuilder
from domain.entities.podcast import Episode
from domain.repositories.file_episode_repository import FileEpisodeRepository
from shared.logger import get_logger


class EpisodeDownloader:
    def __init__(self, file_episode_repository: FileEpisodeRepository):
        self.file_episode_repository = file_episode_repository
        self.logger = get_logger(__name__)

    def run(self, episodes: List[Episode]) -> List[Episode]:
        downloaded_episodes = []

        for episode in episodes:
            try:
                downloaded_episode = self._download_episode(episode)
                downloaded_episodes.append(downloaded_episode)
            except Exception as e:
                self.logger.error(f"Error downloading episode {episode.title}: {e}")
                downloaded_episodes.append(episode)

        return downloaded_episodes

    def _download_episode(self, episode: Episode) -> Episode:
        if not episode.url:
            self.logger.warning(
                f"Episode {episode.title} has no URL, skipping download"
            )
            return episode

        if self.file_episode_repository.exists(episode):
            file_path = self.file_episode_repository.get_file_path(episode)
            # self.logger.info(f"Episode {episode.title} already exists at {file_path}, skipping download")
            return EpisodeBuilder(episode).with_local_file_path(file_path).build()

        self.logger.info(f"Downloading episode: {episode.title}")

        with requests.get(episode.url, stream=True) as response:
            response.raise_for_status()
            audio_data = b""

            for chunk in response.iter_content(chunk_size=8192):
                audio_data += chunk

        file_path = self.file_episode_repository.save(episode, audio_data)

        return EpisodeBuilder(episode).with_local_file_path(file_path).build()
