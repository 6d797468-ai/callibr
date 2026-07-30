import type {
  AuthToken,
  AuthenticatedUser,
  CrmActionDefinition,
  CrmActionExecution,
  ScenarioSummary,
  SessionReport,
  SimulationFeedback,
  SimulationSession,
  AuditRecord,
} from "./types";

const API_BASE_URL =
  import.meta.env.VITE_CALLIBR_API_BASE_URL ?? "http://localhost:8000";
const DEMO_TRACE_ID = "trace_frontend_demo";

function apiHeaders(token: string | null): Record<string, string> {
  const h: Record<string, string> = {
    "Content-Type": "application/json",
    "X-Trace-Id": DEMO_TRACE_ID,
  };
  if (token) {
    h.Authorization = `Bearer ${token}`;
  } else {
    h["X-Tenant-Id"] = "tenant_demo";
    h["X-User-Id"] = "learner_demo";
  }
  return h;
}

export async function apiFetch<T>(
  path: string,
  token: string | null,
  init?: RequestInit,
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { ...apiHeaders(token), ...init?.headers },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.message ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export function login(): Promise<AuthToken> {
  return apiFetch<AuthToken>("/api/v1/auth/login", null, {
    method: "POST",
    body: JSON.stringify({
      tenant_id: "tenant_demo",
      email: "learner@demo.callibr.local",
      password: "callibr-demo",
    }),
  });
}

export function listScenarios(token: string): Promise<ScenarioSummary[]> {
  return apiFetch<ScenarioSummary[]>("/api/v1/scenarios", token);
}

export function startSimulation(
  scenarioId: string,
  token: string,
): Promise<SimulationSession> {
  return apiFetch<SimulationSession>("/api/v1/simulations", token, {
    method: "POST",
    body: JSON.stringify({
      scenario_id: scenarioId,
    }),
  });
}

export function getSession(
  sessionId: string,
  token: string,
): Promise<SimulationSession> {
  return apiFetch<SimulationSession>(
    `/api/v1/simulations/${sessionId}`,
    token,
  );
}

export function sendMessage(
  sessionId: string,
  content: string,
  token: string,
): Promise<{ session: SimulationSession }> {
  return apiFetch<{ session: SimulationSession }>(
    `/api/v1/simulations/${sessionId}/messages`,
    token,
    {
      method: "POST",
      body: JSON.stringify({ content }),
    },
  );
}

export function listCrmActions(
  sessionId: string,
  token: string,
): Promise<CrmActionDefinition[]> {
  return apiFetch<CrmActionDefinition[]>(
    `/api/v1/simulations/${sessionId}/crm/actions`,
    token,
  );
}

export function executeCrmAction(
  sessionId: string,
  actionId: string,
  token: string,
): Promise<CrmActionExecution> {
  return apiFetch<CrmActionExecution>(
    `/api/v1/simulations/${sessionId}/crm/actions`,
    token,
    {
      method: "POST",
      body: JSON.stringify({ action_id: actionId }),
    },
  );
}

export function getAuditTrail(
  sessionId: string,
  token: string,
): Promise<AuditRecord[]> {
  return apiFetch<AuditRecord[]>(
    `/api/v1/simulations/${sessionId}/audit`,
    token,
  );
}

export function getSessionReport(
  sessionId: string,
  token: string,
): Promise<SessionReport> {
  return apiFetch<SessionReport>(
    `/api/v1/simulations/${sessionId}/report`,
    token,
  );
}

export function submitFeedback(
  feedback: SimulationFeedback,
  token: string,
): Promise<{ status: string }> {
  return apiFetch<{ status: string }>("/api/v1/feedback", token, {
    method: "POST",
    body: JSON.stringify(feedback),
  });
}
