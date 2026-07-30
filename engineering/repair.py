"""
Callibr Repair — Three-Level Repair System

Niveau 1 (Sur) : Automatique sans risque
Niveau 2 (Assiste) : Propose un patch
Niveau 3 (Guide) : Propose des strategies
"""

import subprocess
import sys
from pathlib import Path

from engineering.diagnostics import run_all_diagnostics


def _repair_level_1_safe() -> list[str]:
    actions = []

    fmt = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            "apps",
            "packages",
            "platform",
            "engines",
            "tests",
        ],
        capture_output=True,
        text=True,
    )
    if fmt.returncode == 0:
        actions.append("Code formate (ruff format)")

    fix = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--fix",
            "apps",
            "packages",
            "platform",
            "engines",
            "tests",
        ],
        capture_output=True,
        text=True,
    )
    if fix.returncode == 0:
        actions.append("Lint corrige (ruff --fix)")

    root = Path(".")
    for pkg_dir in [
        root / "packages" / "kernel" / "src" / "callibr_kernel",
        root / "packages" / "contracts" / "src" / "callibr_contracts",
        root / "packages" / "persistence" / "src" / "callibr_persistence",
        root / "packages" / "telemetry" / "src" / "callibr_telemetry",
        root / "platform" / "identity" / "src" / "callibr_identity",
    ]:
        if pkg_dir.exists() and not (pkg_dir / "__init__.py").exists():
            (pkg_dir / "__init__.py").write_text("")
            actions.append(f"__init__.py cree: {pkg_dir}")

    return actions


def _repair_level_2_assisted() -> list[str]:
    diagnostics = run_all_diagnostics()
    proposals = []

    for d in diagnostics:
        if d.passed:
            continue

        if d.check_id == "chk-tenant-isolation" or d.check_id == "chk-arch-layers":
            proposals.append(
                f"PROPOSITION pour {d.location}:\n"
                f"  {d.fix_proposal}\n"
                f"  [Non implemente — necessite validation humaine]"
            )

    return proposals


def _repair_level_3_guided() -> list[str]:
    diagnostics = run_all_diagnostics()
    guides = []

    for d in diagnostics:
        if d.passed:
            continue

        if d.check_id == "chk-arch-layers":
            guides.append(
                f"VIOLATION ARCHITECTURALE dans {d.location}\n"
                f"\n"
                f"Deux strategies possibles :\n"
                f"\n"
                f"  1. Port & Adapter\n"
                f"     Creer un port (interface) dans kernel/.\n"
                f"     L'adapter d'infrastructure implemente ce port.\n"
                f"     Le domaine depend du port, pas de l'adapter.\n"
                f"\n"
                f"  2. Dependency Injection\n"
                f"     Passer le store en parametre du service.\n"
                f"     Le service ne connait que l'interface Protocol.\n"
                f"\n"
                f"  Choisissez une strategie avant de corriger."
            )

    return guides


def run_repair() -> int:
    print("=" * 70)
    print("CALLIBR REPAIR — REPARATION INTELLIGENTE")
    print("=" * 70)
    print()

    print("--- NIVEAU 1 : REPARATION AUTOMATIQUE ---")
    print()
    level1 = _repair_level_1_safe()
    if level1:
        for action in level1:
            print(f"  [OK] {action}")
    else:
        print("  Aucune action automatique necessaire.")
    print()

    print("--- NIVEAU 2 : REPARATION ASSISTEE ---")
    print()
    level2 = _repair_level_2_assisted()
    if level2:
        for proposal in level2:
            print(f"  {proposal}")
            print()
    else:
        print("  Aucune proposition.")
    print()

    print("--- NIVEAU 3 : REPARATION GUIDEE ---")
    print()
    level3 = _repair_level_3_guided()
    if level3:
        for guide in level3:
            print(f"  {guide}")
            print()
    else:
        print("  Aucune guidance necessaire.")
    print()

    print("REPARATION TERMINEE")
    print("Relancer 'callibr doctor' pour valider.")
    return 0
