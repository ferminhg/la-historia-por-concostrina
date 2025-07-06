import json
from datetime import datetime
from typing import Optional

from ...domain.entities.episode import Episode
from ...domain.repositories.episode_repository import EpisodeRepository


class JSONEpisodeRepository(EpisodeRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self) -> list[Episode]:
        try:
            with open(self.file_path, encoding="utf-8") as file:
                data = json.load(file)
                return [self._dict_to_episode(item) for item in data]
        except FileNotFoundError:
            return []

    def get_by_id(self, episode_id: str) -> Optional[Episode]:
        episodes = self.get_all()
        for episode in episodes:
            if episode.url == episode_id:
                return episode
        return None

    def save(self, episode: Episode) -> Episode:
        return episode

    def _dict_to_episode(self, data: dict) -> Episode:
        return Episode(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            url=data["url"],
            published_date=datetime.fromisoformat(
                data["published_date"].replace("Z", "+00:00")
            ),
            duration=data["duration"],
            file_size=data["file_size"],
            local_file_path=data.get("local_file_path"),
            podcast=data.get("podcast"),
        )
