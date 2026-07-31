from __future__ import annotations

from callibr_contracts.pilot import (
    ActivityItem,
    DashboardAlert,
    DashboardOverview,
    FunnelStage,
    PilotDashboard,
)
from callibr_contracts.telemetry import ProductEvent

_FUNNEL_STAGES: list[tuple[str, str, str]] = [
    ("premier_lancement", "Premier lancement", "ApplicationOpened"),
    ("wizard_termine", "Wizard terminé", "WizardCompleted"),
    ("simulation_lancee", "Simulation lancée", "ScenarioStarted"),
    ("simulation_terminee", "Simulation terminée", "ConversationCompleted"),
    ("rapport_ouvert", "Rapport consulté", "ReportViewed"),
    ("feedback_envoye", "Feedback envoyé", "FeedbackSubmitted"),
]

_ACTION_LABELS: dict[str, str] = {
    "ApplicationOpened": "Application ouverte",
    "LoginSucceeded": "Connexion réussie",
    "ScenarioViewed": "Scénario consulté",
    "ScenarioStarted": "Simulation lancée",
    "FirstMessageSent": "Premier message envoyé",
    "ConversationCompleted": "Simulation terminée",
    "WizardCompleted": "Wizard terminé",
    "ProcedureCompleted": "Procédure terminée",
    "ReportViewed": "Rapport consulté",
    "ReportExported": "Rapport exporté",
    "SessionResumed": "Session reprise",
    "SessionAbandoned": "Session abandonnée",
    "FeedbackSubmitted": "Feedback envoyé",
}

_SUCCESS_THRESHOLD = 70
_TARGET_DURATION_MINUTES = 15.0
_TARGET_SATISFACTION = 4.0


class PilotDashboardService:
    """Business cockpit for a pilot manager.

    Feeds only from the persistence stores (sessions, feedback, product
    events). No technical metrics: no tokens, no budgets, no latency,
    no model/provider details.
    """

    def __init__(self, session_store, feedback_store, product_event_store) -> None:
        self._session_store = session_store
        self._feedback_store = feedback_store
        self._product_event_store = product_event_store

    def compute(self) -> PilotDashboard:
        sessions = self._session_store.list()
        counts = self._product_event_store.count_by_type()
        feedback_count = self._feedback_store.count()

        overview = self._overview(sessions)
        funnel = self._funnel(counts)
        recent_activity = self._recent_activity(sessions)
        alerts = self._alerts(overview, counts, feedback_count)

        return PilotDashboard(
            overview=overview,
            funnel=funnel,
            recent_activity=recent_activity,
            alerts=alerts,
        )

    def _overview(self, sessions) -> DashboardOverview:
        simulations_total = len(sessions)
        passed = [
            s
            for s in sessions
            if s.status == "completed" and s.evaluation is not None
            and s.evaluation.score >= _SUCCESS_THRESHOLD
        ]
        success_rate = round(len(passed) / simulations_total * 100, 1) if simulations_total else 0.0

        feedback_count = self._feedback_store.count()
        average_satisfaction = (
            round(self._feedback_store.average_satisfaction(), 1) if feedback_count else 0.0
        )

        durations = [
            (s.completed_at - s.started_at).total_seconds() / 60.0
            for s in sessions
            if s.completed_at and s.started_at
        ]
        average_duration_minutes = round(sum(durations) / len(durations), 1) if durations else 0.0

        return DashboardOverview(
            simulations_total=simulations_total,
            success_rate=success_rate,
            average_satisfaction=average_satisfaction,
            average_duration_minutes=average_duration_minutes,
        )

    def _funnel(self, counts: dict[str, int]) -> list[FunnelStage]:
        stage_counts = [counts.get(event_type, 0) for _, _, event_type in _FUNNEL_STAGES]
        base = next((c for c in stage_counts if c > 0), 0)
        return [
            FunnelStage(
                id=stage_id,
                label=label,
                count=count,
                percentage=round(count / base * 100, 1) if base else 0.0,
            )
            for (stage_id, label, event_type), count in zip(_FUNNEL_STAGES, stage_counts, strict=True)
        ]

    def _recent_activity(self, sessions) -> list[ActivityItem]:
        actor_by_session = {s.session_id: s.learner_id for s in sessions}
        scenario_title_by_session = {s.session_id: s.scenario.title for s in sessions}
        score_by_session = {
            s.session_id: s.evaluation.score
            for s in sessions
            if s.evaluation is not None
        }

        items: list[ActivityItem] = []
        for event in self._product_event_store.list(limit=100):
            if event.event_type == "FeedbackSubmitted":
                continue
            items.append(
                ActivityItem(
                    timestamp=event.timestamp,
                    actor=actor_by_session.get(event.session_id, ""),
                    action=_ACTION_LABELS.get(event.event_type, event.event_type),
                    detail=self._event_detail(
                        event, scenario_title_by_session, score_by_session
                    ),
                )
            )
        for feedback in self._feedback_store.list(limit=100):
            items.append(
                ActivityItem(
                    timestamp=feedback.submitted_at,
                    actor=actor_by_session.get(feedback.session_id, ""),
                    action="Feedback envoyé",
                    detail="★" * feedback.satisfaction,
                )
            )

        items.sort(key=lambda item: item.timestamp, reverse=True)
        return items[:10]

    def _event_detail(
        self,
        event: ProductEvent,
        scenario_title_by_session: dict[str, str],
        score_by_session: dict[str, int],
    ) -> str:
        if event.event_type == "ConversationCompleted":
            score = score_by_session.get(event.session_id)
            return f"Score {score}/100" if score is not None else ""
        if event.event_type == "ScenarioStarted":
            return scenario_title_by_session.get(event.session_id, "")
        return ""

    def _alerts(
        self,
        overview: DashboardOverview,
        counts: dict[str, int],
        feedback_count: int,
    ) -> list[DashboardAlert]:
        alerts: list[DashboardAlert] = []
        scenarios_started = counts.get("ScenarioStarted", 0)
        conversations_completed = counts.get("ConversationCompleted", 0)
        abandons = max(0, scenarios_started - conversations_completed)
        if abandons > 0:
            label = "simulation abandonnée" if abandons == 1 else "simulations abandonnées"
            alerts.append(
                DashboardAlert(
                    level="warning",
                    title=f"{abandons} {label}",
                    message=(
                        "Des simulations lancées n'ont jamais été terminées. "
                        "Vérifiez les scénarios concernés et l'engagement des apprenants."
                    ),
                )
            )
        if overview.simulations_total and overview.average_duration_minutes > _TARGET_DURATION_MINUTES:
            alerts.append(
                DashboardAlert(
                    level="warning",
                    title="Durée moyenne supérieure à 15 min",
                    message=(
                        f"{overview.average_duration_minutes} min en moyenne par simulation, "
                        "au-delà de la cible de 15 min."
                    ),
                )
            )
        if feedback_count and overview.average_satisfaction < _TARGET_SATISFACTION:
            alerts.append(
                DashboardAlert(
                    level="warning",
                    title="Satisfaction sous la cible (4/5)",
                    message=(
                        f"{overview.average_satisfaction}/5 en moyenne, en dessous de la cible. "
                        "Relancez le formulaire de feedback auprès des apprenants."
                    ),
                )
            )

        if not alerts:
            if overview.simulations_total or scenarios_started:
                alerts.append(
                    DashboardAlert(
                        level="info",
                        title="Système sain",
                        message="Aucun problème détecté — tous les indicateurs sont dans les cibles.",
                    )
                )
            else:
                alerts.append(
                    DashboardAlert(
                        level="info",
                        title="Premières données attendues",
                        message=(
                            "Aucune simulation pour l'instant — lancez votre première "
                            "formation pour remplir ce tableau de bord."
                        ),
                    )
                )
        return alerts
