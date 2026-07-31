export type ScenarioSummary = {
  scenario_id: string;
  domain_pack: string;
  title: string;
  level: "foundation" | "intermediate" | "advanced";
  channel: "chat" | "voice" | "email" | "backoffice";
  estimated_minutes: number;
  learning_goals: string[];
};

export type SimulationMessage = {
  role: "learner" | "customer" | "system" | "coach";
  content: string;
  at: string;
  metadata: Record<string, unknown>;
};

export type EvaluationCriterionResult = {
  criterion_id: string;
  label: string;
  status: "passed" | "missed";
  score: number;
  max_score: number;
  evidence: string[];
  feedback: string;
};

export type SimulationEvaluation = {
  score: number;
  max_score: number;
  criteria: EvaluationCriterionResult[];
  strengths: string[];
  risks: string[];
  next_best_actions: string[];
};

export type CrmActionDefinition = {
  action_id: string;
  label: string;
  category: string;
  description: string;
  required_fields: string[];
  produces: string[];
};

export type CrmActionExecution = {
  execution_id: string;
  action_id: string;
  label: string;
  status: "succeeded" | "blocked";
  executed_at: string;
  message: string;
  output: Record<string, unknown>;
};

export type AuditRecord = {
  audit_id: string;
  event_type: string;
  tenant_id: string;
  aggregate_type: string;
  aggregate_id: string;
  occurred_at: string;
  trace_id: string;
  actor_id: string | null;
  payload: Record<string, unknown>;
};

export type AuthenticatedUser = {
  tenant_id: string;
  user_id: string;
  email: string;
  display_name: string;
  roles: string[];
  trace_id: string;
};

export type AuthToken = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user: AuthenticatedUser;
};

export type SimulationSession = {
  session_id: string;
  tenant_id: string;
  learner_id: string;
  scenario: ScenarioSummary;
  status: "active" | "completed";
  current_step: string;
  started_at: string;
  completed_at: string | null;
  messages: SimulationMessage[];
  crm_context: Record<string, unknown>;
  crm_actions: CrmActionExecution[];
  evaluation: SimulationEvaluation | null;
  conversation_session_id?: string;
  procedure_execution_id?: string;
};

export type SessionReport = {
  session_id: string;
  tenant_id: string;
  learner_id: string;
  scenario: ScenarioSummary;
  status: "active" | "completed";
  generated_at: string;
  started_at: string;
  completed_at: string | null;
  duration_seconds: number;
  message_count: number;
  learner_message_count: number;
  customer_message_count: number;
  crm_action_count: number;
  audit_event_count: number;
  final_score: number;
  max_score: number;
  criteria: EvaluationCriterionResult[];
  strengths: string[];
  risks: string[];
  next_best_actions: string[];
  crm_actions: CrmActionExecution[];
  procedure_execution_id?: string;
  procedure_progress?: StepProgress[];
};

export type StepProgress = {
  step_id: string;
  status: string;
  score: number;
  completed_at: string | null;
};

export type TrainingIntent = "yes" | "maybe" | "no";

export type SimulationFeedback = {
  session_id: string;
  tenant_id: string;
  learner_id: string;
  satisfaction: number;
  perceived_realism: number;
  difficulty: number;
  usefulness: number;
  would_use_for_training: TrainingIntent;
  free_text: string;
  submitted_at: string;
};

export const DEMO_LOGIN = {
  tenant_id: "tenant_demo",
  email: "learner@demo.callibr.local",
  password: "callibr-demo",
};

export type ApiErrorCause = "timeout" | "network" | "http" | "parse";

export type ApiErrorPayload = {
  code?: string | null;
  message?: string | null;
  title?: string | null;
  explanation?: string | null;
  action?: string | null;
  retryable?: boolean | null;
  details?: Record<string, unknown> | null;
  http_status?: number | null;
  trace_id?: string | null;
};

export class ApiError extends Error {
  readonly code: string;
  readonly causeType: ApiErrorCause;
  readonly httpStatus: number | null;
  readonly payload: ApiErrorPayload;
  readonly traceId?: string;
  readonly original?: unknown;

  constructor(
    code: string,
    causeType: ApiErrorCause,
    message: string,
    payload: ApiErrorPayload = {},
    httpStatus: number | null = null,
    original?: unknown,
    traceId?: string,
  ) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.causeType = causeType;
    this.httpStatus = httpStatus;
    this.payload = payload;
    this.traceId = traceId;
    this.original = original;
  }

  static fromHttp(
    status: number,
    payload: ApiErrorPayload,
    traceId?: string,
  ): ApiError {
    return new ApiError(
      payload.code ?? `HTTP_${status}`,
      "http",
      payload.message ?? `HTTP ${status}`,
      payload,
      status,
      undefined,
      traceId,
    );
  }
}
