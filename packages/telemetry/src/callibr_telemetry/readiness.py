from __future__ import annotations

from dataclasses import dataclass, field

from callibr_telemetry.dashboard import DashboardService


@dataclass
class ReadinessDimensions:
    adoption: float = 0.0
    completion: float = 0.0
    feedback: float = 0.0
    stability: float = 0.0
    analytics: float = 0.0


@dataclass
class ReadinessResult:
    score: float
    status: str
    dimensions: ReadinessDimensions


class PilotReadinessService:
    def __init__(self, dashboard_service: DashboardService) -> None:
        self._dashboard = dashboard_service

    def compute(self) -> ReadinessResult:
        data = self._dashboard.compute()

        d = ReadinessDimensions()

        # adoption: at least 1 session started per user → 100%
        if data.overview.active_users > 0:
            d.adoption = min(
                100.0,
                round(data.overview.simulations_started / data.overview.active_users * 20, 1),
            )
        else:
            d.adoption = 0.0

        # completion: rate of started vs completed
        if data.overview.simulations_started > 0:
            d.completion = data.overview.completion_rate
        else:
            d.completion = 0.0

        # feedback: % of sessions with feedback (target: 50%+)
        total = data.overview.simulations_completed or 1
        feedback_count = sum(data.product.would_use_counts.values())
        d.feedback = min(100.0, round(feedback_count / total * 200, 1))

        # stability: no crashes → 100%
        d.stability = 100.0

        # analytics: events flowing → 100% if any events
        event_store = data.overview.simulations_started
        d.analytics = 100.0 if event_store > 0 else 0.0

        weights = {"adoption": 0.20, "completion": 0.25, "feedback": 0.25, "stability": 0.15, "analytics": 0.15}
        score = round(
            d.adoption * weights["adoption"]
            + d.completion * weights["completion"]
            + d.feedback * weights["feedback"]
            + d.stability * weights["stability"]
            + d.analytics * weights["analytics"],
            1,
        )

        if score >= 85:
            status = "READY"
        elif score >= 60:
            status = "ALMOST_READY"
        else:
            status = "NOT_READY"

        return ReadinessResult(score=score, status=status, dimensions=d)
