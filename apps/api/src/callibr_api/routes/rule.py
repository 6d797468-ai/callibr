from __future__ import annotations

from typing import Annotated

from callibr_api.dependencies import get_rule_service
from callibr_contracts import (
    ExecutionContext,
    RuleDefinition,
    RuleEvaluation,
    RuleExplainResult,
    ValidateRuleResult,
)
from callibr_rule import RuleService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/rules", tags=["Rule Engine"])


@router.get("")
def list_rules(
    service: Annotated[RuleService, Depends(get_rule_service)],
) -> list[RuleDefinition]:
    return service.list()


@router.post("", status_code=201)
def define_rule(
    definition: RuleDefinition,
    service: Annotated[RuleService, Depends(get_rule_service)],
) -> RuleDefinition:
    return service.define(definition)


@router.get("/{rule_id}")
def get_rule(
    rule_id: str,
    service: Annotated[RuleService, Depends(get_rule_service)],
) -> RuleDefinition:
    return service.get(rule_id)


@router.post("/{rule_id}/validate")
def validate_rule(
    rule_id: str,
    service: Annotated[RuleService, Depends(get_rule_service)],
) -> ValidateRuleResult:
    return service.validate(rule_id)


@router.post("/evaluate")
def evaluate_rules(
    service: Annotated[RuleService, Depends(get_rule_service)],
    rule_ids: list[str] | None = None,
    context: ExecutionContext | None = None,
) -> RuleEvaluation:
    return service.evaluate(rules=rule_ids, context=context)


@router.post("/explain")
def explain_rules(
    service: Annotated[RuleService, Depends(get_rule_service)],
    rule_ids: list[str] | None = None,
    context: ExecutionContext | None = None,
) -> RuleExplainResult:
    return service.explain(rules=rule_ids, context=context)
