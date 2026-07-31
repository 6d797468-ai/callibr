import type { SessionSummaryItem } from "../lib/types";

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

type Props = {
  sessions: SessionSummaryItem[];
  onOpen: (session: SessionSummaryItem) => void;
  actionLabel?: (session: SessionSummaryItem) => string;
};

export default function SessionList({ sessions, onOpen, actionLabel }: Props) {
  return (
    <div className="collection-list">
      {sessions.map((s) => (
        <button
          className="collection-row"
          key={s.session_id}
          onClick={() => onOpen(s)}
          type="button"
        >
          <div className="collection-row-main">
            <div className="collection-row-title">{s.scenario_title}</div>
            <div className="collection-row-detail">
              {s.domain_pack} · {formatDate(s.started_at)}
            </div>
          </div>
          <div className="collection-row-meta">
            <span className={`status-badge ${s.status}`}>
              {s.status === "completed" ? "Terminée" : "En cours"}
            </span>
            {s.score !== null && (
              <span className="score-pill">
                {s.score}/{s.max_score}
              </span>
            )}
            <span className="collection-row-action">
              {actionLabel ? actionLabel(s) : "Ouvrir →"}
            </span>
          </div>
        </button>
      ))}
    </div>
  );
}
