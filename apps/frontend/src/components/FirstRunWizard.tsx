import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";
import type { ScenarioSummary } from "../lib/types";

const STEPS = [
  { id: "welcome", label: "Bienvenue" },
  { id: "system", label: "Votre système" },
  { id: "scenario", label: "Votre première simulation" },
  { id: "done", label: "Bravo" },
];

type SystemCheckItem = {
  name: string;
  status: "passed" | "warning" | "failed";
  label: string;
  detail: string;
  timing_ms: number;
};

type SystemCheckResult = {
  score: number;
  ready: boolean;
  warnings: number;
  checks: SystemCheckItem[];
};

type Props = {
  token: string;
  scenarios: ScenarioSummary[];
};

function levelClass(level: string): string {
  if (level === "foundation") return "easy";
  if (level === "intermediate") return "mid";
  return "hard";
}

export default function FirstRunWizard({ token, scenarios }: Props) {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [checkResult, setCheckResult] = useState<SystemCheckResult | null>(null);
  const [checking, setChecking] = useState(false);
  const [micStatus, setMicStatus] = useState<"idle" | "testing" | "passed" | "failed" | "skipped">("idle");
  const [selectedScenario, setSelectedScenario] = useState<ScenarioSummary | null>(null);
  const [starting, setStarting] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const runSystemCheck = useCallback(() => {
    setChecking(true);
    apiFetch<SystemCheckResult>("/api/v1/pilot/system-check", token)
      .then(setCheckResult)
      .catch(() => setCheckResult({
        score: 0, ready: false, warnings: 99,
        checks: [{ name: "api", status: "failed", label: "API", detail: "Impossible de contacter le serveur", timing_ms: 0 }],
      }))
      .finally(() => setChecking(false));
  }, [token]);

  useEffect(() => {
    if (step === 1 && !checkResult && !checking) runSystemCheck();
  }, [step, checkResult, checking, runSystemCheck]);

  async function testMic() {
    setMicStatus("testing");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorder.current = recorder;
      audioChunks.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.current.push(e.data);
      };

      recorder.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(audioChunks.current, { type: "audio/webm" });
        setMicStatus(blob.size > 0 ? "passed" : "failed");
      };

      recorder.start();
      setTimeout(() => {
        if (recorder.state === "recording") recorder.stop();
      }, 1500);
    } catch {
      setMicStatus("failed");
    }
  }

  const needsMicTest = checkResult
    && checkResult.checks.some(c => c.name === "stt" && c.status === "passed" && c.detail.includes("Deepgram"))
    || checkResult?.checks.some(c => c.name === "tts" && c.status === "passed" && c.detail.includes("ElevenLabs"));

  const micResolved = micStatus === "passed" || micStatus === "failed" || micStatus === "skipped";

  function next() {
    if (step < 3) setStep(step + 1);
  }

  function back() {
    if (step > 0) setStep(step - 1);
  }

  async function launch() {
    if (!selectedScenario) return;
    setStarting(true);
    localStorage.setItem("callibr_first_run", "done");
    navigate(`/simulation?scenario=${selectedScenario.scenario_id}`);
  }

  function finish() {
    localStorage.setItem("callibr_first_run", "done");
    navigate("/scenarios");
  }

  return (
    <div className="wizard-overlay">
      <div className="wizard-card">
        <div className="wizard-header">
          <h1>
            {step === 0 && "Bienvenue dans Callibr"}
            {step === 1 && "Vérification de votre poste"}
            {step === 2 && "Choisissez votre scénario"}
            {step === 3 && "Vous êtes prêt"}
          </h1>
          <p className="wizard-subtitle">
            {step === 0 && "En quelques clics, vous allez vivre votre première simulation de formation."}
            {step === 1 && "Nous analysons votre environnement pour vous offrir la meilleure expérience."}
            {step === 2 && "Sélectionnez la mise en situation qui correspond à vos objectifs."}
            {step === 3 && "Tout est en place pour démarrer votre première formation."}
          </p>
        </div>

        <div className="wizard-steps">
          {STEPS.map((s, i) => (
            <div key={s.id} className={`wiz-step ${i === step ? "wiz-active" : i < step ? "wiz-done" : "wiz-pending"}`}>
              <span className="wiz-num">{i < step ? "✓" : i + 1}</span>
              <span className="wiz-label">{s.label}</span>
            </div>
          ))}
        </div>

        <div className="wizard-body">
          {/* ── Step 0: Welcome ── */}
          {step === 0 && (
            <div className="wiz-welcome">
              <div className="wiz-welcome-icon">
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                  <rect x="8" y="20" width="48" height="32" rx="4" stroke="#245b78" strokeWidth="2" fill="#f0f4f8" />
                  <circle cx="32" cy="36" r="8" fill="#245b78" />
                  <path d="M28 36l3 3 5-6" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M22 16l4-8h12l4 8" stroke="#245b78" strokeWidth="2" fill="none" strokeLinejoin="round" />
                </svg>
              </div>
              <p className="wiz-welcome-text">
                Callibr vous permet de vous entraîner à des mises en situation professionnelles
                grâce à l'intelligence artificielle. Vous dialoguerez avec un client virtuel
                et recevrez un rapport détaillé sur votre performance.
              </p>
              <div className="wiz-welcome-features">
                <div className="wiz-wf-item">
                  <span className="wiz-wf-icon">🎙</span>
                  <span>Commandes vocales ou texte</span>
                </div>
                <div className="wiz-wf-item">
                  <span className="wiz-wf-icon">📋</span>
                  <span>Scénarios réalistes</span>
                </div>
                <div className="wiz-wf-item">
                  <span className="wiz-wf-icon">📊</span>
                  <span>Rapport immédiat</span>
                </div>
              </div>
            </div>
          )}

          {/* ── Step 1: System Check + optional voice test ── */}
          {step === 1 && (
            <div className="wiz-system">
              {checking ? (
                <div className="wiz-loading">
                  <div className="login-spinner" />
                  <p>Analyse de votre configuration...</p>
                </div>
              ) : checkResult ? (
                <>
                  {/* Score bar */}
                  <div className="wiz-score-bar">
                    <div className="wiz-score-info">
                      <span className="wiz-score-label">Score système</span>
                      <span className={`wiz-score-value ${checkResult.ready ? "wiz-score-good" : "wiz-score-warn"}`}>
                        {checkResult.score}%
                      </span>
                      {checkResult.ready
                        ? <span className="wiz-score-badge badge-ready">Prêt</span>
                        : <span className="wiz-score-badge badge-warn">{checkResult.warnings} alerte(s)</span>
                      }
                    </div>
                    <div className="wiz-score-track">
                      <div className={`wiz-score-fill ${checkResult.ready ? "fill-ready" : "fill-warn"}`}
                        style={{ width: `${Math.min(checkResult.score, 100)}%` }} />
                    </div>
                  </div>

                  {/* Check items */}
                  {checkResult.checks.map((c) => (
                    <div key={c.name} className={`wiz-check status-${c.status}`}>
                      <span className="wiz-check-icon">
                        {c.status === "passed" ? "✓" : "!"}
                      </span>
                      <div className="wiz-check-body">
                        <strong>{c.label}</strong>
                        <span className="wiz-check-detail">{c.detail}</span>
                      </div>
                      {c.timing_ms > 0 && <span className="wiz-check-time">{c.timing_ms} ms</span>}
                    </div>
                  ))}

                  {!checkResult.ready && (
                    <p className="wiz-check-foot">
                      Certains services ne sont pas configurés. Vous pouvez continuer — ils seront simulés.
                    </p>
                  )}

                  {/* Adaptive voice test */}
                  {needsMicTest && !micResolved && (
                    <div className="wiz-mic-section">
                      <hr className="wiz-divider" />
                      <div className="wiz-voice-test">
                        <div className="wiz-mic-icon">
                          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#245b78" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                            <line x1="12" y1="19" x2="12" y2="23" />
                            <line x1="8" y1="23" x2="16" y2="23" />
                          </svg>
                        </div>
                        <div className="wiz-voice-body">
                          <strong>Testez votre microphone</strong>
                          <span className="wiz-check-detail">Un microphone est recommandé pour la reconnaissance vocale.</span>
                          <div className="wiz-mic-actions" style={{ marginTop: 8 }}>
                            <button className="btn-primary" onClick={testMic} type="button">Tester</button>
                            <button className="btn-secondary" onClick={() => setMicStatus("skipped")} type="button" style={{ marginLeft: 8 }}>
                              Continuer en mode texte
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {needsMicTest && micStatus === "testing" && (
                    <div className="wiz-mic-section">
                      <hr className="wiz-divider" />
                      <div className="wiz-voice-test">
                        <span className="wiz-pulse" style={{ marginRight: 12 }} />
                        <span>Test en cours — parlez quelques secondes...</span>
                      </div>
                    </div>
                  )}

                  {micStatus === "passed" && (
                    <div className="wiz-mic-section">
                      <hr className="wiz-divider" />
                      <div className="wiz-voice-test wiz-voice-passed">
                        <span style={{ color: "#2f7d57", fontSize: 20, fontWeight: 700, marginRight: 8 }}>✓</span>
                        Microphone opérationnel
                      </div>
                    </div>
                  )}

                  {micStatus === "failed" && (
                    <div className="wiz-mic-section">
                      <hr className="wiz-divider" />
                      <div className="wiz-voice-test wiz-voice-failed">
                        <span style={{ color: "#c62828", fontSize: 20, fontWeight: 700, marginRight: 8 }}>!</span>
                        <div>
                          <strong>Microphone non détecté</strong>
                          <p className="wiz-check-detail" style={{ margin: "2px 0 0" }}>
                            Vous pourrez dialoguer par texte. Voulez-vous réessayer ou continuer ?
                          </p>
                          <div className="wiz-mic-actions" style={{ marginTop: 8 }}>
                            <button className="btn-secondary" onClick={testMic} type="button">Réessayer</button>
                            <button className="btn-secondary" onClick={() => setMicStatus("skipped")} type="button" style={{ marginLeft: 8 }}>
                              Continuer en mode texte
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="wiz-loading">
                  <p>Impossible de vérifier le système.</p>
                  <button className="btn-secondary" onClick={runSystemCheck} type="button">Réessayer</button>
                </div>
              )}
            </div>
          )}

          {/* ── Step 2: Scenario Select ── */}
          {step === 2 && (
            <div className="wiz-scenarios">
              {scenarios.length === 0 ? (
                <p className="wiz-empty">Aucun scénario disponible.</p>
              ) : (
                <div className="wiz-scroll">
                  {scenarios.map((s) => (
                    <button
                      key={s.scenario_id}
                      className={`wiz-scenario ${selectedScenario?.scenario_id === s.scenario_id ? "wiz-selected" : ""}`}
                      onClick={() => setSelectedScenario(s)}
                      type="button"
                    >
                      <div className="wiz-sc-top">
                        <h3>{s.title}</h3>
                        <span className={`scenario-difficulty diff-${levelClass(s.level)}`}>
                          {s.level === "foundation" ? "Fondation" : s.level === "intermediate" ? "Intermédiaire" : "Avancé"}
                        </span>
                      </div>
                      <p className="wiz-sc-desc">{s.domain_pack}</p>
                      {s.learning_goals && s.learning_goals.length > 0 && (
                        <ul className="wiz-sc-goals">
                          {s.learning_goals.slice(0, 2).map((g, i) => (
                            <li key={i}>{g}</li>
                          ))}
                        </ul>
                      )}
                      {s.estimated_minutes && (
                        <span className="wiz-sc-time">~{s.estimated_minutes} min</span>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* ── Step 3: Ready / Bravo ── */}
          {step === 3 && (
            <div className="wiz-ready">
              <div className="wiz-ready-icon">
                <span className="wiz-ready-check">✓</span>
              </div>
              <div className="wiz-ready-body">
                <h2>
                  {selectedScenario
                    ? `${selectedScenario.title} — prêt à démarrer`
                    : "Prêt à démarrer"}
                </h2>
                <p className="wiz-ready-detail">
                  Votre environnement est configuré, votre scénario est sélectionné.
                  Vous allez dialoguer avec un client virtuel et recevoir un rapport
                  détaillé à la fin de l'entretien.
                </p>
                {checkResult && (
                  <div className="wiz-ready-meta">
                    <span>Système : {checkResult.score}%</span>
                    {micStatus === "passed" && <span>Micro : OK</span>}
                    {selectedScenario?.estimated_minutes && (
                      <span>Durée : ~{selectedScenario.estimated_minutes} min</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="wizard-footer">
          <div className="wizard-footer-left">
            {step > 0 && step < 3 && (
              <button className="btn-secondary" onClick={back} type="button">← Retour</button>
            )}
          </div>
          <div className="wizard-footer-right">
            <button className="btn-secondary" onClick={finish} type="button" style={{ marginRight: 8 }}>
              Accéder à l'accueil
            </button>

            {step === 0 && (
              <button className="btn-primary" onClick={next} type="button">
                C'est parti →
              </button>
            )}

            {step === 1 && (
              <button className="btn-primary"
                disabled={checking || (needsMicTest && micStatus === "testing")}
                onClick={next} type="button">
                Continuer →
              </button>
            )}

            {step === 2 && (
              <button className="btn-primary"
                disabled={!selectedScenario}
                onClick={next} type="button">
                Continuer →
              </button>
            )}

            {step === 3 && (
              <button className="btn-primary"
                disabled={starting}
                onClick={selectedScenario ? launch : finish} type="button">
                {starting ? "Préparation..." : selectedScenario ? "Commencer ma première formation" : "Accéder à l'accueil"}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
