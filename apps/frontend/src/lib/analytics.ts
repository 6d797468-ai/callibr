const API_BASE_URL =
  import.meta.env.VITE_CALLIBR_API_BASE_URL ?? "http://localhost:8000";

const PRODUCT_EVENTS = [
  "ApplicationOpened",
  "LoginSucceeded",
  "ScenarioViewed",
  "ScenarioStarted",
  "WizardCompleted",
  "FirstMessageSent",
  "ConversationCompleted",
  "ProcedureCompleted",
  "ReportViewed",
  "ReportExported",
  "SessionResumed",
  "SessionAbandoned",
] as const;

type ProductEventType = (typeof PRODUCT_EVENTS)[number];

type ProductEventPayload = {
  event_type: ProductEventType;
  tenant_id?: string;
  scenario_id?: string;
  session_id?: string;
  duration?: number;
  metadata?: Record<string, unknown>;
};

function emit(event: ProductEventPayload) {
  const body = JSON.stringify({
    ...event,
    version: "0.1.0",
    timestamp: new Date().toISOString(),
  });
  // Fire-and-forget: use sendBeacon if available, fallback to fetch
  if (navigator.sendBeacon) {
    navigator.sendBeacon(
      `${API_BASE_URL}/api/v1/product/events/ingest`,
      body,
    );
  } else {
    fetch(`${API_BASE_URL}/api/v1/product/events/ingest`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
      keepalive: true,
    }).catch(() => {});
  }
}

export function trackApplicationOpened() {
  emit({ event_type: "ApplicationOpened" });
}

export function trackScenarioViewed() {
  emit({ event_type: "ScenarioViewed" });
}

export function trackWizardCompleted() {
  emit({ event_type: "WizardCompleted" });
}

export function trackReportExported(sessionId: string) {
  emit({ event_type: "ReportExported", session_id: sessionId });
}
