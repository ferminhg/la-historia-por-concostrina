from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Cost:
    episode_id: str
    duration_minutes: float
    cost_usd: Decimal
    api_model: str
    created_at: datetime
