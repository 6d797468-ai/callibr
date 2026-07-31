import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../lib/api";
import type { SessionSummaryItem } from "../lib/types";
import ErrorPanel from "../components/ErrorPanel";
import EmptyState from "../components/EmptyState";
import SessionList from "../components/SessionList";
import { friendlyError, type UserFacingError } from "../lib/errors";

type Props = {
  token: string | null;
};

export default function SessionsListPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [sessions, setSessions] = useState<SessionSummaryItem[] | null>(null);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!bearer) {
      navigate("/");
      return;
    }
    setError(null);
    api
      .listSessions(bearer)
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
        <p>Chargement de vos simulations...</p>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="collection-page">
        <header className="collection-header">
          <p className="eyebrow">Simulations</p>
          <h1>Mes simulations</h1>
          <p className="subtitle">Retrouvez ici toutes les sessions que vous avez lancées</p>
        </header>
        <EmptyState
          icon="🎬"
          title="Aucune simulation"
          description="Vous n'avez pas encore lancé de simulation. Commencez par une mise en situation : votre session apparaîtra ici."
          actionLabel="Commencer une simulation"
          onAction={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  return (
    <div className="collection-page">
      <header className="collection-header">
        <p className="eyebrow">Simulations</p>
        <h1>Mes simulations</h1>
        <p className="subtitle">Retrouvez ici toutes les sessions que vous avez lancées</p>
      </header>
      <SessionList
        sessions={sessions}
        onOpen={(s) =>
          navigate(s.status === "completed" ? `/report?session=${s.session_id}` : `/simulation?scenario=${s.scenario_id}`)
        }
        actionLabel={(s) => (s.status === "completed" ? "Voir le rapport →" : "Relancer →")}
      />
    </div>
  );
}
