import json
from datetime import datetime
from typing import List, Optional

from domain.entities.podcast import Episode, Podcast
from domain.repositories.episode_repository import EpisodeRepository


class JSONEpisodeRepository(EpisodeRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, episodes: List[Episode]) -> None:
        episodes_data = []
        for episode in episodes:
            episode_dict = {
                "title": episode.title,
                "description": episode.description,
                "url": episode.url,
                "published_date": episode.published_date.isoformat(),
                "duration": episode.duration,
                "file_size": episode.file_size,
                "local_file_path": episode.local_file_path,
                "podcast": None,
            }

            if episode.podcast:
                episode_dict["podcast"] = {
                    "title": episode.podcast.title,
                    "description": episode.podcast.description,
                    "feed_url": episode.podcast.feed_url,
                    "last_updated": episode.podcast.last_updated.isoformat(),
                }

            episodes_data.append(episode_dict)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(episodes_data, f, indent=2, ensure_ascii=False)

    def find_all(self) -> List[Episode]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                episodes_data = json.load(f)

            episodes = []
            for episode_dict in episodes_data:
                podcast = None
                if episode_dict.get("podcast"):
                    podcast_data = episode_dict["podcast"]
                    podcast = Podcast(
                        title=podcast_data["title"],
                        description=podcast_data["description"],
                        feed_url=podcast_data["feed_url"],
                        last_updated=datetime.fromisoformat(
                            podcast_data["last_updated"]
                        ),
                    )

                episode = Episode(
                    title=episode_dict["title"],
                    description=episode_dict["description"],
                    url=episode_dict["url"],
                    published_date=datetime.fromisoformat(
                        episode_dict["published_date"]
                    ),
                    duration=episode_dict.get("duration"),
                    file_size=episode_dict.get("file_size"),
                    podcast=podcast,
                    local_file_path=episode_dict.get("local_file_path"),
                )
                episodes.append(episode)

            return episodes
        except FileNotFoundError:
            return []

    def find_by_title(self, title: str) -> Episode:
        episodes = self.find_all()
        for episode in episodes:
            if episode.title == title:
                return episode
        raise ValueError(f"Episode with title '{title}' not found")
