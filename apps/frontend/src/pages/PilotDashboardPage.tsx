import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";

type DashboardData = {
  overview: {
    simulations_started: number;
    simulations_completed: number;
    completion_rate: number;
    average_duration_seconds: number;
    active_users: number;
    total_sessions: number;
  };
  performance: {
    average_score: number;
    score_trend: { label: string; value: number }[];
    weakest_criteria: { label: string; average: number }[];
    strongest_criteria: { label: string; average: number }[];
  };
  product: {
    average_satisfaction: number;
    would_use_counts: Record<string, number>;
    abandon_count: number;
    average_time_before_abandon: number;
    replay_count: number;
  };
  business: {
    scenario_ranking: {
      scenario_id: string;
      title: string;
      average_score: number;
      count: number;
    }[];
    difficulty_distribution: Record<string, number>;
    average_duration_by_scenario: Record<string, number>;
    satisfaction_by_scenario: Record<string, number>;
  };
};

type ReadinessResult = {
  score: number;
  status: "READY" | "ALMOST_READY" | "NOT_READY";
  dimensions: {
    adoption: number;
    completion: number;
    feedback: number;
    stability: number;
    analytics: number;
  };
};

type Props = {
  token: string | null;
};

function Gauge({ value, label, color }: { value: number; label: string; color: string }) {
  const pct = Math.min(value, 100);
  return (
    <div className="gauge">
      <svg viewBox="0 0 120 120" className="gauge-svg">
        <circle cx="60" cy="60" r="52" fill="none" stroke="#eef2f5" strokeWidth="10" />
        <circle
          cx="60" cy="60" r="52"
          fill="none" stroke={color}
          strokeWidth="10"
          strokeDasharray={`${(pct / 100) * 327} 327`}
          strokeLinecap="round"
          transform="rotate(-90 60 60)"
        />
        <text x="60" y="55" textAnchor="middle" fontSize="24" fontWeight="800" fill="#172026">
          {pct}
        </text>
        <text x="60" y="75" textAnchor="middle" fontSize="10" fill="#526879">
          /100
        </text>
      </svg>
      <span className="gauge-label">{label}</span>
    </div>
  );
}

function ScoreRing({ value }: { value: number }) {
  const pct = Math.min(Math.round(value), 100);
  return (
    <div className="score-ring-lg">
      <span className="score-ring-value">{pct}</span>
      <span className="score-ring-max">/100</span>
    </div>
  );
}

export default function PilotDashboardPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [data, setData] = useState<DashboardData | null>(null);
  const [readiness, setReadiness] = useState<ReadinessResult | null>(null);
  const [error, setError] = useState("");
  const [tab, setTab] = useState("overview");
  const iframeRef = useRef<HTMLIFrameElement>(null);

  function downloadReport() {
    const apiBase = import.meta.env.VITE_CALLIBR_API_BASE_URL ?? "http://localhost:8000";
    const url = `${apiBase}/api/v1/pilot/report/export`;
    // Use iframe trick for download with auth headers
    const iframe = iframeRef.current;
    if (!iframe) return;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.setRequestHeader("Authorization", `Bearer ${bearer}`);
    xhr.setRequestHeader("X-Tenant-Id", "tenant_demo");
    xhr.setRequestHeader("X-User-Id", "learner_demo");
    xhr.responseType = "blob";
    xhr.onload = () => {
      if (xhr.status === 200) {
        const blob = xhr.response;
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `callibr-executive-report-${new Date().toISOString().slice(0, 10)}.pdf`;
        a.click();
        URL.revokeObjectURL(a.href);
      }
    };
    xhr.send();
  }

  useEffect(() => {
    if (!bearer) { navigate("/"); return; }
    Promise.all([
      apiFetch<DashboardData>("/api/v1/pilot/dashboard", bearer),
      apiFetch<ReadinessResult>("/api/v1/pilot/readiness", bearer),
    ])
      .then(([d, r]) => { setData(d); setReadiness(r); })
      .catch((err) => setError(err.message));
  }, [bearer, navigate]);

  if (error) {
    return (
      <div className="dashboard-page error">
        <p>{error}</p>
        <button className="btn-primary" onClick={() => navigate("/scenarios")} type="button">
          Retour
        </button>
      </div>
    );
  }

  if (!data || !readiness) {
    return (
      <div className="dashboard-page loading">
        <div className="login-spinner" />
        <p>Chargement du tableau de bord...</p>
      </div>
    );
  }

  const readinessLabel = readiness.status === "READY" ? "Prêt" : readiness.status === "ALMOST_READY" ? "Presque prêt" : "Pas encore prêt";
  const readinessColor = readiness.status === "READY" ? "#2f7d57" : readiness.status === "ALMOST_READY" ? "#e65100" : "#c62828";

  return (
    <div className="dashboard-page">
      <iframe ref={iframeRef} style={{ display: "none" }} title="download-helper" />
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">Pilot Success Center</p>
          <h1>Callibr — Release 0.1</h1>
        </div>
        <div className="dashboard-actions">
          <button className="btn-primary" onClick={downloadReport} type="button">
            Télécharger le rapport
          </button>
          <button className="btn-secondary" onClick={() => navigate("/scenarios")} type="button">
            ← Scénarios
          </button>
        </div>
      </header>

      {/* Readiness bar */}
      <div className="readiness-bar">
        <div className="readiness-info">
          <span className="readiness-label">Pilot Readiness</span>
          <span className="readiness-score" style={{ color: readinessColor }}>{readiness.score}%</span>
          <span className={`readiness-status status-${readiness.status.toLowerCase()}`}>
            {readinessLabel}
          </span>
        </div>
        <div className="readiness-track">
          <div className="readiness-fill" style={{ width: `${readiness.score}%`, background: readinessColor }} />
        </div>
      </div>

      {/* Navigation tabs */}
      <nav className="dashboard-tabs">
        {(["overview", "performance", "product", "business"] as const).map((t) => (
          <button
            key={t}
            className={`tab ${tab === t ? "tab-active" : ""}`}
            onClick={() => setTab(t)}
            type="button"
          >
            {t === "overview" ? "Vue d'ensemble" : t === "performance" ? "Performance" : t === "product" ? "Produit" : "Métier"}
          </button>
        ))}
      </nav>

      {/* Tab: Overview */}
      {tab === "overview" && (
        <div className="dashboard-section">
          <div className="metric-grid">
            <div className="metric-card">
              <span className="metric-value">{data.overview.simulations_started}</span>
              <span className="metric-label">Simulations lancées</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{data.overview.simulations_completed}</span>
              <span className="metric-label">Terminées</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{data.overview.completion_rate}%</span>
              <span className="metric-label">Taux de complétion</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{Math.round(data.overview.average_duration_seconds / 60)}m</span>
              <span className="metric-label">Durée moyenne</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{data.overview.active_users}</span>
              <span className="metric-label">Utilisateurs actifs</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{data.overview.total_sessions}</span>
              <span className="metric-label">Sessions totales</span>
            </div>
          </div>

          {data.business.scenario_ranking.length > 0 && (
            <section className="dashboard-card">
              <h2>Classement des scénarios</h2>
              <table className="ranking-table">
                <thead>
                  <tr><th>Scénario</th><th>Score moyen</th><th>Simulations</th></tr>
                </thead>
                <tbody>
                  {data.business.scenario_ranking.map((s) => (
                    <tr key={s.scenario_id}>
                      <td>{s.title}</td>
                      <td><strong>{s.average_score}</strong></td>
                      <td>{s.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}
        </div>
      )}

      {/* Tab: Performance */}
      {tab === "performance" && (
        <div className="dashboard-section">
          <div className="dashboard-card score-card">
            <ScoreRing value={data.performance.average_score} />
            <div>
              <h2>Score moyen : {data.performance.average_score}/100</h2>
              <p className="subtitle">Moyenne sur {data.overview.simulations_completed} simulation(s) terminée(s)</p>
            </div>
          </div>

          <div className="criteria-columns">
            {data.performance.weakest_criteria.length > 0 && (
              <div className="dashboard-card">
                <h2>Points faibles</h2>
                <ul className="criteria-list weak">
                  {data.performance.weakest_criteria.map((c) => (
                    <li key={c.label}>
                      <span className="cl-label">{c.label}</span>
                      <span className="cl-value">{c.average}%</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {data.performance.strongest_criteria.length > 0 && (
              <div className="dashboard-card">
                <h2>Points forts</h2>
                <ul className="criteria-list strong">
                  {data.performance.strongest_criteria.map((c) => (
                    <li key={c.label}>
                      <span className="cl-label">{c.label}</span>
                      <span className="cl-value">{c.average}%</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div className="readiness-gauges">
            <Gauge value={readiness.dimensions.adoption} label="Adoption" color="#245b78" />
            <Gauge value={readiness.dimensions.completion} label="Complétion" color="#2f7d57" />
            <Gauge value={readiness.dimensions.feedback} label="Feedback" color="#f4b836" />
            <Gauge value={readiness.dimensions.stability} label="Stabilité" color="#7b61ff" />
            <Gauge value={readiness.dimensions.analytics} label="Analytics" color="#e65100" />
          </div>
        </div>
      )}

      {/* Tab: Product */}
      {tab === "product" && (
        <div className="dashboard-section">
          <div className="metric-grid">
            <div className="metric-card">
              <span className="metric-value">{data.product.average_satisfaction}/5</span>
              <span className="metric-label">Satisfaction moyenne</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{data.product.abandon_count}</span>
              <span className="metric-label">Abandons</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">{data.product.replay_count}</span>
              <span className="metric-label">Replays consultés</span>
            </div>
          </div>

          <div className="dashboard-card">
            <h2>Recommanderait la simulation à son équipe</h2>
            <div className="would-use-bars">
              {(["yes", "maybe", "no"] as const).map((k) => {
                const total = Object.values(data.product.would_use_counts).reduce((a, b) => a + b, 0) || 1;
                const pct = Math.round((data.product.would_use_counts[k] || 0) / total * 100);
                const label = k === "yes" ? "Oui" : k === "maybe" ? "Peut-être" : "Non";
                const color = k === "yes" ? "#2f7d57" : k === "maybe" ? "#e65100" : "#c62828";
                return (
                  <div className="would-use-row" key={k}>
                    <span className="wur-label">{label}</span>
                    <div className="wur-track">
                      <div className="wur-fill" style={{ width: `${pct}%`, background: color }} />
                    </div>
                    <span className="wur-value">{data.product.would_use_counts[k] || 0}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Tab: Business */}
      {tab === "business" && (
        <div className="dashboard-section">
          {data.business.scenario_ranking.length > 0 ? (
            <div className="dashboard-card">
              <h2>Classement des scénarios</h2>
              <table className="ranking-table">
                <thead>
                  <tr><th>#</th><th>Scénario</th><th>Score moyen</th><th>Simulations</th></tr>
                </thead>
                <tbody>
                  {data.business.scenario_ranking.map((s, i) => (
                    <tr key={s.scenario_id}>
                      <td className="rank-num">{i + 1}</td>
                      <td>{s.title}</td>
                      <td><strong>{s.average_score}</strong></td>
                      <td>{s.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="dashboard-card empty">
              <p>Aucune donnée scénario disponible pour le moment.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
