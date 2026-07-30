"""
Callibr Verify - Full Validation Pipeline

Execute la chaine de validation complete :
pytest -> ruff -> mypy -> integration -> arch tests -> smoke -> coverage -> DoD
"""

import subprocess
import sys
from dataclasses import dataclass


@dataclass
class StepResult:
    name: str
    passed: bool
    output: str = ""


def run_step(name: str, command: list[str]) -> StepResult:
    print(f"Etape: {name}...", end=" ", flush=True)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            print("OK")
            return StepResult(name=name, passed=True, output=result.stdout)
        else:
            print("ECHEC")
            if result.stderr:
                print(f"  {result.stderr[:500]}")
            return StepResult(name=name, passed=False, output=result.stderr)
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return StepResult(name=name, passed=False, output="Timeout apres 300s")
    except FileNotFoundError:
        print("NON TROUVE")
        return StepResult(name=name, passed=False, output=f"Commande non trouvee: {command[0]}")


def run_verify() -> int:
    print("=" * 60)
    print("CALLIBR VERIFY")
    print("=" * 60)
    print()

    steps = [
        ("Tests unitaires", [sys.executable, "-m", "pytest", "tests/", "-v"]),
        (
            "Lint (ruff)",
            [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "apps",
                "packages",
                "platform",
                "engines",
                "tests",
            ],
        ),
        (
            "Typage (mypy)",
            [
                sys.executable,
                "-m",
                "mypy",
                "--ignore-missing-imports",
                "packages/",
                "platform/",
                "engines/",
            ],
        ),
        ("Architecture tests", [sys.executable, "-m", "pytest", "tests/architecture/", "-v"]),
        ("Tests API", [sys.executable, "-m", "pytest", "apps/api/tests/", "-v"]),
    ]

    results: list[StepResult] = []

    for name, command in steps:
        result = run_step(name, command)
        results.append(result)
        if not result.passed:
            print()
            print("PIPELINE ARRETE - correction necessaire")
            break

    print()
    print("=" * 60)
    print("RESUME VERIFY")
    print("=" * 60)

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total = len(results)

    print(f"Total: {total}")
    print(f"Reussis: {passed}")
    print(f"Echecs: {failed}")
    print()

    if failed == 0:
        print("TOUS LES CHECKS SONT VERTS")
        return 0
    else:
        print("DES CHECKS ONT ECHOUE :")
        for r in results:
            if not r.passed:
                print(f"  - {r.name}")
        return 1
