import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import type { ScenarioSummary } from "../lib/types";
import EmptyState from "../components/EmptyState";
import { trackScenarioViewed } from "../lib/analytics";

type Props = {
  scenarios: ScenarioSummary[];
  token: string;
};

const DIFFICULTY_LABEL: Record<string, string> = {
  foundation: "Facile",
  intermediate: "Intermédiaire",
  advanced: "Avancé",
};

const DIFFICULTY_CLASS: Record<string, string> = {
  foundation: "diff-easy",
  intermediate: "diff-mid",
  advanced: "diff-hard",
};

export default function ScenarioListPage({ scenarios, token }: Props) {
  const navigate = useNavigate();

  useEffect(() => {
    trackScenarioViewed();
  }, []);

  function start(scenarioId: string) {
    navigate(`/simulation?scenario=${scenarioId}`);
  }

  return (
    <div className="scenario-list-page">
      <header className="scenario-list-header">
        <h1>Choisissez un scénario</h1>
        <p className="subtitle">
          Entraînez-vous sur une mise en situation réaliste
        </p>
      </header>

      {scenarios.length === 0 ? (
        <EmptyState
          icon="🗂️"
          title="Aucun scénario disponible"
          description="Le catalogue de scénarios est vide pour le moment. Revenez un peu plus tard : de nouvelles mises en situation seront bientôt disponibles."
          actionLabel="Actualiser"
          onAction={() => window.location.reload()}
        />
      ) : (
        <div className="scenario-grid">
          {scenarios.map((s) => (
            <button
              className="scenario-card"
              key={s.scenario_id}
              onClick={() => start(s.scenario_id)}
              type="button"
            >
              <div className="scenario-card-top">
                <span className={`scenario-difficulty ${DIFFICULTY_CLASS[s.level]}`}>
                  {DIFFICULTY_LABEL[s.level]}
                </span>
                <span className="scenario-duration">{s.estimated_minutes} min</span>
              </div>

              <h2>{s.title}</h2>

              <span className="scenario-pack">{s.domain_pack}</span>

              <ul className="scenario-goals">
                {s.learning_goals.map((g) => (
                  <li key={g}>{g}</li>
                ))}
              </ul>

              <span className="scenario-start-btn">Démarrer la simulation</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
