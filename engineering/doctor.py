"""
Callibr Doctor - Intelligent Health Check System

Verifie automatiquement l'etat du projet Callibr.
Fournit des diagnostics intelligents avec contexte complet.
"""

from engineering.diagnostics import Severity, run_all_diagnostics
from engineering.scoring import compute_global_score


def _severity_icon(severity: Severity) -> str:
    return {
        Severity.CRITICAL: "!!!",
        Severity.HIGH: "!! ",
        Severity.MEDIUM: "!  ",
        Severity.LOW: ".  ",
    }[severity]


def run_doctor() -> int:
    print("=" * 70)
    print("CALLIBR DOCTOR — DIAGNOSTIC INTELLIGENT")
    print("=" * 70)
    print()

    diagnostics = run_all_diagnostics()

    if not diagnostics:
        print("AUCUN PROBLEME DETECTE")
        print()
    else:
        for d in diagnostics:
            icon = _severity_icon(d.severity)
            status = "PASS" if d.passed else "FAIL"
            print(f"[{status}] [{icon}] {d.title}")
            print(f"       Fichier  : {d.location}")
            print(f"       Cause    : {d.cause}")
            print(f"       Regle    : {d.rule_reference}")
            print(f"       Capability: {d.capability}")
            print(f"       Impact   : {d.impact}")
            print(f"       Fix      : {d.fix_proposal}")
            if d.auto_fixable:
                print("       Auto-fix : OUI — 'callibr repair' peut corriger")
            print()

    print("=" * 70)
    print("ENGINEERING SCORE")
    print("=" * 70)
    print()

    global_score, categories = compute_global_score()

    for cat in categories:
        bar_len = int(cat.score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {cat.name:<20} {bar} {cat.score:>5.1f}%")

    print()
    print(f"  {'GLOBAL':<20} {'':20} {global_score:>5.1f}%")
    print()

    failed = sum(1 for d in diagnostics if not d.passed)
    if failed == 0:
        print("TOUS LES CHECKS SONT VERTS")
        return 0
    else:
        print(f"{failed} PROBLEMES DETECTES — voir les diagnostics ci-dessus")
        return 1
