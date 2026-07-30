"""
Callibr Intelligent Diagnostics

Chaque diagnostic fournit :
- pourquoi le probleme existe
- ou il se trouve exactement
- a quelle regle il se rattache
- quel est son impact
- comment le corriger
"""

from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    CRITICAL = "CRITIQUE"
    HIGH = "HAUTE"
    MEDIUM = "MOYENNE"
    LOW = "BASSE"


class Category(Enum):
    ARCHITECTURE = "architecture"
    SECURITY = "securite"
    QUALITY = "qualite"
    DEBT = "dette"
    INFRASTRUCTURE = "infrastructure"
    FUNCTIONAL = "fonctionnel"


@dataclass
class Diagnostic:
    check_id: str
    passed: bool
    severity: Severity
    category: Category
    title: str
    cause: str
    location: str
    rule_reference: str
    capability: str
    impact: str
    fix_proposal: str
    auto_fixable: bool = False
    details: str = ""


def diagnostic_architecture_layers() -> list[Diagnostic]:
    import ast
    from pathlib import Path

    ROOT = Path(".")
    diagnostics = []

    domain_dirs = [
        ROOT / "packages" / "kernel" / "src",
        ROOT / "packages" / "contracts" / "src",
    ]
    for engine_dir in (ROOT / "engines").iterdir():
        if engine_dir.is_dir() and (engine_dir / "src").exists():
            domain_dirs.append(engine_dir / "src")

    for domain_dir in domain_dirs:
        if not domain_dir.exists():
            continue
        for py_file in domain_dir.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text())
                for node in ast.walk(tree):
                    module = None
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            module = alias.name
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module

                    if module and (
                        "callibr_persistence" in module
                        or "callibr_identity" in module
                        or "callibr_api" in module
                    ):
                        diagnostics.append(
                            Diagnostic(
                                check_id="chk-arch-layers",
                                passed=False,
                                severity=Severity.CRITICAL,
                                category=Category.ARCHITECTURE,
                                title=f"Violation architecturale dans {py_file.name}",
                                cause=(
                                    f"Le module domaine '{py_file.parent.parent.name}' importe"
                                    f" '{module.split('.')[0]}', qui est un module infrastructure."
                                    " En architecture hexagonale, le domaine ne doit jamais"
                                    " dependre de l'infrastructure."
                                ),
                                location=str(py_file),
                                rule_reference="ADR-0003 (Architecture Hexagonale) / AEB D03",
                                capability="ORCHESTRATION",
                                impact=(
                                    "Couplage domain → infrastructure. Rend impossible le"
                                    " remplacement de l'infrastructure sans impacter le domaine."
                                ),
                                fix_proposal=(
                                    "Introduire un port (interface) dans le package"
                                    " kernel ou contracts. L'adapter d'infrastructure"
                                    " doit implementer ce port. Le domaine depend du"
                                    " port, pas de l'adapter."
                                ),
                                auto_fixable=False,
                            )
                        )
            except Exception:
                pass

    return diagnostics


def diagnostic_tenant_isolation() -> list[Diagnostic]:
    from pathlib import Path

    ROOT = Path(".")
    diagnostics = []

    store_patterns = ["store", "repository"]
    for py_file in ROOT.rglob("*.py"):
        if (
            "node_modules" in str(py_file)
            or ".venv" in str(py_file)
            or "engineering" in str(py_file)
        ):
            continue

        is_store = any(p in py_file.name.lower() for p in store_patterns)
        if not is_store:
            continue

        try:
            content = py_file.read_text()
            if (
                "tenant_id" not in content
                and "TenantContext" not in content
                and "test" not in str(py_file)
            ):
                diagnostics.append(
                    Diagnostic(
                        check_id="chk-tenant-isolation",
                        passed=False,
                        severity=Severity.CRITICAL,
                        category=Category.SECURITY,
                        title=f"Isolation de tenant non verifiee dans {py_file.name}",
                        cause=(
                            f"Le fichier '{py_file}' ne contient aucune reference"
                            " a tenant_id ou TenantContext. Dans une architecture"
                            " multi-tenant SaaS, chaque store doit filtrer par"
                            " tenant_id."
                        ),
                        location=str(py_file),
                        rule_reference="ADR-0001 (PostgreSQL) / AEB C03 / AEB I02",
                        capability="MULTI-TENANT",
                        impact=(
                            "Risque de fuite de donnees inter-tenant. "
                            "Un utilisateur pourrait lire les donnees d'un autre tenant."
                        ),
                        fix_proposal=(
                            "1. Ajouter un parametre tenant_id a chaque methode du store.\n"
                            "2. Filtrer les requetes avec WHERE tenant_id = :tenant_id.\n"
                            "3. Pour PostgreSQL, envisager Row Level Security (RLS)."
                        ),
                        auto_fixable=False,
                    )
                )
        except Exception:
            pass

    return diagnostics


def diagnostic_incomplete_implementations() -> list[Diagnostic]:
    from pathlib import Path

    ROOT = Path(".")
    diagnostics = []

    for py_file in ROOT.rglob("*.py"):
        if (
            "node_modules" in str(py_file)
            or ".venv" in str(py_file)
            or "engineering" in str(py_file)
        ):
            continue

        try:
            content = py_file.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("raise NotImplementedError"):
                    diagnostics.append(
                        Diagnostic(
                            check_id="chk-pass",
                            passed=False,
                            severity=Severity.MEDIUM,
                            category=Category.DEBT,
                            title=f"Implementation incomplete dans {py_file.name}:{i}",
                            cause=(
                                f"La ligne {i} contient 'raise NotImplementedError'. "
                                "Cela indique une interface ou methode non implementee."
                            ),
                            location=f"{py_file}:{i}",
                            rule_reference="Implementation Principles #7 (Pas de dette volontaire)",
                            capability="ORCHESTRATION",
                            impact="Le composant ne peut pas etre utilise en production.",
                            fix_proposal=(
                                "Implementer la methode ou la supprimer si non necessaire."
                            ),
                            auto_fixable=False,
                        )
                    )
        except Exception:
            pass

    return diagnostics


def diagnostic_missing_migrations() -> list[Diagnostic]:
    from pathlib import Path

    alembic_dir = Path("infrastructure/postgres/alembic")
    if not alembic_dir.exists():
        return [
            Diagnostic(
                check_id="chk-migrations",
                passed=False,
                severity=Severity.HIGH,
                category=Category.INFRASTRUCTURE,
                title="Dossier Alembic absent",
                cause=(
                    "Le projet utilise PostgreSQL mais n'a pas de systeme de migrations Alembic. "
                    "Le schema est gere via un fichier SQL brut (001_runtime_state.sql)."
                ),
                location="infrastructure/postgres/",
                rule_reference="ADR-0007 (Alembic) / AEB D02",
                capability="MULTI-TENANT",
                impact=(
                    "Les changements de schema ne sont pas versionnes. "
                    "Risque de drift entre environnements. "
                    "Pas de rollback possible."
                ),
                fix_proposal=(
                    "1. Initialiser Alembic : alembic init infrastructure/postgres/alembic\n"
                    "2. Generer la premiere migration depuis le schema existant.\n"
                    "3. Integrer les migrations dans le pipeline CI/CD."
                ),
                auto_fixable=False,
            )
        ]
    return []


def diagnostic_capability_completeness() -> list[Diagnostic]:
    from pathlib import Path

    ROOT = Path(".")
    diagnostics = []

    capability_map = {
        "SIMULATION": {
            "code_paths": ["engines/simulation/src"],
            "contract_paths": ["packages/contracts/src/callibr_contracts/simulation.py"],
            "test_paths": [
                "tests/unit/test_simulation_service.py",
                "apps/api/tests/test_simulation_api.py",
            ],
        },
        "CRM": {
            "code_paths": ["engines/crm/src"],
            "contract_paths": ["packages/contracts/src/callibr_contracts/crm.py"],
            "test_paths": ["tests/unit/test_crm_action_service.py"],
        },
        "EVALUATION": {
            "code_paths": ["engines/evaluation/src"],
            "contract_paths": [],
            "test_paths": [],
        },
        "SCENARIO": {
            "code_paths": ["engines/scenario/src"],
            "contract_paths": [],
            "test_paths": [],
        },
        "IDENTITY": {
            "code_paths": ["platform/identity/src"],
            "contract_paths": ["packages/contracts/src/callibr_contracts/identity.py"],
            "test_paths": ["tests/unit/test_identity_provider.py"],
        },
    }

    for cap_name, paths in capability_map.items():
        missing = []
        for code_path in paths["code_paths"]:
            if not (ROOT / code_path).exists():
                missing.append(f"code: {code_path}")
            elif not any((ROOT / code_path).rglob("*.py")):
                missing.append(f"code vide: {code_path}")

        for contract_path in paths["contract_paths"]:
            if not (ROOT / contract_path).exists():
                missing.append(f"contrat: {contract_path}")

        for test_path in paths["test_paths"]:
            if not (ROOT / test_path).exists():
                missing.append(f"test: {test_path}")

        if missing:
            diagnostics.append(
                Diagnostic(
                    check_id="chk-capabilities",
                    passed=False,
                    severity=Severity.HIGH,
                    category=Category.FUNCTIONAL,
                    title=f"Capability {cap_name} incomplète",
                    cause=(
                        f"La capability {cap_name} n'a pas tous ses composants. "
                        f"Manquant : {', '.join(missing)}."
                    ),
                    location=", ".join(missing),
                    rule_reference=f"Capability Catalog — {cap_name}",
                    capability=cap_name,
                    impact="La capability n'est pas utilisable de bout en bout.",
                    fix_proposal=f"Creer les composants manquants pour {cap_name}.",
                    auto_fixable=False,
                )
            )

    return diagnostics


ALL_DIAGNOSTICS = [
    diagnostic_architecture_layers,
    diagnostic_tenant_isolation,
    diagnostic_incomplete_implementations,
    diagnostic_missing_migrations,
    diagnostic_capability_completeness,
]


def run_all_diagnostics() -> list[Diagnostic]:
    diagnostics = []
    for func in ALL_DIAGNOSTICS:
        diagnostics.extend(func())
    return diagnostics
