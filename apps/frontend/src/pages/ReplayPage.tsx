import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { apiFetch } from "../lib/api";
import ErrorPanel from "../components/ErrorPanel";
import { friendlyError, type UserFacingError } from "../lib/errors";

type ReplayTurn = {
  turn_index: number;
  learner_message: string;
  customer_message: string;
};

type SessionReplay = {
  session_id: string;
  scenario: { title: string; domain_pack: string };
  started_at: string;
  completed_at: string | null;
  status: string;
  turns: ReplayTurn[];
};

type Props = {
  token: string | null;
};

export default function ReplayPage({ token }: Props) {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const sessionId = params.get("session") ?? "";
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [replay, setReplay] = useState<SessionReplay | null>(null);
  const [currentTurn, setCurrentTurn] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!sessionId || !bearer) {
      navigate("/scenarios");
      return;
    }
    setError(null);
    apiFetch<SessionReplay>(
      `/api/v1/simulations/${sessionId}/replay`,
      bearer,
    )
      .then(setReplay)
      .catch((err) => setError(friendlyError(err)));
  }, [sessionId, bearer, navigate, attempt]);

  if (error) {
    return (
      <div className="replay-page error">
        <ErrorPanel
          error={error}
          onRetry={() => setAttempt((n) => n + 1)}
          onBack={() => navigate("/scenarios")}
        />
      </div>
    );
  }

  if (!replay) {
    return (
      <div className="replay-page loading">
        <div className="login-spinner" />
      </div>
    );
  }

  const turn = replay.turns[currentTurn];
  if (!turn) {
    return (
      <div className="replay-page done">
        <div className="replay-card">
          <h2>Replay terminé</h2>
          <p>La simulation a {replay.turns.length} échanges.</p>
          <button
            className="btn-primary"
            onClick={() => navigate(`/report?session=${sessionId}`)}
            type="button"
          >
            Voir le rapport →
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="replay-page">
      <div className="replay-header">
        <div>
          <p className="eyebrow">Replay</p>
          <h1>{replay.scenario.title}</h1>
          <p className="subtitle">
            {replay.scenario.domain_pack} &mdash; Échange {currentTurn + 1}/{replay.turns.length}
          </p>
        </div>
        <button
          className="btn-secondary"
          onClick={() => navigate("/scenarios")}
          type="button"
        >
          ← Scénarios
        </button>
      </div>

      <div className="replay-turns">
        <div className="replay-turn">
          <div className="chat-bubble learner">
            <span className="chat-role">Apprenant</span>
            <p>{turn.learner_message}</p>
          </div>
          <div className="chat-bubble customer">
            <span className="chat-role">Client</span>
            <p>{turn.customer_message}</p>
          </div>
        </div>
      </div>

      <div className="replay-controls">
        <button
          className="btn-secondary"
          disabled={currentTurn === 0}
          onClick={() => { setCurrentTurn((i) => i - 1); setPlaying(false); }}
          type="button"
        >
          ← Précédent
        </button>

        <button
          className={`btn-primary ${playing ? "btn-active" : ""}`}
          onClick={() => setPlaying(true)}
          type="button"
        >
          {playing ? "▶ Auto" : "▶ Auto"}
        </button>

        <button
          className="btn-primary"
          disabled={currentTurn === replay.turns.length - 1}
          onClick={() => { setCurrentTurn((i) => i + 1); setPlaying(false); }}
          type="button"
        >
          Suivant →
        </button>
      </div>
    </div>
  );
}
