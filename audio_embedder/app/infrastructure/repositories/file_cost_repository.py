import json
import os
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ...domain.entities.cost import Cost
from ...domain.repositories.cost_repository import CostRepository
from ...shared.logger import get_logger


class FileCostRepository(CostRepository):
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.logger = get_logger(self.__class__.__name__)
        os.makedirs(base_path, exist_ok=True)

    def save(self, cost: Cost) -> bool:
        file_path = self._get_file_path(cost.episode_id)

        if os.path.exists(file_path):
            self.logger.info(
                f"Cost file already exists for episode {cost.episode_id}, skipping save"
            )
            return False

        data = self._cost_to_dict(cost)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

            self.logger.info(
                f"Cost saved for episode {cost.episode_id}: ${cost.cost_usd:.4f}"
            )
            return True
        except Exception as e:
            self.logger.error(f"Error saving cost for episode {cost.episode_id}: {e}")
            return False

    def find_by_episode_id(self, episode_id: str) -> Optional[Cost]:
        file_path = self._get_file_path(episode_id)
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, encoding="utf-8") as file:
                data = json.load(file)
                return self._dict_to_cost(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def get_all(self) -> list[Cost]:
        costs = []
        for filename in os.listdir(self.base_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.base_path, filename)
                try:
                    with open(file_path, encoding="utf-8") as file:
                        data = json.load(file)
                        costs.append(self._dict_to_cost(data))
                except (json.JSONDecodeError, KeyError):
                    continue
        return costs

    def get_total_cost(self) -> Decimal:
        total = Decimal("0")
        for cost in self.get_all():
            total += cost.cost_usd
        return total

    def _get_file_path(self, episode_id: str) -> str:
        filename = f"{episode_id}_cost.json"
        return os.path.join(self.base_path, filename)

    def _dict_to_cost(self, data: dict) -> Cost:
        return Cost(
            episode_id=data["episode_id"],
            duration_minutes=data["duration_minutes"],
            cost_usd=Decimal(str(data["cost_usd"])),
            api_model=data["api_model"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    def _cost_to_dict(self, cost: Cost) -> dict:
        return {
            "episode_id": cost.episode_id,
            "duration_minutes": cost.duration_minutes,
            "cost_usd": str(cost.cost_usd),
            "api_model": cost.api_model,
            "created_at": cost.created_at.isoformat(),
        }
