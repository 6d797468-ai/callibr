import { useCallback, useEffect, useRef, useState } from "react";
import type { SimulationSession } from "../lib/types";
import ErrorPanel from "./ErrorPanel";
import type { UserFacingError } from "../lib/errors";

const VOICE_WS_URL =
  import.meta.env.VITE_CALLIBR_WS_URL ?? "ws://localhost:8000";

type MicState = "idle" | "requesting" | "listening" | "processing" | "speaking";

type Props = {
  session: SimulationSession | null;
  onSend: (message: string) => void;
  thinking: boolean;
  voiceSessionId: string | null;
};

function MicIcon({ state }: { state: MicState }) {
  const colors: Record<MicState, string> = {
    idle: "#666",
    requesting: "#888",
    listening: "#e53935",
    processing: "#fdd835",
    speaking: "#43a047",
  };
  return (
    <svg
      fill="none"
      height="32"
      viewBox="0 0 24 24"
      width="32"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect
        fill={colors[state]}
        height="12"
        rx="3"
        width="8"
        x="8"
        y="2"
      />
      <path
        d="M5 11a7 7 0 0 0 14 0"
        stroke={colors[state]}
        strokeLinecap="round"
        strokeWidth="2"
      />
      <line
        stroke={colors[state]}
        strokeLinecap="round"
        strokeWidth="2"
        x1="12"
        x2="12"
        y1="18"
        y2="22"
      />
      {state === "listening" && (
        <g>
          <circle cx="16" cy="6" fill={colors[state]} r="1.5" opacity="0.6" />
          <circle cx="19" cy="10" fill={colors[state]} r="1" opacity="0.4" />
        </g>
      )}
      {state === "speaking" && (
        <g>
          <circle cx="16" cy="6" fill={colors[state]} r="1.5" />
          <circle cx="19" cy="10" fill={colors[state]} r="1" />
          <circle cx="20" cy="15" fill={colors[state]} r="0.8" opacity="0.6" />
        </g>
      )}
    </svg>
  );
}

export default function VoiceChatPanel({
  session,
  onSend,
  thinking,
  voiceSessionId,
}: Props) {
  const [micState, setMicState] = useState<MicState>("idle");
  const [transcript, setTranscript] = useState("");
  const [error, setError] = useState<UserFacingError | null>(null);
  const [wsAttempt, setWsAttempt] = useState(0);
  const retryRef = useRef<(() => void) | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [session?.messages.length]);

  const connectWs = useCallback(
    (sid: string) => {
      const ws = new WebSocket(
        `${VOICE_WS_URL}/api/v1/voice/sessions/${sid}/stream`,
      );
      ws.onopen = () => setMicState("listening");
      ws.onclose = () => {
        setMicState((m) => (m === "idle" ? m : "idle"));
      };
      ws.onerror = () => {
        const friendly: UserFacingError = {
          title: "Connexion vocale perdue",
          explanation:
            "La connexion au serveur vocal a été interrompue.",
          action: "Cliquez sur « Réessayer » pour rétablir la connexion.",
          retryable: true,
        };
        retryRef.current = retryConnection;
        setError(friendly);
      };
      ws.onmessage = async (event) => {
        if (event.data instanceof Blob) {
          setMicState("speaking");
          const blob = event.data;
          const url = URL.createObjectURL(blob);
          const audio = new Audio(url);
          audioRef.current = audio;
          audio.onended = () => {
            URL.revokeObjectURL(url);
            setMicState("listening");
          };
          await audio.play();
        } else {
          try {
            const msg = JSON.parse(event.data);
            if (msg.type === "transcription") {
              setTranscript(msg.text);
              onSend(msg.text);
              setMicState("listening");
            } else if (msg.type === "session_ended") {
              setMicState("idle");
            } else if (msg.type === "info") {
              setTranscript(msg.message);
            } else if (msg.type === "error") {
              const friendly: UserFacingError = {
                title: msg.title ?? "Conversation vocale interrompue",
                explanation:
                  msg.message ??
                  "Une erreur technique est survenue pendant la conversation vocale.",
                action: msg.action ?? "Réessayez.",
                retryable: true,
              };
              retryRef.current = retryConnection;
              setError(friendly);
            }
          } catch {
            // ignore parse errors
          }
        }
      };
      wsRef.current = ws;
    },
    [onSend],
  );

  function retryConnection() {
    setError(null);
    wsRef.current?.close();
    setWsAttempt((n) => n + 1);
  }

  useEffect(() => {
    if (voiceSessionId && session?.status === "active") {
      connectWs(voiceSessionId);
    }
    return () => {
      wsRef.current?.close();
    };
  }, [voiceSessionId, session?.status, connectWs, wsAttempt]);

  async function startListening() {
    if (micState === "listening") return;
    setError(null);
    setTranscript("");
    try {
      setMicState("requesting");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
          ? "audio/webm;codecs=opus"
          : "audio/webm",
      });
      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
          if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(e.data);
          }
        }
      };
      recorder.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(
            JSON.stringify({ action: "stop_listening" }),
          );
        }
        setMicState("processing");
      };
      recorder.start(250);
      mediaRecorderRef.current = recorder;
      setMicState("listening");
    } catch (err) {
      const denied = err instanceof DOMException && err.name === "NotAllowedError";
      const friendly: UserFacingError = {
        title: denied ? "Microphone non autorisé" : "Erreur microphone",
        explanation: denied
          ? "L'accès au microphone a été refusé."
          : "Le microphone n'a pas pu être démarré.",
        action: denied
          ? "Autorisez l'accès au micro dans votre navigateur, puis réessayez."
          : "Vérifiez votre microphone, puis réessayez.",
        retryable: true,
      };
      retryRef.current = () => void startListening();
      setError(friendly);
      setMicState("idle");
    }
  }

  function stopListening() {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
    }
  }

  function toggleMic() {
    if (micState === "listening") {
      stopListening();
    } else {
      startListening();
    }
  }

  const messages = session?.messages ?? [];
  const disabled =
    !session ||
    thinking ||
    session.status === "completed" ||
    !voiceSessionId;

  return (
    <div className="chat-panel voice-chat-panel">
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

      <div className="voice-controls">
        <div className="voice-mic-status">
          <MicIcon state={micState} />
          <span className="mic-label">
            {micState === "idle" && "Appuyez pour parler"}
            {micState === "requesting" && "Accès micro..."}
            {micState === "listening" && "Écoute..."}
            {micState === "processing" && "Traitement..."}
            {micState === "speaking" && "Réponse vocale..."}
          </span>
        </div>

        {transcript && (
          <p className="voice-transcript">"{transcript}"</p>
        )}

        {error && (
          <ErrorPanel
            error={error}
            onRetry={() => retryRef.current?.()}
          />
        )}

        <button
          className={`voice-ptt-btn ${micState === "listening" ? "recording" : ""}`}
          disabled={disabled}
          onClick={toggleMic}
          type="button"
        >
          {micState === "listening" ? "Relâcher" : "Push to Talk"}
        </button>
      </div>
    </div>
  );
}
