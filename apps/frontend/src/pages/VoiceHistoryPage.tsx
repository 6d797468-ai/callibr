import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../lib/api";
import type { VoiceSessionSummary } from "../lib/types";
import ErrorPanel from "../components/ErrorPanel";
import EmptyState from "../components/EmptyState";
import { friendlyError, type UserFacingError } from "../lib/errors";

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

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${Math.round(seconds)} s`;
  return `${Math.round(seconds / 60)} min`;
}

const STATE_LABELS: Record<string, string> = {
  idle: "En attente",
  listening: "À l'écoute",
  processing: "Traitement",
  speaking: "Réponse",
  interrupted: "Interrompue",
  paused: "En pause",
  ended: "Terminée",
};

type Props = {
  token: string | null;
};

export default function VoiceHistoryPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [sessions, setSessions] = useState<VoiceSessionSummary[] | null>(null);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!bearer) {
      navigate("/");
      return;
    }
    setError(null);
    api
      .listVoiceSessions(bearer)
      .then(setSessions)
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

  if (!sessions) {
    return (
      <div className="collection-page loading">
        <div className="login-spinner" />
        <p>Chargement de l'historique vocal...</p>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="collection-page">
        <header className="collection-header">
          <p className="eyebrow">Voix</p>
          <h1>Historique vocal</h1>
          <p className="subtitle">Vos conversations vocales passées</p>
        </header>
        <EmptyState
          icon="🎙️"
          title="Aucune conversation vocale"
          description="Le mode vocal vous permet de vous entraîner à l'oral. Lancez une simulation puis activez le mode vocal pour démarrer une conversation."
          actionLabel="Lancer une simulation vocale"
          onAction={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  return (
    <div className="collection-page">
      <header className="collection-header">
        <p className="eyebrow">Voix</p>
        <h1>Historique vocal</h1>
        <p className="subtitle">Vos conversations vocales passées</p>
      </header>
      <div className="collection-list">
        {[...sessions].reverse().map((s) => (
          <button
            className="collection-row"
            key={s.session_id}
            onClick={() =>
              s.simulation_session_id
                ? navigate(`/report?session=${s.simulation_session_id}`)
                : navigate("/scenarios")
            }
            type="button"
          >
            <div className="collection-row-main">
              <div className="collection-row-title">Session vocale</div>
              <div className="collection-row-detail">
                {formatTime(s.started_at)} · Écoute {formatDuration(s.total_listen_duration)} · Parole {formatDuration(s.total_speak_duration)}
              </div>
            </div>
            <div className="collection-row-meta">
              <span className={`status-badge ${s.state === "ended" ? "ended" : "active"}`}>
                {STATE_LABELS[s.state] ?? s.state}
              </span>
              <span className="collection-row-action">
                {s.simulation_session_id ? "Voir le rapport →" : "→"}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
