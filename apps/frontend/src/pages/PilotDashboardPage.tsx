import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";
import ErrorPanel from "../components/ErrorPanel";
import { friendlyError, type UserFacingError } from "../lib/errors";

type FunnelStage = {
  id: string;
  label: string;
  count: number;
  percentage: number;
};

type ActivityItem = {
  timestamp: string;
  actor: string;
  action: string;
  detail: string;
};

type DashboardAlert = {
  level: "info" | "warning";
  title: string;
  message: string;
};

type PilotDashboard = {
  overview: {
    simulations_total: number;
    success_rate: number;
    average_satisfaction: number;
    average_duration_minutes: number;
  };
  funnel: FunnelStage[];
  recent_activity: ActivityItem[];
  alerts: DashboardAlert[];
};

type Props = {
  token: string | null;
};

function formatDuration(minutes: number): string {
  if (minutes <= 0) return "—";
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  return `${h}h${m > 0 ? ` ${m}min` : ""}`;
}

function formatTimestamp(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatActor(actor: string): string {
  if (!actor) return "Apprenant";
  return actor.replace(/^(learner|agent)_/, "");
}

export default function PilotDashboardPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [data, setData] = useState<PilotDashboard | null>(null);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!bearer) { navigate("/"); return; }
    setError(null);
    apiFetch<PilotDashboard>("/api/v1/pilot/dashboard", bearer)
      .then(setData)
      .catch((err) => setError(friendlyError(err)));
  }, [bearer, navigate, attempt]);

  if (error) {
    return (
      <div className="dashboard-page error">
        <ErrorPanel
          error={error}
          onRetry={() => setAttempt((n) => n + 1)}
          onBack={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  if (!data) {
    return (
      <div className="dashboard-page loading">
        <div className="login-spinner" />
        <p>Chargement du tableau de bord...</p>
      </div>
    );
  }

  const { overview } = data;
  const kpis = [
    { label: "Simulations", value: String(overview.simulations_total), suffix: "", hint: "formations lancées" },
    { label: "Taux de réussite", value: `${overview.success_rate}`, suffix: "%", hint: "score ≥ 70/100" },
    { label: "Satisfaction", value: `${overview.average_satisfaction}`, suffix: "/5", hint: "note moyenne" },
    { label: "Durée", value: formatDuration(overview.average_duration_minutes), suffix: "", hint: "par simulation" },
  ];

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">Pilot Success Center</p>
          <h1>Tableau de bord pilotage</h1>
        </div>
        <div className="dashboard-actions">
          <button className="btn-secondary" onClick={() => navigate("/scenarios")} type="button">
            ← Scénarios
          </button>
        </div>
      </header>

      <div className="cockpit-layout">
        <div className="cockpit-main">
          {/* KPI cards */}
          <div className="metric-grid">
            {kpis.map((kpi) => (
              <div className="metric-card" key={kpi.label}>
                <span className="metric-value">
                  {kpi.value}<span className="metric-suffix">{kpi.suffix}</span>
                </span>
                <span className="metric-label">{kpi.label}</span>
                <span className="metric-hint">{kpi.hint}</span>
              </div>
            ))}
          </div>

          {/* Funnel */}
          <section className="dashboard-card">
            <h2>Parcours d'adoption</h2>
            <p className="subtitle">Du premier lancement au retour des apprenants</p>
            <div className="funnel">
              {data.funnel.map((stage) => (
                <div className="funnel-stage" key={stage.id}>
                  <div className="funnel-head">
                    <span className="funnel-label">{stage.label}</span>
                    <span className="funnel-value">{stage.percentage}%</span>
                    <span className="funnel-count">{stage.count}</span>
                  </div>
                  <div className="funnel-track">
                    <div
                      className="funnel-fill"
                      style={{ width: `${Math.min(stage.percentage, 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        <div className="cockpit-side">
          {/* Alerts */}
          <section className="dashboard-card">
            <h2>Alertes</h2>
            {data.alerts.length === 0 ? (
              <p className="empty-hint">Aucune alerte.</p>
            ) : (
              <div className="alerts">
                {data.alerts.map((alert, i) => (
                  <div className={`alert-card alert-${alert.level}`} key={i}>
                    <span className="alert-icon">{alert.level === "warning" ? "⚠" : "✓"}</span>
                    <div className="alert-body">
                      <strong>{alert.title}</strong>
                      <p>{alert.message}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* Recent activity */}
          <section className="dashboard-card">
            <h2>Activité récente</h2>
            {data.recent_activity.length === 0 ? (
              <p className="empty-hint">Aucune activité pour l'instant.</p>
            ) : (
              <ul className="activity-list">
                {data.recent_activity.map((item, i) => (
                  <li className="activity-item" key={`${item.timestamp}-${i}`}>
                    <span className="activity-time">{formatTimestamp(item.timestamp)}</span>
                    <div className="activity-body">
                      <span className="activity-title">{item.action}</span>
                      {item.detail && <span className="activity-detail">{item.detail}</span>}
                      <span className="activity-actor">{formatActor(item.actor)}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
