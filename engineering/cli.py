"""
Callibr Engineering CLI

Commands:
    doctor       - Diagnostic intelligent du projet
    verify       - Pipeline de validation complet
    repair       - Reparation intelligente (3 niveaux)
    score        - Afficher le score engineering
    plan         - Generer un plan d'execution
    trend        - Afficher la tendance du score
    gate         - Release Gate
    capabilities - Couverture des capabilities
    check        - Verification individuelle
"""

import argparse

from engineering.check import run_check
from engineering.doctor import run_doctor
from engineering.execution import generate_all_plans
from engineering.knowledge_enhanced import compute_capability_coverage
from engineering.release_gate import run_release_gate
from engineering.repair import run_repair
from engineering.scoring import compute_global_score
from engineering.trend import print_trend, record_score
from engineering.verify import run_verify


def _run_score() -> int:
    global_score, categories = compute_global_score()
    print("=" * 50)
    print("ENGINEERING SCORE")
    print("=" * 50)
    print()
    for cat in categories:
        bar_len = int(cat.score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {cat.name:<20} {bar} {cat.score:>5.1f}%")
    print()
    print(f"  {'GLOBAL':<20} {'':20} {global_score:>5.1f}%")
    record_score()
    return 0


def _run_plan() -> int:
    plans = generate_all_plans()
    if not plans:
        print("Aucun plan d'execution necessaire — tous les checks passent.")
        return 0
    for plan in plans:
        print(plan.summary())
        print("-" * 70)
    return 0


def _run_capabilities() -> int:
    coverages = compute_capability_coverage()
    print("=" * 60)
    print("CAPABILITY COVERAGE")
    print("=" * 60)
    print()
    print(
        f"  {'Capability':<15} {'Code':>5} {'Contrat':>7} {'Tests':>5}"
        f" {'API':>5} {'Front':>5} {'Doc':>4} {'Total':>6} {'Statut':<12}"
    )
    print(
        f"  {'-' * 15} {'-' * 5} {'-' * 7} {'-' * 5} {'-' * 5}"
        f" {'-' * 5} {'-' * 4} {'-' * 6} {'-' * 12}"
    )
    for c in coverages:
        code = "  OK" if c.has_code else "  --"
        contr = "     OK" if c.has_contracts else "     --"
        tests = "   OK" if c.has_tests else "   --"
        api = "   OK" if c.has_api else "   --"
        front = "   OK" if c.has_frontend else "   --"
        doc = " OK" if c.has_documentation else " --"
        total = f"{c.coverage_pct:.0f}%"
        print(
            f"  {c.capability:<15} {code} {contr} {tests} {api}"
            f" {front} {doc} {total:>6} {c.status:<12}"
        )
    print()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="callibr",
        description="Callibr Engineering Execution System",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commande a executer")

    subparsers.add_parser("doctor", help="Diagnostic intelligent du projet")
    subparsers.add_parser("verify", help="Pipeline de validation complet")
    subparsers.add_parser("repair", help="Reparation intelligente (3 niveaux)")
    subparsers.add_parser("score", help="Afficher le score engineering")
    subparsers.add_parser("plan", help="Generer un plan d'execution")
    subparsers.add_parser("trend", help="Afficher la tendance du score")
    subparsers.add_parser("gate", help="Release Gate")
    subparsers.add_parser("capabilities", help="Couverture des capabilities")

    check_parser = subparsers.add_parser("check", help="Verification individuelle")
    check_parser.add_argument("name", help="Nom de la verification")

    args = parser.parse_args()

    commands = {
        "doctor": run_doctor,
        "verify": run_verify,
        "repair": run_repair,
        "score": _run_score,
        "plan": _run_plan,
        "trend": print_trend,
        "gate": run_release_gate,
        "capabilities": _run_capabilities,
        "check": lambda: run_check(args.name) if hasattr(args, "name") else 1,
    }

    if args.command in commands:
        return commands[args.command]()
    else:
        parser.print_help()
        return 1
