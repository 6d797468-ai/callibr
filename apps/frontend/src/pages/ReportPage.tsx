import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import * as api from "../lib/api";
import type { SessionReport } from "../lib/types";

type Props = {
  token: string | null;
};

export default function ReportPage({ token }: Props) {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const sessionId = params.get("session") ?? "";
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [report, setReport] = useState<SessionReport | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!sessionId) {
      navigate("/scenarios");
      return;
    }
    if (!bearer) {
      navigate("/");
      return;
    }
    api
      .getSessionReport(sessionId, bearer)
      .then(setReport)
      .catch((err) => setError(err.message));
  }, [sessionId, bearer, navigate]);

  if (error) {
    return (
      <div className="report-page error">
        <p>{error}</p>
        <button onClick={() => navigate("/scenarios")} type="button">
          Retour aux scénarios
        </button>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="report-page loading">
        <div className="login-spinner" />
        <p>Génération du rapport...</p>
      </div>
    );
  }

  const pct = Math.round((report.final_score / report.max_score) * 100);
  const grade =
    pct >= 80 ? "Excellent" : pct >= 60 ? "Bon" : pct >= 40 ? "Moyen" : "À améliorer";

  return (
    <div className="report-page">
      <header className="report-header">
        <div>
          <p className="eyebrow">Rapport de simulation</p>
          <h1>{report.scenario.title}</h1>
          <p className="subtitle">
            {report.scenario.domain_pack} &mdash;{" "}
            {Math.round(report.duration_seconds / 60)} min &mdash;{" "}
            {report.message_count} messages
          </p>
        </div>
        <button
          className="btn-secondary"
          onClick={() => navigate("/scenarios")}
          type="button"
        >
          ← Scénarios
        </button>
      </header>

      <div className="report-summary">
        <div className="report-score-ring">
          <span className="report-score-value">{pct}</span>
          <span className="report-score-label">/100</span>
        </div>
        <div className="report-score-info">
          <p className="report-grade">{grade}</p>
          <p className="report-detail">
            Score final : {report.final_score}/{report.max_score}
          </p>
        </div>
      </div>

      <section className="report-criteria">
        <h2>Critères d'évaluation</h2>
        <div className="criteria-table">
          {report.criteria.map((c) => (
            <div className={`cr-row ${c.status}`} key={c.criterion_id}>
              <div className="cr-label">{c.label}</div>
              <div className="cr-score">
                {Math.round((c.score / c.max_score) * 100)}%
              </div>
              <div className="cr-bar">
                <div
                  className="cr-bar-fill"
                  style={{
                    width: `${(c.score / c.max_score) * 100}%`,
                  }}
                />
              </div>
              <div className="cr-feedback">{c.feedback}</div>
            </div>
          ))}
        </div>
      </section>

      {report.strengths.length > 0 && (
        <section className="report-section">
          <h2>Points forts</h2>
          <ul className="report-list check">
            {report.strengths.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </section>
      )}

      {report.risks.length > 0 && (
        <section className="report-section">
          <h2>Points de vigilance</h2>
          <ul className="report-list warn">
            {report.risks.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </section>
      )}

      {report.next_best_actions.length > 0 && (
        <section className="report-section">
          <h2>Prochaines étapes</h2>
          <ul className="report-list next">
            {report.next_best_actions.map((a, i) => (
              <li key={i}>{a}</li>
            ))}
          </ul>
        </section>
      )}

      {report.crm_actions && report.crm_actions.length > 0 && (
        <section className="report-section">
          <h2>Actions CRM réalisées</h2>
          <ul className="report-list crm">
            {report.crm_actions.map((a) => (
              <li key={a.execution_id}>
                {a.label} &mdash;{" "}
                <span className={a.status}>{a.status}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="report-actions">
        <button
          className="btn-secondary"
          onClick={() => navigate(`/replay?session=${sessionId}`)}
          type="button"
        >
          Revoir la simulation
        </button>
        <button
          className="btn-primary"
          onClick={() => navigate(`/feedback?session=${sessionId}`)}
          type="button"
        >
          Donner mon avis sur la simulation
        </button>
      </div>
    </div>
  );
}
