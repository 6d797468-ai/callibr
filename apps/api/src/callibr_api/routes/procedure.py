from __future__ import annotations

from typing import Annotated

from callibr_api.dependencies import get_procedure_service
from callibr_contracts import (
    AdvanceProcedureRequest,
    ProcedureDefinition,
    ProcedureExecution,
    ProcedureSummary,
    StartProcedureRequest,
)
from callibr_procedure import ProcedureService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/procedures", tags=["Procedures"])


@router.get("")
def list_procedures(
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> list[ProcedureSummary]:
    return service.list_procedures()


@router.post("", status_code=201)
def define_procedure(
    definition: ProcedureDefinition,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureDefinition:
    return service.define(definition)


@router.get("/{procedure_id}")
def get_procedure(
    procedure_id: str,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureDefinition:
    return service.get_procedure(procedure_id)


@router.post("/{procedure_id}/executions", status_code=201)
def start_execution(
    procedure_id: str,
    request: StartProcedureRequest,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureExecution:
    return service.start(request.model_copy(update={"procedure_id": procedure_id}))


@router.get("/{procedure_id}/executions")
def list_executions(
    procedure_id: str,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> list[ProcedureExecution]:
    return service.list_executions(procedure_id)


@router.get("/executions/{execution_id}")
def get_execution(
    execution_id: str,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureExecution:
    return service.get_execution(execution_id)


@router.post("/executions/{execution_id}/advance")
def advance_execution(
    execution_id: str,
    request: AdvanceProcedureRequest,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureExecution:
    return service.advance(execution_id, request)


@router.post("/executions/{execution_id}/fail")
def fail_execution(
    execution_id: str,
    step_id: str,
    error: str,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureExecution:
    return service.fail(execution_id, step_id, error)


@router.post("/executions/{execution_id}/complete")
def complete_execution(
    execution_id: str,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
    score: int | None = None,
) -> ProcedureExecution:
    return service.complete(execution_id, score)


@router.post("/executions/{execution_id}/abort")
def abort_execution(
    execution_id: str,
    service: Annotated[ProcedureService, Depends(get_procedure_service)],
) -> ProcedureExecution:
    return service.abort(execution_id)
