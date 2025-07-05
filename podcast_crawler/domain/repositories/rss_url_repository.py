from abc import ABC, abstractmethod
from typing import List

from domain.entities.podcast import Podcast


class RSSUrlRepository(ABC):

    @abstractmethod
    def search(self) -> List[Podcast]:
        pass