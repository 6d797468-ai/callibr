"""
Callibr Release Gate

Avant de fusionner ou de publier, le systeme execute automatiquement :
doctor -> verify -> architecture tests -> integration tests -> score -> gate
"""

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from engineering.diagnostics import Severity, run_all_diagnostics
from engineering.knowledge_enhanced import compute_capability_coverage
from engineering.scoring import compute_global_score


@dataclass
class GateResult:
    name: str
    passed: bool
    message: str
    score: float | None = None


_SECRET_PATTERNS: list[re.Pattern] = [
    re.compile(r'sk-proj-[A-Za-z0-9_-]{20,}'),      # OpenAI project key
    re.compile(r'sk-or-v1-[A-Za-z0-9_-]{20,}'),      # OpenRouter
    re.compile(r'AIzaSy[A-Za-z0-9_-]{30,}'),          # Google API key
    re.compile(r'GOCSPX-[A-Za-z0-9_-]{20,}'),         # Google OAuth secret
    re.compile(r'ghp_[A-Za-z0-9_-]{20,}'),            # GitHub PAT
]

_ALLOWED_PATH_PATTERNS: list[re.Pattern] = [
    re.compile(r'\.env\.example$'),
    re.compile(r'test_.*\.py$'),
    re.compile(r'scan-secrets\.'),
]


def _is_allowed(path: Path) -> bool:
    return any(p.search(str(path)) for p in _ALLOWED_PATH_PATTERNS)


_TARGET_GLOBS = ["*.py", "*.yaml", "*.yml", "*.json", "*.toml", "*.cfg", "*.ini", "*.env", ".env.example"]


def _check_secrets(root: str = ".") -> tuple[bool, str]:
    """Scan source files for credential patterns using targeted globs."""
    findings: list[str] = []
    root_path = Path(root).resolve()
    scanned = 0
    for glob in _TARGET_GLOBS:
        for path in root_path.rglob(glob):
            if not path.is_file():
                continue
            if any(ign in path.parts for ign in ("node_modules", ".venv", "venv", "__pycache__", ".git", "dist", "build")):
                continue
            if path.name.startswith(".") and path.name not in (".env", ".env.example"):
                continue
            if _is_allowed(path):
                continue
            scanned += 1
            try:
                text = path.read_text(errors="replace")
                for i, line in enumerate(text.splitlines(), 1):
                    for pattern in _SECRET_PATTERNS:
                        if pattern.search(line):
                            findings.append(f"  {path}:{i}")
            except (OSError, UnicodeDecodeError):
                continue
    if findings:
        return False, f"{len(findings)} secret(s) detecte(s) dans {scanned} fichiers:\n" + "\n".join(findings[:10])
    return True, f"Aucun secret detecte dans {scanned} fichiers"


def _run_cmd(cmd: list[str], timeout: int = 120) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def run_release_gate() -> int:
    print("=" * 70)
    print("CALLIBR RELEASE GATE")
    print("=" * 70)
    print()

    results: list[GateResult] = []

    print("1. Architecture tests...")
    passed, output = _run_cmd(
        [sys.executable, "-m", "pytest", "tests/architecture/", "-v", "--tb=short"]
    )
    results.append(
        GateResult(
            name="Architecture",
            passed=passed,
            message="Tests d'architecture passent" if passed else "Tests d'architecture echouent",
        )
    )

    print("2. Tests unitaires et API...")
    passed, output = _run_cmd(
        [sys.executable, "-m", "pytest", "tests/", "apps/api/tests/", "-v", "--tb=short"]
    )
    results.append(
        GateResult(
            name="Tests",
            passed=passed,
            message="Tests passent" if passed else "Tests echouent",
        )
    )

    print("3. Lint...")
    passed, output = _run_cmd(
        [sys.executable, "-m", "ruff", "check", "apps", "packages", "platform", "engines", "tests"]
    )
    results.append(
        GateResult(
            name="Lint",
            passed=passed,
            message="Lint propre" if passed else "Erreurs de lint",
        )
    )

    print("4. Diagnostics...")
    diagnostics = run_all_diagnostics()
    critical = [d for d in diagnostics if not d.passed and d.severity == Severity.CRITICAL]
    results.append(
        GateResult(
            name="Security & Architecture",
            passed=len(critical) == 0,
            message=f"{len(critical)} violations critiques"
            if critical
            else "Aucune violation critique",
        )
    )

    print("5. Engineering Score...")
    global_score, categories = compute_global_score()
    results.append(
        GateResult(
            name="Score",
            passed=global_score >= 80.0,
            message=f"Score {global_score:.1f}%",
            score=global_score,
        )
    )

    print("6. Capability coverage...")
    coverages = compute_capability_coverage()
    incomplete = [c for c in coverages if c.coverage_pct < 50]
    results.append(
        GateResult(
            name="Capabilities",
            passed=len(incomplete) == 0,
            message=f"{len(incomplete)} capabilities sous 50%"
            if incomplete
            else "Toutes les capabilities sont couvertes",
        )
    )

    print("7. Secret scan...")
    from engineering.checks.secret_scan import scan_secrets

    scan_result = scan_secrets()
    passed = scan_result.passed
    n_findings = len(scan_result.findings)
    n_scanned = scan_result.scanned_files
    msg = (
        f"Aucun secret detecte dans {n_scanned} fichiers"
        if passed
        else f"{n_findings} secret(s) detecte(s) dans {n_scanned} fichiers"
    )
    results.append(GateResult(name="Secrets", passed=passed, message=msg))

    print()
    print("=" * 70)
    print("RESULTAT RELEASE GATE")
    print("=" * 70)
    print()

    all_passed = True
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] {r.name:<25} {r.message}")
        if not r.passed:
            all_passed = False

    print()

    if all_passed:
        print("  RELEASE : AUTORISEE")
        print()
        return 0
    else:
        print("  RELEASE : REFUSEE")
        print()
        print("  Raisons :")
        for r in results:
            if not r.passed:
                print(f"    - {r.name}: {r.message}")
        print()
        return 1
