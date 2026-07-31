import type { UserFacingError } from "../lib/errors";

type Props = {
  error: UserFacingError;
  onRetry?: () => void;
  onBack?: () => void;
  retryLabel?: string;
};

export default function ErrorPanel({
  error,
  onRetry,
  onBack,
  retryLabel = "Réessayer",
}: Props) {
  return (
    <div className="error-panel" role="alert">
      <h3 className="error-panel-title">{error.title}</h3>
      <p className="error-panel-explanation">{error.explanation}</p>
      <p className="error-panel-action">{error.action}</p>
      <div className="error-panel-actions">
        {onRetry && (
          <button className="btn-primary" onClick={onRetry} type="button">
            {retryLabel}
          </button>
        )}
        {onBack && (
          <button className="btn-secondary" onClick={onBack} type="button">
            Retour
          </button>
        )}
      </div>
    </div>
  );
}
