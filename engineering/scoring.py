"""
Callibr Engineering Score

Calcule un score global de qualite du projet.
"""

from dataclasses import dataclass


@dataclass
class ScoreCategory:
    name: str
    score: float  # 0-100
    weight: float  # 0-1
    details: str = ""


def compute_architecture_score() -> ScoreCategory:
    import ast
    from pathlib import Path

    ROOT = Path(".")
    violations = 0
    checked = 0

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
            checked += 1
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
                        violations += 1
            except Exception:
                pass

    if checked == 0:
        return ScoreCategory("Architecture", 100.0, 0.20)
    score = max(0, 100 - (violations / checked * 100))
    return ScoreCategory("Architecture", round(score, 1), 0.20)


def compute_test_score() -> ScoreCategory:
    from pathlib import Path

    ROOT = Path(".")
    test_files = list((ROOT / "tests").rglob("test_*.py"))
    api_test_files = list((ROOT / "apps" / "api" / "tests").rglob("test_*.py"))
    total_test_files = len(test_files) + len(api_test_files)

    src_dirs = [
        ROOT / "packages",
        ROOT / "platform",
        ROOT / "engines",
        ROOT / "apps" / "api" / "src",
    ]
    src_files = 0
    for d in src_dirs:
        if d.exists():
            src_files += len(list(d.rglob("*.py")))

    if src_files == 0:
        return ScoreCategory("Tests", 100.0, 0.20)

    ratio = total_test_files / src_files
    score = min(100, ratio * 200)
    return ScoreCategory("Tests", round(score, 1), 0.20)


def compute_type_safety_score() -> ScoreCategory:
    from pathlib import Path

    ROOT = Path(".")
    typed = 0
    untyped = 0

    for py_file in ROOT.rglob("*.py"):
        if (
            "node_modules" in str(py_file)
            or ".venv" in str(py_file)
            or "engineering" in str(py_file)
        ):
            continue
        try:
            content = py_file.read_text()
            if "def " in content:
                has_type_hints = "->" in content or ": str" in content or ": int" in content
                if has_type_hints:
                    typed += 1
                else:
                    untyped += 1
        except Exception:
            pass

    total = typed + untyped
    if total == 0:
        return ScoreCategory("Typage", 100.0, 0.10)
    score = (typed / total) * 100
    return ScoreCategory("Typage", round(score, 1), 0.10)


def compute_security_score() -> ScoreCategory:
    from pathlib import Path

    ROOT = Path(".")
    violations = 0

    secret_patterns = ["password", "secret", "api_key"]
    for py_file in ROOT.rglob("*.py"):
        if (
            "node_modules" in str(py_file)
            or ".venv" in str(py_file)
            or "engineering" in str(py_file)
        ):
            continue
        try:
            content = py_file.read_text()
            for line in content.splitlines():
                for pattern in secret_patterns:
                    if (
                        (f'"{pattern}"' in line.lower() or f"'{pattern}'" in line.lower())
                        and "example" not in line.lower()
                        and "test" not in str(py_file)
                    ):
                        violations += 1
        except Exception:
            pass

    score = max(0, 100 - violations * 25)
    return ScoreCategory("Securite", round(score, 1), 0.15)


def compute_tenant_isolation_score() -> ScoreCategory:
    from pathlib import Path

    ROOT = Path(".")
    total = 0
    isolated = 0

    for py_file in ROOT.rglob("*.py"):
        if (
            "node_modules" in str(py_file)
            or ".venv" in str(py_file)
            or "engineering" in str(py_file)
        ):
            continue
        if "test" in str(py_file):
            continue
        is_store = "store" in py_file.name.lower() or "repository" in py_file.name.lower()
        if not is_store:
            continue

        total += 1
        try:
            content = py_file.read_text()
            if "tenant_id" in content or "TenantContext" in content:
                isolated += 1
        except Exception:
            pass

    if total == 0:
        return ScoreCategory("Tenant Isolation", 100.0, 0.15)
    score = (isolated / total) * 100
    return ScoreCategory("Tenant Isolation", round(score, 1), 0.15)


def compute_documentation_score() -> ScoreCategory:
    from pathlib import Path

    ROOT = Path(".")
    checks = []

    checks.append((ROOT / "implementation" / "IMPLEMENTATION-PRINCIPLES.md").exists())
    checks.append((ROOT / "implementation" / "DEFINITION-OF-DONE.md").exists())
    checks.append((ROOT / "implementation" / "IMPLEMENTATION-WORKFLOW.md").exists())
    checks.append((ROOT / "implementation" / "09-capabilities" / "CAPABILITY-INDEX.md").exists())
    checks.append((ROOT / "adr" / "ADR-REGISTRY.md").exists())

    score = (sum(checks) / len(checks)) * 100
    return ScoreCategory("Documentation", round(score, 1), 0.10)


def compute_infrastructure_score() -> ScoreCategory:
    from pathlib import Path

    ROOT = Path(".")
    checks = []

    checks.append((ROOT / "docker-compose.yml").exists())
    checks.append((ROOT / "infrastructure" / "docker" / "api.Dockerfile").exists())
    checks.append((ROOT / "infrastructure" / "postgres" / "001_runtime_state.sql").exists())
    checks.append((ROOT / "infrastructure" / "postgres" / "alembic").exists())

    score = (sum(checks) / len(checks)) * 100
    return ScoreCategory("Infrastructure", round(score, 1), 0.10)


def compute_global_score() -> tuple[float, list[ScoreCategory]]:
    categories = [
        compute_architecture_score(),
        compute_test_score(),
        compute_type_safety_score(),
        compute_security_score(),
        compute_tenant_isolation_score(),
        compute_documentation_score(),
        compute_infrastructure_score(),
    ]

    total_weight = sum(c.weight for c in categories)
    weighted_sum = sum(c.score * c.weight for c in categories)
    global_score = weighted_sum / total_weight if total_weight > 0 else 0

    return round(global_score, 1), categories
