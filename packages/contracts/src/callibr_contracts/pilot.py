from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DashboardOverview:
    simulations_total: int
    success_rate: float
    average_satisfaction: float
    average_duration_minutes: float


@dataclass(frozen=True)
class FunnelStage:
    id: str
    label: str
    count: int
    percentage: float


@dataclass(frozen=True)
class ActivityItem:
    timestamp: str
    actor: str
    action: str
    detail: str


@dataclass(frozen=True)
class DashboardAlert:
    level: str  # "info" | "warning"
    title: str
    message: str


@dataclass(frozen=True)
class PilotDashboard:
    overview: DashboardOverview
    funnel: list[FunnelStage] = field(default_factory=list)
    recent_activity: list[ActivityItem] = field(default_factory=list)
    alerts: list[DashboardAlert] = field(default_factory=list)
