import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../lib/api";
import type { FeedbackRecord } from "../lib/types";
import ErrorPanel from "../components/ErrorPanel";
import EmptyState from "../components/EmptyState";
import { friendlyError, type UserFacingError } from "../lib/errors";

function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function StarRow({ value }: { value: number }) {
  return (
    <span className="star-row" aria-label={`${value} sur 5`}>
      {[1, 2, 3, 4, 5].map((s) => (
        <span className={`star-mini ${s <= value ? "star-filled" : "star-empty"}`} key={s}>
          ★
        </span>
      ))}
    </span>
  );
}

type Props = {
  token: string | null;
};

export default function FeedbackListPage({ token }: Props) {
  const navigate = useNavigate();
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [feedback, setFeedback] = useState<FeedbackRecord[] | null>(null);
  const [error, setError] = useState<UserFacingError | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!bearer) {
      navigate("/");
      return;
    }
    setError(null);
    api
      .listFeedback(bearer)
      .then(setFeedback)
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

  if (!feedback) {
    return (
      <div className="collection-page loading">
        <div className="login-spinner" />
        <p>Chargement des avis...</p>
      </div>
    );
  }

  if (feedback.length === 0) {
    return (
      <div className="collection-page">
        <header className="collection-header">
          <p className="eyebrow">Avis</p>
          <h1>Mes avis</h1>
          <p className="subtitle">Vos retours sur les simulations terminées</p>
        </header>
        <EmptyState
          icon="💬"
          title="Aucun avis"
          description="Vous n'avez pas encore donné votre avis. Terminez une simulation puis partagez votre retour pour l'améliorer."
          actionLabel="Voir le dernier rapport"
          onAction={() => navigate("/reports")}
        />
      </div>
    );
  }

  return (
    <div className="collection-page">
      <header className="collection-header">
        <p className="eyebrow">Avis</p>
        <h1>Mes avis</h1>
        <p className="subtitle">Vos retours sur les simulations terminées</p>
      </header>
      <div className="collection-list">
        {feedback.map((f) => (
          <button
            className="collection-row"
            key={f.session_id}
            onClick={() => navigate(`/report?session=${f.session_id}`)}
            type="button"
          >
            <div className="collection-row-main">
              <div className="collection-row-title">
                <StarRow value={f.satisfaction} />
              </div>
              <div className="collection-row-detail">
                {formatDate(f.submitted_at)} · Recommanderait :{" "}
                {f.would_use_for_training === "yes"
                  ? "Oui"
                  : f.would_use_for_training === "maybe"
                    ? "Peut-être"
                    : "Non"}
              </div>
              {f.free_text && (
                <div className="collection-row-detail">{f.free_text}</div>
              )}
            </div>
            <span className="collection-row-action">Voir le rapport →</span>
          </button>
        ))}
      </div>
    </div>
  );
}
