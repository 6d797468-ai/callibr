import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../lib/api";
import type { ReportSummaryItem } from "../lib/types";
import ErrorPanel from "../components/ErrorPanel";
import EmptyState from "../components/EmptyState";
import { friendlyError, type UserFacingError } from "../lib/errors";

function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

type Props = {
  token: string | null;
};

export default function ReportsListPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [reports, setReports] = useState<ReportSummaryItem[] | null>(null);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!bearer) {
      navigate("/");
      return;
    }
    setError(null);
    api
      .listReports(bearer)
      .then(setReports)
      .catch((err) => setError(friendlyError(err)));
  }, [bearer, navigate, attempt]);

  if (error) {
    return (
      <div className="collection-page error">
        <ErrorPanel
          error={error}
          onRetry={() => setAttempt((n) => n + 1)}
          onBack={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  if (!reports) {
    return (
      <div className="collection-page loading">
        <div className="login-spinner" />
        <p>Chargement de vos rapports...</p>
      </div>
    );
  }

  if (reports.length === 0) {
    return (
      <div className="collection-page">
        <header className="collection-header">
          <p className="eyebrow">Rapports</p>
          <h1>Mes rapports</h1>
          <p className="subtitle">Les rapports d'évaluation de vos simulations terminées</p>
        </header>
        <EmptyState
          icon="📊"
          title="Aucun rapport"
          description="Vous n'avez pas encore de rapport. Terminez une simulation pour obtenir un rapport d'évaluation détaillé."
          actionLabel="Lancer une première simulation"
          onAction={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  return (
    <div className="collection-page">
      <header className="collection-header">
        <p className="eyebrow">Rapports</p>
        <h1>Mes rapports</h1>
        <p className="subtitle">Les rapports d'évaluation de vos simulations terminées</p>
      </header>
      <div className="collection-list">
        {reports.map((r) => (
          <button
            className="collection-row"
            key={r.session_id}
            onClick={() => navigate(`/report?session=${r.session_id}`)}
            type="button"
          >
            <div className="collection-row-main">
              <div className="collection-row-title">{r.scenario_title}</div>
              <div className="collection-row-detail">
                {r.domain_pack} · {formatDate(r.completed_at ?? r.started_at)} · {r.duration_minutes} min
              </div>
            </div>
            <div className="collection-row-meta">
              <span className="score-pill">
                {r.score}/{r.max_score}
              </span>
              <span className="collection-row-action">Voir le rapport →</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
