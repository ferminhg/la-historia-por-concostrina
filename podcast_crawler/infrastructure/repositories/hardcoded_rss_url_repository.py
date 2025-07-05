from datetime import datetime
from typing import List

from domain.entities.podcast import Episode, Podcast
from domain.repositories.rss_url_repository import RSSUrlRepository


class HardcodedRSSUrlRepository(RSSUrlRepository):

    def search(self) -> List[Podcast]:
        return [
            Podcast(
                title="Cualquier tiempo pasado fue anterior",
                description="Podcast histórico de Nieves Concostrina",
                feed_url="https://fapi-top.prisasd.com/podcast/playser/cualquier_tiempo_pasado_fue_anterior/itunestfp/podcast.xml",
                episodes=[
                    Episode(
                        title="Episodio ejemplo 1",
                        description="Descripción del episodio 1",
                        url="https://example.com/episode1.mp3",
                        published_date=datetime.now(),
                        duration=3600,
                        file_size=50000000,
                    )
                ],
                last_updated=datetime.now(),
            ),
            Podcast(
                title="Todo Concostrina",
                description="Podcast principal de Nieves Concostrina",
                feed_url="https://fapi-top.prisasd.com/podcast/playser/todo_concostrina/itunestfp/podcast.xml",
                episodes=[
                    Episode(
                        title="Episodio ejemplo 2",
                        description="Descripción del episodio 2",
                        url="https://example.com/episode2.mp3",
                        published_date=datetime.now(),
                        duration=3000,
                        file_size=40000000,
                    )
                ],
                last_updated=datetime.now(),
            ),
        ]