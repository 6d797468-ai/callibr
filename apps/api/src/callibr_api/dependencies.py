from __future__ import annotations

import logging
from functools import lru_cache
from typing import Annotated, Any

from callibr_contracts import LLMAdapter, LLMRouter, TokenBudget
from callibr_conversation import (
    CapabilityBasedRouter,
    ConversationService,
    DeterministicSafetyValidator,
    DeterministicTokenCounter,
    MockAdapter,
    OpenAIAdapter,
    PriorityContextReducer,
    ProviderRegistry,
    TokenBudgetEvaluator,
)
from callibr_crm import CrmActionService
from callibr_evaluation import EvaluationService
from callibr_identity import DemoIdentityProvider
from callibr_kernel import EventBus, TenantContext, new_trace_id
from callibr_persistence import (
    InMemoryAuditEventStore,
    InMemoryConversationStore,
    InMemoryIdentityStore,
    InMemoryPersonaDefinitionStore,
    InMemoryProcedureStore,
    InMemoryRuleStore,
    InMemoryScenarioDefinitionStore,
    InMemoryTransactionManager,
    PostgresAuditEventStore,
    PostgresConversationStore,
    PostgresIdentityStore,
    PostgresPersonaDefinitionStore,
    PostgresProcedureStore,
    PostgresRuleStore,
    PostgresScenarioDefinitionStore,
    PostgresTransactionManager,
)
from callibr_persistence.providers.base import PersistenceProvider
from callibr_persistence.providers.factory import PersistenceFactory
from callibr_persona import (
    PersonaRegistry,
    PersonaService,
    PersonaValidator,
)
from callibr_procedure import ProcedureService
from callibr_procedure.executor import ProcedureExecutor
from callibr_procedure.registry import ProcedureRegistry
from callibr_rule import (
    RuleRegistry,
    RuleService,
    RuleValidator,
)
from callibr_scenario import (
    InMemoryScenarioRepository,
    ScenarioService,
    ScenarioValidator,
)
from callibr_scenario import (
    ScenarioRegistry as ScenarioDefRegistry,
)
from callibr_simulation import SimulationService
from callibr_telemetry.dashboard import DashboardService
from callibr_telemetry.pilot import PilotDashboardService
from callibr_telemetry.readiness import PilotReadinessService
from fastapi import Header, Request

from callibr_api.config import get_settings

log = logging.getLogger(__name__)


@lru_cache
def get_event_bus() -> EventBus:
    return EventBus()


@lru_cache
def get_audit_event_store() -> InMemoryAuditEventStore:
    settings = get_settings()
    if settings.persistence_backend.lower() == "postgres":
        store = PostgresAuditEventStore(settings.database_url)
        store.init_schema()
        return store
    return InMemoryAuditEventStore()


@lru_cache
def get_procedure_registry() -> ProcedureRegistry:
    return ProcedureRegistry()


@lru_cache
def get_procedure_executor() -> ProcedureExecutor:
    return ProcedureExecutor()


@lru_cache
def get_procedure_store() -> PostgresProcedureStore | InMemoryProcedureStore:
    settings = get_settings()

    if settings.persistence_backend.lower() == "postgres":
        return PostgresProcedureStore(settings.database_url)
    return InMemoryProcedureStore()


@lru_cache
def get_procedure_service() -> ProcedureService:
    return ProcedureService(
        registry=get_procedure_registry(),
        executor=get_procedure_executor(),
        store=get_procedure_store(),
        audit_event_store=get_audit_event_store(),
        event_bus=get_event_bus(),
    )


@lru_cache
def get_scenario_service() -> ScenarioService:
    settings = get_settings()

    scenario_registry = ScenarioDefRegistry()
    validator = ScenarioValidator(
        procedure_registry=get_procedure_registry(),
        procedure_store=get_procedure_store(),
    )

    store = (
        PostgresScenarioDefinitionStore(settings.database_url)
        if settings.persistence_backend.lower() == "postgres"
        else InMemoryScenarioDefinitionStore()
    )

    return ScenarioService(
        registry=scenario_registry,
        validator=validator,
        store=store,
        procedure_service=get_procedure_service(),
        audit_event_store=get_audit_event_store(),
        event_bus=get_event_bus(),
    )


@lru_cache
def get_persona_service() -> PersonaService:
    settings = get_settings()

    registry = PersonaRegistry()
    validator = PersonaValidator()

    store = (
        PostgresPersonaDefinitionStore(settings.database_url)
        if settings.persistence_backend.lower() == "postgres"
        else InMemoryPersonaDefinitionStore()
    )

    return PersonaService(
        registry=registry,
        validator=validator,
        store=store,
        audit_event_store=get_audit_event_store(),
        event_bus=get_event_bus(),
    )


@lru_cache
def get_rule_service() -> RuleService:
    settings = get_settings()

    registry = RuleRegistry()
    validator = RuleValidator()

    store = (
        PostgresRuleStore(settings.database_url)
        if settings.persistence_backend.lower() == "postgres"
        else InMemoryRuleStore()
    )

    return RuleService(
        registry=registry,
        validator=validator,
        store=store,
        audit_event_store=get_audit_event_store(),
        event_bus=get_event_bus(),
    )


@lru_cache
def get_llm_adapter() -> LLMAdapter:
    settings = get_settings()
    if settings.openai_api_key:
        log.info("LLM Adapter: OpenAIAdapter (model=%s)", settings.openai_model)
        return OpenAIAdapter(api_key=settings.openai_api_key, model=settings.openai_model)

    log.warning("LLM Adapter: No OpenAI API key provided, falling back to MockAdapter.")
    return MockAdapter()


@lru_cache
def get_transaction_manager() -> PostgresTransactionManager | InMemoryTransactionManager:
    settings = get_settings()
    if settings.persistence_backend.lower() == "postgres":
        return PostgresTransactionManager(settings.database_url)
    return InMemoryTransactionManager()


@lru_cache
def get_conversation_store() -> PostgresConversationStore | InMemoryConversationStore:
    settings = get_settings()
    if settings.persistence_backend.lower() == "postgres":
        store = PostgresConversationStore(settings.database_url)
        store.init_schema()
        return store
    return InMemoryConversationStore()


@lru_cache
def get_token_budget() -> TokenBudget:
    return TokenBudget(
        context_window=8_192,
        reserved_output_tokens=1_024,
        safety_margin_tokens=256,
    )


@lru_cache
def get_provider_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    mock = MockAdapter()
    registry.register(
        model_id="mock",
        adapter=mock,
    )
    settings = get_settings()
    if settings.openai_api_key:
        openai_adapter = OpenAIAdapter(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )
        registry.register(
            model_id=settings.openai_model,
            adapter=openai_adapter,
        )
    return registry


@lru_cache
def get_llm_router() -> LLMRouter:
    return CapabilityBasedRouter(registry=get_provider_registry())


@lru_cache
def get_budget_evaluator() -> TokenBudgetEvaluator:
    counter = DeterministicTokenCounter()
    return TokenBudgetEvaluator(counter)


@lru_cache
def get_context_reducer() -> PriorityContextReducer:
    return PriorityContextReducer()


@lru_cache
def get_safety_validator() -> DeterministicSafetyValidator:
    return DeterministicSafetyValidator()


@lru_cache
def get_conversation_service() -> ConversationService:
    settings = get_settings()

    kwargs: dict[str, Any] = {
        "scenario_service": get_scenario_service(),
        "procedure_service": get_procedure_service(),
        "persona_service": get_persona_service(),
        "rule_service": get_rule_service(),
        "evaluation_service": EvaluationService(),
        "crm_service": CrmActionService(),
        "event_bus": get_event_bus(),
        "transaction_manager": get_transaction_manager(),
        "conversation_store": get_conversation_store(),
        "llm_adapter": get_llm_adapter(),
    }

    if settings.ai_runtime_budget_enabled:
        kwargs["budget_evaluator"] = get_budget_evaluator()
        kwargs["token_budget"] = get_token_budget()

    if settings.ai_runtime_safety_enabled:
        kwargs["safety_validator"] = get_safety_validator()

    if settings.ai_runtime_reduction_enabled:
        kwargs["context_reducer"] = get_context_reducer()

    if settings.ai_runtime_routing_enabled:
        kwargs["llm_router"] = get_llm_router()

    return ConversationService(**kwargs)


@lru_cache
def get_persistence_provider() -> PersistenceProvider:
    settings = get_settings()
    provider = PersistenceFactory.create(
        settings.persistence_backend.lower(),
        settings.database_url,
    )
    if settings.persistence_backend.lower() == "postgres":
        provider.init_schema()
    return provider


@lru_cache
def get_session_store():
    return get_persistence_provider().simulation_store


@lru_cache
def get_feedback_store():
    return get_persistence_provider().feedback_store


@lru_cache
def get_product_event_store():
    return get_persistence_provider().analytics_store


@lru_cache
def get_simulation_service() -> SimulationService:
    scenario_repo = InMemoryScenarioRepository()
    crm_service = CrmActionService()
    evaluation_service = EvaluationService()
    event_bus = get_event_bus()
    session_store = get_session_store()
    return SimulationService(
        scenario_repository=scenario_repo,
        crm_action_service=crm_service,
        evaluation_service=evaluation_service,
        session_store=session_store,
        audit_event_store=get_audit_event_store(),
        event_bus=event_bus,
        conversation_service=get_conversation_service(),
    )


@lru_cache
def get_identity_provider() -> DemoIdentityProvider:
    settings = get_settings()
    if settings.persistence_backend.lower() == "postgres":
        identity_store = PostgresIdentityStore(settings.database_url)
        identity_store.init_schema()
    else:
        identity_store = InMemoryIdentityStore()
    return DemoIdentityProvider(
        tenant_id=settings.demo_tenant_id,
        environment=settings.env,
        demo_user_email=settings.demo_user_email,
        demo_user_password=settings.demo_user_password,
        auth_secret=settings.auth_secret,
        token_ttl_seconds=settings.auth_token_ttl_seconds,
        identity_store=identity_store,
    )


def get_tenant_context(
    request: Request,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    x_trace_id: Annotated[str | None, Header(alias="X-Trace-Id")] = None,
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> TenantContext:
    settings = get_settings()
    trace_id = x_trace_id or getattr(request.state, "trace_id", None) or new_trace_id()
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        user = get_identity_provider().authenticate_token(token, trace_id)
        return TenantContext(
            tenant_id=user.tenant_id,
            user_id=user.user_id,
            trace_id=trace_id,
        )
    return TenantContext(
        tenant_id=x_tenant_id or settings.demo_tenant_id,
        user_id=x_user_id or "learner_demo",
        trace_id=trace_id,
    )


@lru_cache
def get_dashboard_service() -> DashboardService:
    return DashboardService(
        get_session_store(),
        get_feedback_store(),
        get_product_event_store(),
    )


@lru_cache
def get_pilot_dashboard_service() -> PilotDashboardService:
    return PilotDashboardService(
        get_session_store(),
        get_feedback_store(),
        get_product_event_store(),
    )


@lru_cache
def get_readiness_service() -> PilotReadinessService:
    return PilotReadinessService(get_dashboard_service())
