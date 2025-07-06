from decimal import Decimal
from datetime import datetime

from ..domain.entities.cost import Cost
from ..domain.repositories.cost_repository import CostRepository


class CostUtils:
    @staticmethod
    def get_daily_summary(cost_repository: CostRepository, date: datetime.date) -> dict:
        all_costs = cost_repository.get_all()
        daily_costs = [c for c in all_costs if c.created_at.date() == date]

        total_cost = sum(c.cost_usd for c in daily_costs)
        total_minutes = sum(c.duration_minutes for c in daily_costs)
        episodes_count = len(daily_costs)

        return {
            "date": date.isoformat(),
            "total_cost_usd": total_cost,
            "total_minutes": total_minutes,
            "episodes_count": episodes_count,
            "average_cost_per_episode": total_cost / episodes_count
            if episodes_count > 0
            else Decimal("0"),
        }

    @staticmethod
    def get_monthly_summary(
        cost_repository: CostRepository, year: int, month: int
    ) -> dict:
        all_costs = cost_repository.get_all()
        monthly_costs = [
            c
            for c in all_costs
            if c.created_at.year == year and c.created_at.month == month
        ]

        total_cost = sum(c.cost_usd for c in monthly_costs)
        total_minutes = sum(c.duration_minutes for c in monthly_costs)
        episodes_count = len(monthly_costs)

        return {
            "year": year,
            "month": month,
            "total_cost_usd": total_cost,
            "total_minutes": total_minutes,
            "episodes_count": episodes_count,
            "average_cost_per_episode": total_cost / episodes_count
            if episodes_count > 0
            else Decimal("0"),
        }

    @staticmethod
    def format_cost_summary(cost_repository: CostRepository) -> str:
        all_costs = cost_repository.get_all()
        if not all_costs:
            return "No cost data available"

        total_cost = cost_repository.get_total_cost()
        total_minutes = sum(c.duration_minutes for c in all_costs)
        total_episodes = len(all_costs)

        avg_cost_per_episode = (
            total_cost / total_episodes if total_episodes > 0 else Decimal("0")
        )
        avg_cost_per_minute = (
            total_cost / Decimal(str(total_minutes))
            if total_minutes > 0
            else Decimal("0")
        )

        return (
            f"💰 Cost Summary:\n"
            f"  Total Cost: ${total_cost:.4f}\n"
            f"  Episodes Transcribed: {total_episodes}\n"
            f"  Total Minutes: {total_minutes:.2f}\n"
            f"  Average Cost/Episode: ${avg_cost_per_episode:.4f}\n"
            f"  Average Cost/Minute: ${avg_cost_per_minute:.4f}"
        )
