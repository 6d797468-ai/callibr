from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

from callibr_contracts import (
    AuditRecord,
    AuthenticatedUser,
    AuthToken,
    CrmActionDefinition,
    ExecuteCrmActionRequest,
    ExecuteCrmActionResponse,
    LoginRequest,
    PilotDashboard,
    ScenarioSummary,
    SendMessageRequest,
    SendMessageResponse,
    SessionReplay,
    SessionReport,
    SimulationSession,
    StartSimulationRequest,
)
from callibr_contracts.feedback import SimulationFeedback
from callibr_contracts.telemetry import FeedbackRecord, ProductEvent
from callibr_identity import DemoIdentityProvider
from callibr_kernel import CallibrError, TenantContext, new_trace_id
from callibr_seed import load_demo_catalogue
from callibr_simulation import SimulationService
from callibr_telemetry import configure_logging
from callibr_telemetry.dashboard import DashboardService
from callibr_telemetry.pilot import PilotDashboardService
from callibr_telemetry.readiness import PilotReadinessService, ReadinessResult
from callibr_telemetry.report import generate_pdf
from fastapi import Depends, FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel

from callibr_api.config import ConfigValidator, get_settings
from callibr_api.dependencies import (
    get_dashboard_service,
    get_feedback_store,
    get_identity_provider,
    get_persona_service,
    get_pilot_dashboard_service,
    get_procedure_service,
    get_product_event_store,
    get_readiness_service,
    get_rule_service,
    get_scenario_service,
    get_simulation_service,
    get_tenant_context,
)
from callibr_api.middleware import PrometheusMiddleware
from callibr_api.routes import conversation as conversation_router
from callibr_api.routes import persona as persona_router
from callibr_api.routes import procedure as procedure_router
from callibr_api.routes import rule as rule_router
from callibr_api.routes import scenario as scenario_router
from callibr_api.routes import voice as voice_router

SimulationServiceDep = Annotated[SimulationService, Depends(get_simulation_service)]
TenantContextDep = Annotated[TenantContext, Depends(get_tenant_context)]
IdentityProviderDep = Annotated[DemoIdentityProvider, Depends(get_identity_provider)]
DashboardServiceDep = Annotated[DashboardService, Depends(get_dashboard_service)]
PilotDashboardServiceDep = Annotated[PilotDashboardService, Depends(get_pilot_dashboard_service)]
ReadinessServiceDep = Annotated[PilotReadinessService, Depends(get_readiness_service)]


def _emit_product_event(
    event_type: str,
    tenant_id: str = "tenant_demo",
    scenario_id: str = "",
    session_id: str = "",
    duration: float = 0.0,
    metadata: dict | None = None,
) -> None:
    store = get_product_event_store()
    store.record(
        ProductEvent(
            event_type=event_type,
            tenant_id=tenant_id,
            timestamp=datetime.now(UTC).isoformat(),
            scenario_id=scenario_id,
            persona_id="",
            procedure_id="",
            session_id=session_id,
            duration=duration,
            version="0.1.0",
            metadata=metadata,
        )
    )


def _status_code_for(error: CallibrError) -> int:
    if error.code.startswith("AUTH"):
        return 401
    if error.code.endswith("_FORBIDDEN"):
        return 403
    if error.code.endswith("_NOT_FOUND") or error.code == "HANDLER_NOT_FOUND":
        return 404
    if error.code.endswith("_BLOCKED"):
        return 409
    if error.code == "HANDLER_ALREADY_REGISTERED":
        return 409
    return 400


def create_app() -> FastAPI:
    # Validate configuration before any other initialisation
    ConfigValidator().validate_or_exit()
    settings = get_settings()
    configure_logging()

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        """Seed reference data into in-memory stores at startup."""
        load_demo_catalogue(
            persona_service=get_persona_service(),
            procedure_service=get_procedure_service(),
            rule_service=get_rule_service(),
            scenario_service=get_scenario_service(),
        )
        yield

    app = FastAPI(
        title="Callibr API",
        version="0.1.0",
        description="Callibr AI contact center simulation platform API",
        lifespan=lifespan,
    )
    app.add_middleware(PrometheusMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        request.state.trace_id = request.headers.get("X-Trace-Id") or new_trace_id()
        response = await call_next(request)
        response.headers["X-Trace-Id"] = request.state.trace_id
        return response

    @app.exception_handler(CallibrError)
    async def callibr_error_handler(_: Request, exc: CallibrError) -> JSONResponse:
        return JSONResponse(
            status_code=_status_code_for(exc),
            content={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.get("/health", tags=["platform"])
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": settings.service_name,
            "environment": settings.env,
        }

    @app.get("/api/v1/platform/info", tags=["platform"])
    def platform_info() -> dict[str, str]:
        return {
            "product": "Callibr",
            "architecture": "ATOS",
            "phase": "P1 Simulation Core MVP",
            "tenant": settings.demo_tenant_id,
        }

    @app.get("/api/v1/me", response_model=AuthenticatedUser, tags=["identity"])
    def current_user(
        context: TenantContextDep,
        identity_provider: IdentityProviderDep,
    ) -> AuthenticatedUser:
        return identity_provider.authenticate(context)

    @app.post("/api/v1/auth/login", response_model=AuthToken, tags=["identity"])
    def login(
        request: LoginRequest,
        context: TenantContextDep,
        identity_provider: IdentityProviderDep,
    ) -> AuthToken:
        effective_request = request.model_copy(
            update={"tenant_id": request.tenant_id or context.tenant_id}
        )
        token = identity_provider.login(effective_request, context.trace_id or "-")
        _emit_product_event("LoginSucceeded", tenant_id=token.user.tenant_id)
        return token

    @app.get("/api/v1/scenarios", response_model=list[ScenarioSummary], tags=["scenarios"])
    def list_scenarios(
        service: SimulationServiceDep,
    ) -> list[ScenarioSummary]:
        return service.list_scenarios()

    @app.post(
        "/api/v1/simulations",
        response_model=SimulationSession,
        status_code=201,
        tags=["simulations"],
    )
    def start_simulation(
        request: StartSimulationRequest,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> SimulationSession:
        effective_request = request.model_copy(
            update={
                "tenant_id": context.tenant_id,
                "learner_id": context.user_id or request.learner_id,
            }
        )
        session = service.start_session(effective_request, context)
        _emit_product_event(
            "ScenarioStarted",
            tenant_id=context.tenant_id,
            scenario_id=session.scenario.scenario_id,
            session_id=session.session_id,
        )
        return session

    @app.get(
        "/api/v1/simulations/{session_id}",
        response_model=SimulationSession,
        tags=["simulations"],
    )
    def get_simulation(
        session_id: str,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> SimulationSession:
        session = service.get_session(session_id, context)
        if session.status == "active" and len(session.messages) > 1:
            _emit_product_event(
                "SessionResumed",
                tenant_id=context.tenant_id,
                scenario_id=session.scenario.scenario_id,
                session_id=session_id,
            )
        return session

    @app.post(
        "/api/v1/simulations/{session_id}/messages",
        response_model=SendMessageResponse,
        tags=["simulations"],
    )
    def send_message(
        session_id: str,
        request: SendMessageRequest,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> SendMessageResponse:
        result = service.send_message(session_id, request, context)
        msg_count = len(result.session.messages)
        if msg_count == 2:  # first reply = opening (customer) + first learner
            _emit_product_event(
                "FirstMessageSent",
                tenant_id=context.tenant_id,
                scenario_id=result.session.scenario.scenario_id,
                session_id=session_id,
            )
        if result.session.status == "completed":
            _emit_product_event(
                "ConversationCompleted",
                tenant_id=context.tenant_id,
                scenario_id=result.session.scenario.scenario_id,
                session_id=session_id,
            )
        return result

    @app.get(
        "/api/v1/simulations/{session_id}/crm/actions",
        response_model=list[CrmActionDefinition],
        tags=["crm"],
    )
    def list_crm_actions(
        session_id: str,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> list[CrmActionDefinition]:
        return service.list_crm_actions(session_id, context)

    @app.post(
        "/api/v1/simulations/{session_id}/crm/actions",
        response_model=ExecuteCrmActionResponse,
        tags=["crm"],
    )
    def execute_crm_action(
        session_id: str,
        request: ExecuteCrmActionRequest,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> ExecuteCrmActionResponse:
        return service.execute_crm_action(session_id, request, context)

    @app.get(
        "/api/v1/simulations/{session_id}/audit",
        response_model=list[AuditRecord],
        tags=["audit"],
    )
    def get_simulation_audit(
        session_id: str,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> list[AuditRecord]:
        return service.get_audit_trail(session_id, context)

    @app.get(
        "/api/v1/simulations/{session_id}/report",
        response_model=SessionReport,
        tags=["evaluation"],
    )
    def get_simulation_report(
        session_id: str,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> SessionReport:
        report = service.get_session_report(session_id, context)
        _emit_product_event(
            "ReportViewed",
            tenant_id=context.tenant_id,
            scenario_id=report.scenario.scenario_id,
            session_id=session_id,
        )
        return report

    @app.get(
        "/api/v1/simulations/{session_id}/replay",
        response_model=SessionReplay,
        tags=["simulations"],
    )
    def get_simulation_replay(
        session_id: str,
        context: TenantContextDep,
        service: SimulationServiceDep,
    ) -> SessionReplay:
        return service.get_replay(session_id, context)

    @app.post("/api/v1/feedback", status_code=201, tags=["feedback"])
    def submit_feedback(
        feedback: SimulationFeedback,
        context: TenantContextDep,
    ) -> dict[str, str]:
        store = get_feedback_store()
        record = FeedbackRecord(
            session_id=feedback.session_id,
            tenant_id=feedback.tenant_id or context.tenant_id,
            learner_id=feedback.learner_id or context.user_id or "learner_demo",
            satisfaction=feedback.satisfaction,
            perceived_realism=feedback.perceived_realism,
            difficulty=feedback.difficulty,
            usefulness=feedback.usefulness,
            would_use_for_training=feedback.would_use_for_training,
            free_text=feedback.free_text,
            submitted_at=datetime.now(UTC).isoformat(),
        )
        store.submit(record)
        _emit_product_event(
            "FeedbackSubmitted",
            tenant_id=record.tenant_id,
            session_id=record.session_id,
            metadata={"satisfaction": record.satisfaction, "would_use": record.would_use_for_training},
        )
        return {"status": "ok"}

    @app.get("/api/v1/feedback", tags=["feedback"])
    def list_feedback(
        context: TenantContextDep,
        limit: int = Query(default=50, le=200),
    ) -> list[FeedbackRecord]:
        return get_feedback_store().list(limit=limit)

    @app.get("/api/v1/feedback/summary", tags=["feedback"])
    def feedback_summary() -> dict:
        store = get_feedback_store()
        return {
            "count": store.count(),
            "average_satisfaction": round(store.average_satisfaction(), 1),
            "would_use_counts": store.count_would_use(),
        }

    @app.get("/api/v1/pilot/dashboard", response_model=PilotDashboard, tags=["pilot"])
    def pilot_dashboard(
        dashboard: PilotDashboardServiceDep,
    ) -> PilotDashboard:
        return dashboard.compute()

    @app.get("/api/v1/pilot/readiness", response_model=ReadinessResult, tags=["pilot"])
    def pilot_readiness(
        readiness: ReadinessServiceDep,
    ) -> ReadinessResult:
        return readiness.compute()

    class SystemCheckItem(BaseModel):
        name: str
        status: str  # "passed" | "warning" | "failed"
        label: str
        detail: str
        timing_ms: int = 0

    class SystemCheckResult(BaseModel):
        score: int
        ready: bool
        warnings: int
        checks: list[SystemCheckItem]

    @app.get("/api/v1/pilot/system-check", response_model=SystemCheckResult, tags=["pilot"])
    def pilot_system_check() -> SystemCheckResult:
        import os
        import time

        from openai import OpenAI

        def _check_llm_latency(api_key: str, base_url: str | None = None) -> int:
            try:
                client = OpenAI(api_key=api_key, base_url=base_url)
                t0 = time.perf_counter()
                client.models.list(timeout=5)
                return int((time.perf_counter() - t0) * 1000)
            except Exception:
                return -1

        checks: list[SystemCheckItem] = []
        warning_count = 0
        total_weight = 0
        passed_weight = 0

        # ── API ──────────────────────────────────────────────────────
        t0 = time.perf_counter()
        s = get_settings()
        api_ms = int((time.perf_counter() - t0) * 1000)
        checks.append(SystemCheckItem(
            name="api", status="passed",
            label="API Callibr",
            detail="API accessible",
            timing_ms=api_ms,
        ))
        total_weight += 25
        passed_weight += 25

        # ── LLM ──────────────────────────────────────────────────────
        has_openai = bool(s.openai_api_key)
        has_openrouter = bool(os.environ.get("OPENROUTER_API_KEY"))

        if has_openai:
            latency = _check_llm_latency(s.openai_api_key)  # type: ignore[arg-type]
            detail = f"OpenAI — {'⚠' if latency < 0 else f'{latency} ms'}"
            status = "passed" if latency > 0 else "warning"
            checks.append(SystemCheckItem(
                name="llm", status=status,
                label="Moteur IA (LLM)",
                detail=detail,
                timing_ms=latency if latency > 0 else 0,
            ))
        elif has_openrouter:
            latency = _check_llm_latency(
                os.environ["OPENROUTER_API_KEY"],
                base_url="https://openrouter.ai/api/v1",
            )
            detail = f"OpenRouter — {'⚠' if latency < 0 else f'{latency} ms'}"
            status = "passed" if latency > 0 else "warning"
            checks.append(SystemCheckItem(
                name="llm", status=status,
                label="Moteur IA (LLM)",
                detail=detail,
                timing_ms=latency if latency > 0 else 0,
            ))
        else:
            checks.append(SystemCheckItem(
                name="llm", status="warning",
                label="Moteur IA (LLM)",
                detail="Aucune clé API — réponses simulées",
                timing_ms=0,
            ))
            warning_count += 1
        total_weight += 25
        if checks[-1].status == "passed":
            passed_weight += 25

        # ── STT ──────────────────────────────────────────────────────
        if s.mock_stt:
            checks.append(SystemCheckItem(
                name="stt", status="passed",
                label="Reconnaissance vocale (STT)",
                detail="Mode simulation",
                timing_ms=0,
            ))
        elif os.environ.get("DEEPGRAM_API_KEY"):
            checks.append(SystemCheckItem(
                name="stt", status="passed",
                label="Reconnaissance vocale (STT)",
                detail="Deepgram — clé présente",
                timing_ms=0,
            ))
        else:
            checks.append(SystemCheckItem(
                name="stt", status="warning",
                label="Reconnaissance vocale (STT)",
                detail="Clé manquante — saisie texte",
                timing_ms=0,
            ))
            warning_count += 1
        total_weight += 25
        if checks[-1].status == "passed":
            passed_weight += 25

        # ── TTS ──────────────────────────────────────────────────────
        if s.mock_tts:
            checks.append(SystemCheckItem(
                name="tts", status="passed",
                label="Synthèse vocale (TTS)",
                detail="Mode simulation",
                timing_ms=0,
            ))
        elif os.environ.get("ELEVENLABS_API_KEY"):
            checks.append(SystemCheckItem(
                name="tts", status="passed",
                label="Synthèse vocale (TTS)",
                detail="ElevenLabs — clé présente",
                timing_ms=0,
            ))
        else:
            checks.append(SystemCheckItem(
                name="tts", status="warning",
                label="Synthèse vocale (TTS)",
                detail="Clé manquante — texte affiché",
                timing_ms=0,
            ))
            warning_count += 1
        total_weight += 25
        if checks[-1].status == "passed":
            passed_weight += 25

        score = int((passed_weight / total_weight) * 100) if total_weight else 0
        return SystemCheckResult(
            score=score,
            ready=warning_count == 0,
            warnings=warning_count,
            checks=checks,
        )

    @app.get("/api/v1/pilot/report/export", tags=["pilot"])
    def pilot_export_pdf(
        dashboard: DashboardServiceDep,
        readiness: ReadinessServiceDep,
    ) -> Response:
        data = dashboard.compute()
        readiness_result = readiness.compute()
        pdf_bytes = generate_pdf(data, readiness_result)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="callibr-executive-report-{datetime.now().strftime("%Y%m%d")}.pdf"',
            },
        )

    class IngestProductEvent(BaseModel):
        event_type: str
        tenant_id: str = "tenant_demo"
        scenario_id: str = ""
        session_id: str = ""
        duration: float = 0.0
        version: str = "0.1.0"
        timestamp: str = ""
        metadata: dict | None = None

    @app.post("/api/v1/product/events/ingest", status_code=204, tags=["product"])
    def ingest_product_event(event: IngestProductEvent) -> None:
        _emit_product_event(
            event_type=event.event_type,
            tenant_id=event.tenant_id,
            scenario_id=event.scenario_id,
            session_id=event.session_id,
            duration=event.duration,
            metadata=event.metadata,
        )

    @app.get("/api/v1/product/events", tags=["product"])
    def list_product_events(
        event_type: str | None = Query(None),
        limit: int = Query(default=100, le=500),
    ) -> list[ProductEvent]:
        store = get_product_event_store()
        return store.list(limit=limit, event_type=event_type)

    @app.get("/api/v1/product/events/counts", tags=["product"])
    def product_event_counts() -> dict[str, int]:
        return get_product_event_store().count_by_type()

    @app.get("/metrics", tags=["System"])
    async def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    app.include_router(conversation_router.router)
    app.include_router(persona_router.router)
    app.include_router(procedure_router.router)
    app.include_router(rule_router.router)
    app.include_router(scenario_router.router)
    app.include_router(voice_router.router)

    return app


app = create_app()
