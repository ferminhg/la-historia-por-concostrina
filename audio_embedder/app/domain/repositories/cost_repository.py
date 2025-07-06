from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal

from ..entities.cost import Cost


class CostRepository(ABC):
    @abstractmethod
    def save(self, cost: Cost) -> bool:
        pass

    @abstractmethod
    def find_by_episode_id(self, episode_id: str) -> Optional[Cost]:
        pass

    @abstractmethod
    def get_all(self) -> list[Cost]:
        pass

    @abstractmethod
    def get_total_cost(self) -> Decimal:
        pass
