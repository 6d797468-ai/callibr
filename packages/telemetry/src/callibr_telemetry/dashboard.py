from __future__ import annotations

from dataclasses import dataclass, field

from callibr_telemetry.feedback import get_feedback_store
from callibr_telemetry.product import get_product_event_store


@dataclass
class DashboardOverview:
    simulations_started: int = 0
    simulations_completed: int = 0
    completion_rate: float = 0.0
    average_duration_seconds: float = 0.0
    active_users: int = 0
    total_sessions: int = 0


@dataclass
class DashboardPerformance:
    average_score: float = 0.0
    score_trend: list[dict] = field(default_factory=list)
    weakest_criteria: list[dict] = field(default_factory=list)
    strongest_criteria: list[dict] = field(default_factory=list)


@dataclass
class DashboardProduct:
    average_satisfaction: float = 0.0
    would_use_counts: dict[str, int] = field(default_factory=dict)
    abandon_count: int = 0
    average_time_before_abandon: float = 0.0
    replay_count: int = 0


@dataclass
class DashboardBusiness:
    scenario_ranking: list[dict] = field(default_factory=list)
    difficulty_distribution: dict[str, int] = field(default_factory=dict)
    average_duration_by_scenario: dict[str, float] = field(default_factory=dict)
    satisfaction_by_scenario: dict[str, float] = field(default_factory=dict)


@dataclass
class DashboardData:
    overview: DashboardOverview = field(default_factory=DashboardOverview)
    performance: DashboardPerformance = field(default_factory=DashboardPerformance)
    product: DashboardProduct = field(default_factory=DashboardProduct)
    business: DashboardBusiness = field(default_factory=DashboardBusiness)


class DashboardService:
    def __init__(self, session_store) -> None:
        self._session_store = session_store

    def compute(self) -> DashboardData:
        sessions = self._session_store.list()
        event_store = get_product_event_store()
        feedback_store = get_feedback_store()

        # Overview
        started = event_store.count_by_type().get("ScenarioStarted", 0)
        completed = event_store.count_by_type().get("ConversationCompleted", 0)
        total_sessions = len(sessions)
        completed_sessions = [s for s in sessions if s.status == "completed"]

        durations = []
        learners = set()
        for s in sessions:
            learners.add(s.learner_id)
            if s.completed_at and s.started_at:
                diff = (s.completed_at - s.started_at).total_seconds()
                if diff > 0:
                    durations.append(diff)

        avg_duration = sum(durations) / len(durations) if durations else 0.0

        overview = DashboardOverview(
            simulations_started=started,
            simulations_completed=completed,
            completion_rate=round(completed / started * 100, 1) if started else 0.0,
            average_duration_seconds=round(avg_duration, 1),
            active_users=len(learners),
            total_sessions=total_sessions,
        )

        # Performance
        scores = []
        criteria_scores: dict[str, list[int]] = {}
        for s in completed_sessions:
            if s.evaluation is not None:
                scores.append(s.evaluation.score)
                for c in s.evaluation.criteria:
                    criteria_scores.setdefault(c.label, []).append(
                        int(c.score / c.max_score * 100) if c.max_score else 0
                    )

        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        sorted_criteria = sorted(
            [
                {"label": k, "average": round(sum(v) / len(v), 1)}
                for k, v in criteria_scores.items()
            ],
            key=lambda x: x["average"],
        )
        weakest = sorted_criteria[:5] if len(sorted_criteria) > 5 else sorted_criteria
        strongest = list(reversed(sorted_criteria))[:5] if len(sorted_criteria) > 5 else list(reversed(sorted_criteria))

        performance = DashboardPerformance(
            average_score=avg_score,
            weakest_criteria=weakest,
            strongest_criteria=strongest,
        )

        # Product
        feedback_count = len(feedback_store._records)
        feedback = DashboardProduct(
            average_satisfaction=round(feedback_store.average_satisfaction(), 1) if feedback_count else 0.0,
            would_use_counts=feedback_store.count_would_use(),
            abandon_count=max(0, started - completed),
            replay_count=event_store.count_by_type().get("ReportViewed", 0),
        )

        # Business
        scenario_scores: dict[str, list[int]] = {}
        for s in completed_sessions:
            sid = s.scenario.scenario_id
            scenario_scores.setdefault(sid, []).append(
                s.evaluation.score if s.evaluation else 0
            )

        ranking = sorted(
            [
                {
                    "scenario_id": sid,
                    "title": next(
                        (s.scenario.title for x in sessions if x.scenario.scenario_id == sid),
                        sid,
                    ),
                    "average_score": round(sum(v) / len(v), 1),
                    "count": len(v),
                }
                for sid, v in scenario_scores.items()
            ],
            key=lambda x: x["average_score"],
            reverse=True,
        )

        business = DashboardBusiness(
            scenario_ranking=ranking,
        )

        return DashboardData(
            overview=overview,
            performance=performance,
            product=feedback,
            business=business,
        )
