import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import * as api from "../lib/api";
import type {
  AuditRecord,
  CrmActionDefinition,
  SimulationEvaluation,
  SimulationSession,
} from "../lib/types";
import VoiceChatPanel from "../components/VoiceChatPanel";

type Props = {
  token: string | null;
};

const API_BASE_URL =
  import.meta.env.VITE_CALLIBR_API_BASE_URL ?? "http://localhost:8000";

function ProcedureTimeline({
  session,
}: {
  session: SimulationSession | null;
}) {
  const steps = [
    { id: "opening", label: "Ouverture" },
    { id: "resolution", label: "Résolution" },
    { id: "closing", label: "Clôture" },
    { id: "report", label: "Rapport" },
  ];

  const currentIndex = session
    ? steps.findIndex((s) => s.id === session.current_step)
    : -1;

  return (
    <div className="procedure-timeline">
      <h3 className="section-title-sm">Procédure</h3>
      <div className="timeline-steps">
        {steps.map((step, i) => {
          const isComplete = i < currentIndex;
          const isActive = i === currentIndex;
          const isPending = i > currentIndex;
          return (
            <div
              className={`timeline-step ${isComplete ? "complete" : ""} ${isActive ? "active" : ""} ${isPending ? "pending" : ""}`}
              key={step.id}
            >
              <span className="timeline-marker">
                {isComplete ? "✓" : i + 1}
              </span>
              <span className="timeline-label">{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function PersonaCard({
  session,
}: {
  session: SimulationSession | null;
}) {
  if (!session) return null;
  const ctx = session.crm_context;
  const name = (ctx.customer_name as string) || "Client";
  return (
    <div className="persona-card">
      <h3 className="section-title-sm">Persona</h3>
      <div className="persona-avatar">{name.charAt(0)}</div>
      <div className="persona-info">
        <p className="persona-name">{name}</p>
        <p className="persona-detail">
          {session.scenario.domain_pack}
        </p>
        <p className="persona-detail">
          Commande: {String(ctx.order_id ?? "-")}
        </p>
      </div>
    </div>
  );
}

function LiveScore({
  evaluation,
}: {
  evaluation: SimulationEvaluation | null;
}) {
  if (!evaluation) return null;
  const score = evaluation.score;
  const barClass =
    score >= 70 ? "score-bar-high" : score >= 40 ? "score-bar-mid" : "score-bar-low";
  return (
    <div className="live-score">
      <h3 className="section-title-sm">Score</h3>
      <div className="score-circle">
        <span className="score-number">{score}</span>
        <span className="score-max">/100</span>
      </div>
      <div className={`score-bar ${barClass}`}>
        <div className="score-bar-fill" style={{ width: `${score}%` }} />
      </div>
      <ul className="score-criteria">
        {evaluation.criteria.map((c) => (
          <li className={`sc-criterion ${c.status}`} key={c.criterion_id}>
            <span className="sc-label">{c.label}</span>
            <span className="sc-value">
              {c.score}/{c.max_score}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ChatPanel({
  session,
  onSend,
  thinking,
}: {
  session: SimulationSession | null;
  onSend: (message: string) => void;
  thinking: boolean;
}) {
  const [draft, setDraft] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [session?.messages.length]);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    const m = draft.trim();
    if (!m || !session || thinking) return;
    onSend(m);
    setDraft("");
  }

  const messages = session?.messages ?? [];

  return (
    <div className="chat-panel">
      <div className="chat-thread">
        {messages.map((msg, i) => (
          <div className={`chat-bubble ${msg.role}`} key={i}>
            <span className="chat-role">
              {msg.role === "customer"
                ? "Client"
                : msg.role === "learner"
                  ? "Vous"
                  : "Système"}
            </span>
            <p>{msg.content}</p>
          </div>
        ))}
        {thinking && (
          <div className="chat-bubble customer thinking">
            <span className="chat-role">Client</span>
            <p className="thinking-dots">
              <span>.</span>
              <span>.</span>
              <span>.</span>
            </p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="chat-composer" onSubmit={submit}>
        <input
          disabled={!session || thinking}
          onChange={(e) => setDraft(e.target.value)}
          placeholder={
            thinking
              ? "Le client réfléchit..."
              : session?.status === "completed"
                ? "Simulation terminée"
                : "Votre réponse..."
          }
          value={draft}
        />
        <button
          disabled={!session || !draft.trim() || thinking || session?.status === "completed"}
          type="submit"
        >
          Envoyer
        </button>
      </form>
    </div>
  );
}

function CrmPanel({
  session,
  token,
}: {
  session: SimulationSession | null;
  token: string | null;
}) {
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [actions, setActions] = useState<CrmActionDefinition[]>([]);
  const [audit, setAudit] = useState<AuditRecord[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session || !bearer) return;
    api.listCrmActions(session.session_id, bearer).then(setActions).catch(() => {});
    api.getAuditTrail(session.session_id, bearer).then(setAudit).catch(() => {});
  }, [session?.session_id, bearer]);

  async function execute(actionId: string) {
    if (!session || !bearer) return;
    try {
      setError("");
      await api.executeCrmAction(session.session_id, actionId, bearer);
      const [updated] = await Promise.all([
        api.getSession(session.session_id, bearer),
        api.listCrmActions(session.session_id, bearer),
      ]);
      window.dispatchEvent(new CustomEvent("sim:refresh", { detail: updated }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Action échouée");
    }
  }

  return (
    <div className="crm-panel">
      <h3 className="section-title-sm">CRM</h3>
      <dl className="crm-context">
        <dt>Client</dt>
        <dd>{String(session?.crm_context.customer_name ?? "-")}</dd>
        <dt>Commande</dt>
        <dd>{String(session?.crm_context.order_id ?? "-")}</dd>
        <dt>Statut</dt>
        <dd>{String(session?.current_step ?? "-")}</dd>
        <dt>Ticket</dt>
        <dd>{String(session?.crm_context.ticket_status ?? "-")}</dd>
      </dl>

      <h4 className="section-title-xs">Actions</h4>
      <div className="crm-actions-list">
        {actions.map((a) => (
          <button
            disabled={!session}
            key={a.action_id}
            onClick={() => execute(a.action_id)}
            type="button"
          >
            {a.label}
          </button>
        ))}
      </div>

      {error ? <p className="error-inline">{error}</p> : null}

      {session?.crm_actions && session.crm_actions.length > 0 && (
        <>
          <h4 className="section-title-xs">Historique</h4>
          <ul className="crm-history">
            {session.crm_actions.map((a) => (
              <li key={a.execution_id}>{a.message}</li>
            ))}
          </ul>
        </>
      )}

      {audit.length > 0 && (
        <>
          <h4 className="section-title-xs">Événements</h4>
          <ul className="crm-history audit">
            {audit.slice(-5).map((r) => (
              <li key={r.audit_id}>{r.event_type}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default function SimulationPage({ token }: Props) {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const scenarioId = params.get("scenario") ?? "";
  const bearer = token ?? sessionStorage.getItem("callibr_token");
  const [session, setSession] = useState<SimulationSession | null>(null);
  const [thinking, setThinking] = useState(false);
  const [error, setError] = useState("");
  const [voiceMode, setVoiceMode] = useState(false);
  const [voiceSessionId, setVoiceSessionId] = useState<string | null>(null);

  useEffect(() => {
    if (!scenarioId) {
      navigate("/scenarios");
      return;
    }
    if (!bearer) {
      navigate("/");
      return;
    }
    api
      .startSimulation(scenarioId, bearer)
      .then((s) => {
        setSession(s);
        setError("");
      })
      .catch((err) => setError(err.message));
  }, [scenarioId, bearer, navigate]);

  useEffect(() => {
    function handler(e: Event) {
      setSession((e as CustomEvent).detail);
    }
    window.addEventListener("sim:refresh", handler);
    return () => window.removeEventListener("sim:refresh", handler);
  }, []);

  useEffect(() => {
    if (!voiceMode || !session) {
      setVoiceSessionId(null);
      return;
    }
    fetch(`${API_BASE_URL}/api/v1/voice/sessions?simulation_session_id=${session.session_id}`, {
      method: "POST",
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.session_id) setVoiceSessionId(data.session_id);
      })
      .catch(() => setError("Impossible de créer la session vocale"));
  }, [voiceMode, session?.session_id]);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!session || !bearer) return;
      setThinking(true);
      setError("");
      try {
        const result = await api.sendMessage(session.session_id, content, bearer);
        setSession(result.session);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur d'envoi");
      } finally {
        setThinking(false);
      }
    },
    [session?.session_id, bearer],
  );

  function viewReport() {
    if (!session) return;
    navigate(`/report?session=${session.session_id}`);
  }

  function replay() {
    setSession(null);
    setError("");
    navigate(`/simulation?scenario=${scenarioId}`);
  }

  return (
    <div className="simulation-page">
      <header className="sim-header">
        <div>
          <p className="eyebrow">{session?.scenario.domain_pack ?? "Simulation"}</p>
          <h1>{session?.scenario.title ?? "Chargement..."}</h1>
        </div>
        <div className="sim-header-actions">
          <button
            className="btn-secondary"
            onClick={() => navigate("/scenarios")}
            type="button"
          >
            ← Scénarios
          </button>
          {session?.status === "active" && (
            <button
              className={`btn-voice-toggle ${voiceMode ? "active" : ""}`}
              onClick={() => setVoiceMode((v) => !v)}
              type="button"
            >
              {voiceMode ? "Mode Texte" : "Mode Vocal"}
            </button>
          )}
          {session?.status === "completed" && (
            <>
              <button className="btn-primary" onClick={viewReport} type="button">
                Voir le rapport
              </button>
              <button className="btn-secondary" onClick={replay} type="button">
                Rejouer
              </button>
            </>
          )}
        </div>
      </header>

      {error && <div className="sim-error">{error}</div>}

      <div className="sim-layout">
        <aside className="sim-sidebar">
          <ProcedureTimeline session={session} />
          <LiveScore evaluation={session?.evaluation ?? null} />
        </aside>

        <section className="sim-chat-area">
          <PersonaCard session={session} />
          {voiceMode ? (
            <VoiceChatPanel
              session={session}
              onSend={sendMessage}
              thinking={thinking}
              voiceSessionId={voiceSessionId}
            />
          ) : (
            <ChatPanel
              session={session}
              onSend={sendMessage}
              thinking={thinking}
            />
          )}
        </section>

        <aside className="sim-sidebar-right">
          <CrmPanel session={session} token={token} />
        </aside>
      </div>
    </div>
  );
}
