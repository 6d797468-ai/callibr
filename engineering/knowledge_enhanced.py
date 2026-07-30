"""
Callibr Enhanced Knowledge Graph

Relie capabilities, tests, code, owners et packages.
Repond a des questions comme :
- "Quelle capability est la moins couverte par les tests ?"
- "Quels ADR sont impactes par la modification de X ?"
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CapabilityCoverage:
    capability: str
    has_code: bool
    has_contracts: bool
    has_tests: bool
    has_api: bool
    has_frontend: bool
    has_documentation: bool
    coverage_pct: float

    @property
    def status(self) -> str:
        if self.coverage_pct == 100:
            return "COMPLETE"
        elif self.coverage_pct >= 75:
            return "AVANCEE"
        elif self.coverage_pct >= 50:
            return "PARTIELLE"
        else:
            return "DEBUTANTE"


CAPABILITY_MAP = {
    "SIMULATION": {
        "code": ["engines/simulation/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/simulation.py"],
        "tests": ["tests/unit/test_simulation_service.py", "apps/api/tests/test_simulation_api.py"],
        "api": [
            "POST /api/v1/simulations",
            "GET /api/v1/simulations/{id}",
            "POST /api/v1/simulations/{id}/messages",
        ],
        "frontend": True,
    },
    "CRM": {
        "code": ["engines/crm/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/crm.py"],
        "tests": ["tests/unit/test_crm_action_service.py"],
        "api": [
            "GET /api/v1/simulations/{id}/crm/actions",
            "POST /api/v1/simulations/{id}/crm/actions",
        ],
        "frontend": True,
    },
    "EVALUATION": {
        "code": ["engines/evaluation/src"],
        "contracts": [],
        "tests": [],
        "api": ["GET /api/v1/simulations/{id}/report"],
        "frontend": True,
    },
    "SCENARIO": {
        "code": ["engines/scenario/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/scenario.py"],
        "tests": ["tests/unit/test_scenario_service.py"],
        "api": [
            "GET /api/v1/scenarios/engine",
            "POST /api/v1/scenarios/engine",
            "GET /api/v1/scenarios/engine/{id}",
            "POST /api/v1/scenarios/engine/{id}/validate",
            "POST /api/v1/scenarios/engine/{id}/compose",
            "POST /api/v1/scenarios/engine/launch",
        ],
        "frontend": False,
    },
    "IDENTITY": {
        "code": ["platform/identity/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/identity.py"],
        "tests": ["tests/unit/test_identity_provider.py"],
        "api": ["POST /api/v1/auth/login", "GET /api/v1/me"],
        "frontend": True,
    },
    "SESSION": {
        "code": ["engines/simulation/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/simulation.py"],
        "tests": ["tests/unit/test_simulation_service.py"],
        "api": ["GET /api/v1/simulations/{id}"],
        "frontend": True,
    },
    "ORCHESTRATION": {
        "code": ["packages/kernel/src"],
        "contracts": [],
        "tests": ["tests/unit/test_kernel.py"],
        "api": [],
        "frontend": False,
    },
    "MULTI-TENANT": {
        "code": ["packages/persistence/src"],
        "contracts": [],
        "tests": [],
        "api": [],
        "frontend": False,
    },
    "OBSERVABILITY": {
        "code": ["packages/telemetry/src"],
        "contracts": [],
        "tests": ["tests/unit/test_telemetry.py"],
        "api": [],
        "frontend": False,
    },
    "PROCEDURE": {
        "code": ["engines/procedure/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/procedure.py"],
        "tests": ["tests/unit/test_procedure_service.py"],
        "api": [
            "GET /api/v1/procedures",
            "POST /api/v1/procedures",
            "GET /api/v1/procedures/{id}",
            "POST /api/v1/procedures/{id}/executions",
            "GET /api/v1/procedures/{id}/executions",
            "GET /api/v1/procedures/executions/{id}",
            "POST /api/v1/procedures/executions/{id}/advance",
            "POST /api/v1/procedures/executions/{id}/fail",
            "POST /api/v1/procedures/executions/{id}/complete",
            "POST /api/v1/procedures/executions/{id}/abort",
        ],
        "frontend": False,
    },
    "PERSONA": {
        "code": ["engines/persona/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/persona.py"],
        "tests": ["tests/unit/test_persona_service.py"],
        "api": [
            "GET /api/v1/personas",
            "POST /api/v1/personas",
            "GET /api/v1/personas/{id}",
            "POST /api/v1/personas/{id}/validate",
            "POST /api/v1/personas/{id}/runtime",
            "POST /api/v1/personas/{id}/prompt-context",
        ],
        "frontend": False,
    },
    "RULE": {
        "code": ["engines/rule/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/rule.py"],
        "tests": ["tests/unit/test_rule_service.py"],
        "api": [
            "GET /api/v1/rules",
            "POST /api/v1/rules",
            "GET /api/v1/rules/{id}",
            "POST /api/v1/rules/{id}/validate",
            "POST /api/v1/rules/evaluate",
            "POST /api/v1/rules/explain",
        ],
        "frontend": False,
    },
    "CONVERSATION": {
        "code": ["engines/conversation/src"],
        "contracts": ["packages/contracts/src/callibr_contracts/conversation.py"],
        "tests": ["tests/unit/test_conversation_runtime.py"],
        "api": [
            "POST /api/v1/conversations",
            "POST /api/v1/conversations/{id}/messages",
            "GET /api/v1/conversations/{id}",
        ],
        "frontend": False,
    },
}


def compute_capability_coverage() -> list[CapabilityCoverage]:
    root = Path(".")
    results = []

    for cap_name, paths in CAPABILITY_MAP.items():
        has_code = any((root / p).exists() for p in paths["code"])
        has_contracts = any((root / p).exists() for p in paths["contracts"])
        has_tests = any((root / p).exists() for p in paths["tests"])
        has_api = len(paths["api"]) > 0
        has_frontend = paths["frontend"]
        has_doc = (root / "implementation" / "09-capabilities" / f"{cap_name}.md").exists()

        dimensions = [has_code, has_contracts, has_tests, has_api, has_frontend, has_doc]
        coverage = (sum(dimensions) / len(dimensions)) * 100

        results.append(
            CapabilityCoverage(
                capability=cap_name,
                has_code=has_code,
                has_contracts=has_contracts,
                has_tests=has_tests,
                has_api=has_api,
                has_frontend=has_frontend,
                has_documentation=has_doc,
                coverage_pct=round(coverage, 1),
            )
        )

    results.sort(key=lambda x: x.coverage_pct)
    return results


def find_adrs_for_package(package_path: str) -> list[str]:
    adr_map = {
        "packages/persistence": ["ADR-0001 PostgreSQL", "ADR-0007 Alembic"],
        "apps/api": ["ADR-0002 FastAPI"],
        "packages/contracts": ["ADR-0006 Pydantic"],
        "packages/kernel": ["ADR-0003 Hexagonal", "ADR-0004 Monorepo"],
    }
    for prefix, adrs in adr_map.items():
        if prefix in package_path:
            return adrs
    return ["ADR-0003 Hexagonal", "ADR-0004 Monorepo"]


def find_least_covered_capability() -> CapabilityCoverage | None:
    coverages = compute_capability_coverage()
    if coverages:
        return coverages[0]
    return None
