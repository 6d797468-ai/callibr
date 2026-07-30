"""
Architecture Tests - Layer Validation

Verifie que l'architecture hexagonale est respectee.
Les domaines ne doivent pas dependre de l'infrastructure.
"""

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent.parent

EXCLUDE_DIRS = {"node_modules", ".venv", "engineering", "__pycache__", ".git"}


def _should_scan(path: Path) -> bool:
    return all(part not in EXCLUDE_DIRS for part in path.parts)


LAYER_MAP = {
    "packages/kernel": "domain",
    "packages/contracts": "domain",
    "engines": "domain",
    "packages/persistence": "infrastructure",
    "platform/identity": "infrastructure",
    "apps/api": "infrastructure",
    "apps/frontend": "infrastructure",
    "infrastructure": "infrastructure",
}


def get_layer(path: str) -> str | None:
    for prefix, layer in LAYER_MAP.items():
        if prefix in path:
            return layer
    return None


def get_imports(filepath: Path) -> list[str]:
    try:
        tree = ast.parse(filepath.read_text())
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        return imports
    except Exception:
        return []


def test_domain_does_not_import_infrastructure():
    violations = []

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
            imports = get_imports(py_file)
            for imp in imports:
                if "callibr_persistence" in imp:
                    violations.append(f"{py_file}: importe callibr_persistence")
                if "callibr_identity" in imp:
                    violations.append(f"{py_file}: importe callibr_identity")
                if "callibr_api" in imp:
                    violations.append(f"{py_file}: importe callibr_api")

    assert len(violations) == 0, "Violations d'architecture:\n" + "\n".join(violations)


def test_contracts_do_not_import_engines():
    contracts_dir = ROOT / "packages" / "contracts" / "src"
    if not contracts_dir.exists():
        pytest.skip("Dossier contracts non trouve")

    violations = []
    for py_file in contracts_dir.rglob("*.py"):
        imports = get_imports(py_file)
        for imp in imports:
            if "callibr_simulation" in imp:
                violations.append(f"{py_file}: importe callibr_simulation")
            if "callibr_crm" in imp:
                violations.append(f"{py_file}: importe callibr_crm")
            if "callibr_evaluation" in imp:
                violations.append(f"{py_file}: importe callibr_evaluation")

    assert len(violations) == 0, "Contracts importent des engines:\n" + "\n".join(violations)


def test_kernel_has_no_external_framework_dependencies():
    kernel_dir = ROOT / "packages" / "kernel" / "src"
    if not kernel_dir.exists():
        pytest.skip("Dossier kernel non trouve")

    violations = []
    for py_file in kernel_dir.rglob("*.py"):
        imports = get_imports(py_file)
        for imp in imports:
            if "fastapi" in imp:
                violations.append(f"{py_file}: importe fastapi")
            if "sqlalchemy" in imp:
                violations.append(f"{py_file}: importe sqlalchemy")
            if "pydantic" in imp and "callibr_contracts" not in imp:
                violations.append(f"{py_file}: importe pydantic (devrait etre dans contracts)")

    assert len(violations) == 0, "Kernel a des dependances interdites:\n" + "\n".join(violations)


def test_all_packages_have_init():
    packages = [
        ROOT / "packages" / "kernel" / "src" / "callibr_kernel",
        ROOT / "packages" / "contracts" / "src" / "callibr_contracts",
        ROOT / "packages" / "persistence" / "src" / "callibr_persistence",
        ROOT / "packages" / "telemetry" / "src" / "callibr_telemetry",
        ROOT / "packages" / "shared" / "src" / "callibr_shared",
        ROOT / "platform" / "identity" / "src" / "callibr_identity",
    ]

    missing = []
    for pkg in packages:
        if pkg.exists() and not (pkg / "__init__.py").exists():
            missing.append(str(pkg))

    assert len(missing) == 0, "Packages sans __init__.py:\n" + "\n".join(missing)


def test_no_hardcoded_secrets():
    secret_patterns = ["password", "secret", "api_key"]
    violations = []

    for py_file in ROOT.rglob("*.py"):
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
                        violations.append(f"{py_file}:{i}: {line.strip()[:80]}")
        except Exception:
            pass

    assert len(violations) == 0, "Secrets hardcodes:\n" + "\n".join(violations)
