"""Prometheus metrics definitions for Callibr."""

from __future__ import annotations

from prometheus_client import Counter, Histogram

# --- Technical Metrics ---

http_requests_total = Counter(
    "callibr_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

http_request_duration_seconds = Histogram(
    "callibr_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# --- Business Metrics ---

llm_tokens_total = Counter(
    "callibr_llm_tokens_total",
    "Total number of tokens consumed by LLM generation",
    ["model", "token_type"],  # token_type: "prompt" or "completion"
)

simulations_started_total = Counter(
    "callibr_simulations_started_total",
    "Total number of simulation sessions started",
    ["tenant_id", "scenario_id"],
)

# --- AI Runtime Metrics ---

llm_routing_total = Counter(
    "callibr_llm_routing_total",
    "LLM routing decisions",
    ["provider", "model", "selected"],
)

safety_validation_total = Counter(
    "callibr_safety_validation_total",
    "Safety validation results",
    ["direction", "verdict"],
)

budget_evaluation_total = Counter(
    "callibr_budget_evaluation_total",
    "Token budget evaluation results",
    ["within_budget"],
)

context_reduction_total = Counter(
    "callibr_context_reduction_total",
    "Context reduction events",
    ["reduced"],
)

validation_results_total = Counter(
    "callibr_validation_results_total",
    "Response validation results (valid/rejected/regenerated)",
    ["valid", "regenerate", "violation_codes"],
)
