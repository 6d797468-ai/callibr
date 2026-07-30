"""
Callibr Health Checks

Chaque check retourne un CheckResult.
"""

import subprocess
import sys
from pathlib import Path

from engineering.types import CheckResult

EXCLUDE_DIRS = {"node_modules", ".venv", "engineering", "__pycache__", ".git"}


def _should_scan(path: Path) -> bool:
    return all(part not in EXCLUDE_DIRS for part in path.parts)


def check_lint() -> CheckResult:
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "apps", "packages", "platform", "engines", "tests"],
        capture_output=True,
        text=True,
    )
    return CheckResult(
        name="lint",
        passed=result.returncode == 0,
        message="Lint OK" if result.returncode == 0 else "Erreurs de lint",
        details=result.stderr[:500] if result.returncode != 0 else "",
    )


def check_tests() -> CheckResult:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--tb=short", "-q"],
        capture_output=True,
        text=True,
    )
    return CheckResult(
        name="tests",
        passed=result.returncode == 0,
        message="Tests OK" if result.returncode == 0 else "Tests en echec",
        details=result.stdout[-500:] if result.returncode != 0 else "",
    )


def check_typage() -> CheckResult:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--ignore-missing-imports",
            "packages/",
            "platform/",
            "engines/",
        ],
        capture_output=True,
        text=True,
    )
    return CheckResult(
        name="typage",
        passed=result.returncode == 0,
        message="Typage OK" if result.returncode == 0 else "Erreurs de typage",
        details=result.stdout[-500:] if result.returncode != 0 else "",
    )


def check_todos() -> CheckResult:
    root = Path(".")
    todos = []
    for py_file in root.rglob("*.py"):
        if not _should_scan(py_file):
            continue
        try:
            content = py_file.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                if "TODO" in line and not line.strip().startswith("#"):
                    todos.append(f"{py_file}:{i}: {line.strip()}")
        except Exception:
            pass
    if todos:
        return CheckResult(
            name="todos",
            passed=False,
            message=f"{len(todos)} TODO trouves",
            details="\n".join(todos[:10]),
        )
    return CheckResult(name="todos", passed=True, message="Pas de TODO")


def check_pass_statements() -> CheckResult:
    root = Path(".")
    passes = []
    for py_file in root.rglob("*.py"):
        if not _should_scan(py_file):
            continue
        try:
            content = py_file.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped == "pass" or stripped.startswith("raise NotImplementedError"):
                    passes.append(f"{py_file}:{i}: {stripped}")
        except Exception:
            pass
    if passes:
        return CheckResult(
            name="pass_statements",
            passed=False,
            message=f"{len(passes)} pass/NotImplementedError trouves",
            details="\n".join(passes[:10]),
        )
    return CheckResult(
        name="pass_statements", passed=True, message="Pas de pass/NotImplementedError"
    )


def check_migrations() -> CheckResult:
    alembic_dir = Path("infrastructure/postgres/alembic")
    if not alembic_dir.exists():
        return CheckResult(
            name="migrations",
            passed=False,
            message="Dossier Alembic non trouve",
            details="Creer infrastructure/postgres/alembic/",
        )
    versions = (
        list((alembic_dir / "versions").glob("*.py")) if (alembic_dir / "versions").exists() else []
    )
    return CheckResult(
        name="migrations",
        passed=True,
        message=f"{len(versions)} migrations",
    )


def check_contracts() -> CheckResult:
    contracts_dir = Path("packages/contracts/src/callibr_contracts")
    if not contracts_dir.exists():
        return CheckResult(
            name="contracts",
            passed=False,
            message="Dossier contracts non trouve",
        )
    py_files = list(contracts_dir.glob("*.py"))
    return CheckResult(
        name="contracts",
        passed=True,
        message=f"{len(py_files)} fichiers de contrats",
    )


def check_capabilities() -> CheckResult:
    cap_dir = Path("implementation/09-capabilities")
    if not cap_dir.exists():
        return CheckResult(
            name="capabilities",
            passed=False,
            message="Dossier capabilities non trouve",
        )
    md_files = list(cap_dir.glob("*.md"))
    return CheckResult(
        name="capabilities",
        passed=True,
        message=f"{len(md_files)} capabilities documentees",
    )


def check_adr() -> CheckResult:
    adr_dir = Path("adr")
    if not adr_dir.exists():
        return CheckResult(
            name="adr",
            passed=False,
            message="Dossier ADR non trouve",
        )
    adr_files = list(adr_dir.glob("ADR-*.md"))
    return CheckResult(
        name="adr",
        passed=True,
        message=f"{len(adr_files)} ADRs",
    )


def check_security() -> CheckResult:
    root = Path(".")
    secrets = []
    secret_patterns = ["password", "secret", "api_key", "token"]
    for py_file in root.rglob("*.py"):
        if not _should_scan(py_file):
            continue
        try:
            content = py_file.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                for pattern in secret_patterns:
                    if (
                        (f'"{pattern}"' in line.lower() or f"'{pattern}'" in line.lower())
                        and "example" not in line.lower()
                        and "test" not in str(py_file)
                    ):
                        secrets.append(f"{py_file}:{i}: {line.strip()[:80]}")
        except Exception:
            pass
    if secrets:
        return CheckResult(
            name="security",
            passed=False,
            message=f"{len(secrets)} secrets potentiels",
            details="\n".join(secrets[:5]),
        )
    return CheckResult(name="security", passed=True, message="Pas de secrets detectes")


def check_api_endpoints() -> CheckResult:
    api_dir = Path("apps/api/src/callibr_api")
    if not api_dir.exists():
        return CheckResult(
            name="api_endpoints",
            passed=False,
            message="Dossier API non trouve",
        )
    py_files = list(api_dir.rglob("*.py"))
    return CheckResult(
        name="api_endpoints",
        passed=True,
        message=f"{len(py_files)} fichiers API",
    )


def check_tenant_isolation() -> CheckResult:
    root = Path(".")
    missing_tenant = []
    for py_file in root.rglob("*.py"):
        if "node_modules" in str(py_file) or ".venv" in str(py_file):
            continue
        if "store" in str(py_file) or "repository" in str(py_file):
            try:
                content = py_file.read_text()
                if (
                    "tenant_id" not in content
                    and "TenantContext" not in content
                    and "test" not in str(py_file)
                ):
                    missing_tenant.append(str(py_file))
            except Exception:
                pass
    if missing_tenant:
        return CheckResult(
            name="tenant_isolation",
            passed=False,
            message=f"{len(missing_tenant)} stores sans tenant_id",
            details="\n".join(missing_tenant[:5]),
        )
    return CheckResult(name="tenant_isolation", passed=True, message="Tenant ID present")


def check_dod() -> CheckResult:
    dod_file = Path("implementation/DEFINITION-OF-DONE.md")
    if not dod_file.exists():
        return CheckResult(
            name="dod",
            passed=False,
            message="Definition of Done non trouvee",
        )
    return CheckResult(name="dod", passed=True, message="Definition of Done presente")


def check_principles() -> CheckResult:
    principles_file = Path("implementation/IMPLEMENTATION-PRINCIPLES.md")
    if not principles_file.exists():
        return CheckResult(
            name="principles",
            passed=False,
            message="Implementation Principles non trouve",
        )
    return CheckResult(name="principles", passed=True, message="Implementation Principles present")


def check_workflow() -> CheckResult:
    workflow_file = Path("implementation/IMPLEMENTATION-WORKFLOW.md")
    if not workflow_file.exists():
        return CheckResult(
            name="workflow",
            passed=False,
            message="Implementation Workflow non trouve",
        )
    return CheckResult(name="workflow", passed=True, message="Implementation Workflow present")


def check_secret_scan() -> CheckResult:
    from engineering.checks.secret_scan import scan_secrets

    result = scan_secrets()
    if result.passed:
        return CheckResult(
            name="secret_scan",
            passed=True,
            message=f"Aucun secret detecte dans {result.scanned_files} fichiers",
        )

    lines = [
        f"  {f.path}:{f.line} [{f.pattern_name}] (entropy={f.entropy})"
        for f in result.findings[:10]
    ]
    if len(result.findings) > 10:
        lines.append(f"  ... et {len(result.findings) - 10} autre(s)")
    return CheckResult(
        name="secret_scan",
        passed=False,
        message=f"{len(result.findings)} secret(s) detecte(s) dans {result.scanned_files} fichiers",
        details="\n".join(lines),
    )


CHECKS = {
    "lint": check_lint,
    "tests": check_tests,
    "typage": check_typage,
    "todos": check_todos,
    "pass_statements": check_pass_statements,
    "migrations": check_migrations,
    "contracts": check_contracts,
    "capabilities": check_capabilities,
    "adr": check_adr,
    "security": check_security,
    "secret_scan": check_secret_scan,
    "api_endpoints": check_api_endpoints,
    "tenant_isolation": check_tenant_isolation,
    "dod": check_dod,
    "principles": check_principles,
    "workflow": check_workflow,
}
