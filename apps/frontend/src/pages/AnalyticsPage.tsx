import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../lib/api";
import type { ProductEventRecord } from "../lib/types";
import ErrorPanel from "../components/ErrorPanel";
import EmptyState from "../components/EmptyState";
import { friendlyError, type UserFacingError } from "../lib/errors";

const EVENT_LABELS: Record<string, string> = {
  ApplicationOpened: "Application ouverte",
  LoginSucceeded: "Connexion réussie",
  ScenarioViewed: "Scénario consulté",
  ScenarioStarted: "Simulation lancée",
  FirstMessageSent: "Premier message envoyé",
  ConversationCompleted: "Simulation terminée",
  WizardCompleted: "Wizard terminé",
  ProcedureCompleted: "Procédure terminée",
  ReportViewed: "Rapport consulté",
  ReportExported: "Rapport exporté",
  SessionResumed: "Session reprise",
  SessionAbandoned: "Session abandonnée",
  FeedbackSubmitted: "Feedback envoyé",
};

function formatTime(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

type Props = {
  token: string | null;
};

export default function AnalyticsPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [events, setEvents] = useState<ProductEventRecord[] | null>(null);
  const [counts, setCounts] = useState<Record<string, number> | null>(null);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!bearer) {
      navigate("/");
      return;
    }
    setError(null);
    Promise.all([api.listProductEvents(bearer), api.getProductEventCounts(bearer)])
      .then(([evts, cts]) => {
        setEvents(evts);
        setCounts(cts);
      })
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

  if (!events || !counts) {
    return (
      <div className="collection-page loading">
        <div className="login-spinner" />
        <p>Chargement des données d'activité...</p>
      </div>
    );
  }

  const total = Object.values(counts).reduce((a, b) => a + b, 0);

  if (total === 0) {
    return (
      <div className="collection-page">
        <header className="collection-header">
          <p className="eyebrow">Analytics</p>
          <h1>Activité</h1>
          <p className="subtitle">Les événements de votre parcours d'apprentissage</p>
        </header>
        <EmptyState
          icon="📈"
          title="Aucun événement"
          description="Votre activité apparaîtra ici dès que vous utiliserez la plateforme : lancement d'une simulation, rapport consulté, avis envoyé…"
          actionLabel="Découvrir le tableau de bord"
          onAction={() => navigate("/dashboard")}
        />
      </div>
    );
  }

  const sortedCounts = Object.entries(counts)
    .sort((a, b) => b[1] - a[1]);

  return (
    <div className="collection-page">
      <header className="collection-header">
        <p className="eyebrow">Analytics</p>
        <h1>Activité</h1>
        <p className="subtitle">Les événements de votre parcours d'apprentissage</p>
      </header>
      <div className="analytics-layout">
        <section className="analytics-card">
          <h2>Répartition par type d'événement</h2>
          <ul>
            {sortedCounts.map(([type, count]) => (
              <li key={type}>
                <span>{EVENT_LABELS[type] ?? type}</span>
                <span className="analytics-count">{count}</span>
              </li>
            ))}
          </ul>
        </section>
        <section className="analytics-card">
          <h2>Derniers événements</h2>
          <div>
            {events.slice(0, 20).map((e, i) => (
              <div className="event-row" key={`${e.timestamp}-${i}`}>
                <span className="event-type">{EVENT_LABELS[e.event_type] ?? e.event_type}</span>
                <span className="event-detail">
                  {e.scenario_id || e.session_id || "—"}
                </span>
                <span className="event-time">{formatTime(e.timestamp)}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
