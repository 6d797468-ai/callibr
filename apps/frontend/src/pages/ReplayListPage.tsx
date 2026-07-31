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

export default function ReplayListPage({ token }: Props) {
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
        <p>Chargement des replays...</p>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="collection-page">
        <header className="collection-header">
          <p className="eyebrow">Replay</p>
          <h1>Revoir une simulation</h1>
          <p className="subtitle">Rejouez le déroulé d'une de vos sessions</p>
        </header>
        <EmptyState
          icon="🎞️"
          title="Aucun replay disponible"
          description="Vous n'avez pas encore de simulation à revoir. Lancez-en une pour pouvoir rejouer la conversation plus tard."
          actionLabel="Ouvrir une simulation"
          onAction={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  return (
    <div className="collection-page">
      <header className="collection-header">
        <p className="eyebrow">Replay</p>
        <h1>Revoir une simulation</h1>
        <p className="subtitle">Rejouez le déroulé d'une de vos sessions</p>
      </header>
      <SessionList
        sessions={sessions}
        onOpen={(s) => navigate(`/replay/session?session=${s.session_id}`)}
        actionLabel={() => "Revoir →"}
      />
    </div>
  );
}
