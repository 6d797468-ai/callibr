import { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../lib/api";
import type { SimulationFeedback, TrainingIntent } from "../lib/types";

type Props = {
  sessionId: string;
  token: string;
};

const STARS = [1, 2, 3, 4, 5] as const;

function StarPicker({
  value,
  onChange,
}: {
  value: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="star-picker">
      {STARS.map((s) => (
        <button
          key={s}
          className={`star ${s <= value ? "star-filled" : "star-empty"}`}
          onClick={() => onChange(s)}
          type="button"
          aria-label={`${s} étoile${s > 1 ? "s" : ""}`}
        >
          ★
        </button>
      ))}
    </div>
  );
}

export default function FeedbackPage({ sessionId, token }: Props) {
  const navigate = useNavigate();
  const [satisfaction, setSatisfaction] = useState(0);
  const [realism, setRealism] = useState(0);
  const [difficulty, setDifficulty] = useState(0);
  const [usefulness, setUsefulness] = useState(0);
  const [trainingIntent, setTrainingIntent] = useState<TrainingIntent | null>(
    null,
  );
  const [freeText, setFreeText] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [sending, setSending] = useState(false);

  async function handleSubmit() {
    if (sending || !trainingIntent) return;
    setSending(true);
    const feedback: SimulationFeedback = {
      session_id: sessionId,
      tenant_id: "tenant_demo",
      learner_id: "learner_demo",
      satisfaction,
      perceived_realism: realism,
      difficulty,
      usefulness,
      would_use_for_training: trainingIntent,
      free_text: freeText,
      submitted_at: new Date().toISOString(),
    };
    try {
      await api.submitFeedback(feedback, token);
      setSubmitted(true);
    } catch {
      // keep form visible on error
    } finally {
      setSending(false);
    }
  }

  if (submitted) {
    return (
      <div className="feedback-page submitted">
        <div className="feedback-card">
          <h2>Merci pour votre retour !</h2>
          <p>Votre avis nous aide à améliorer la simulation.</p>
          <button
            className="btn-primary"
            onClick={() => navigate("/scenarios")}
            type="button"
          >
            ← Retour aux scénarios
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="feedback-page">
      <div className="feedback-card">
        <h2>Votre avis sur la simulation</h2>
        <p className="subtitle">
          Ces questions nous aident à améliorer l'expérience
        </p>

        <div className="feedback-field">
          <label>Satisfaction générale</label>
          <StarPicker value={satisfaction} onChange={setSatisfaction} />
        </div>

        <div className="feedback-field">
          <label>Réalisme perçu</label>
          <StarPicker value={realism} onChange={setRealism} />
        </div>

        <div className="feedback-field">
          <label>Difficulté</label>
          <StarPicker value={difficulty} onChange={setDifficulty} />
        </div>

        <div className="feedback-field">
          <label>Utilité pour votre apprentissage</label>
          <StarPicker value={usefulness} onChange={setUsefulness} />
        </div>

        <div className="feedback-field">
          <label>Recommanderiez-vous cette simulation à votre équipe ?</label>
          <div className="training-intent-picker">
            {(["yes", "maybe", "no"] as const).map((v) => (
              <button
                key={v}
                className={`btn-choice ${trainingIntent === v ? "selected" : ""}`}
                onClick={() => setTrainingIntent(v)}
                type="button"
              >
                {v === "yes"
                  ? "Oui"
                  : v === "maybe"
                    ? "Peut-être"
                    : "Non"}
              </button>
            ))}
          </div>
        </div>

        <div className="feedback-field">
          <label>Commentaire libre (optionnel)</label>
          <textarea
            className="feedback-textarea"
            value={freeText}
            onChange={(e) => setFreeText(e.target.value)}
            rows={4}
            placeholder="Qu'avez-vous aimé ? Qu'aimeriez-vous améliorer ?"
          />
        </div>

        <button
          className="btn-primary"
          disabled={sending || !trainingIntent}
          onClick={handleSubmit}
          type="button"
        >
          {sending ? "Envoi..." : "Envoyer mon avis"}
        </button>
      </div>
    </div>
  );
}
