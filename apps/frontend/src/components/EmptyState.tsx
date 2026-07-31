type Props = {
  icon?: string;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  secondaryLabel?: string;
  onSecondary?: () => void;
};

export default function EmptyState({
  icon = "📄",
  title,
  description,
  actionLabel,
  onAction,
  secondaryLabel,
  onSecondary,
}: Props) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon" aria-hidden="true">
        {icon}
      </div>
      <h2 className="empty-state-title">{title}</h2>
      <p className="empty-state-description">{description}</p>
      {actionLabel && onAction && (
        <button className="btn-primary" onClick={onAction} type="button">
          {actionLabel}
        </button>
      )}
      {secondaryLabel && onSecondary && (
        <button
          className="empty-state-secondary"
          onClick={onSecondary}
          type="button"
        >
          {secondaryLabel}
        </button>
      )}
    </div>
  );
}
