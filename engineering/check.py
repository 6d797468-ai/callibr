"""
Callibr Check - Individual Verification

Execute une verification individuelle par nom.
"""

from engineering.checks import CHECKS


def run_check(name: str) -> int:
    if name not in CHECKS:
        print(f"Verification inconnue: {name}")
        print(f"Verifications disponibles: {', '.join(CHECKS.keys())}")
        return 1

    print(f"Verification: {name}...", end=" ", flush=True)
    try:
        result = CHECKS[name]()
        if result.passed:
            print("OK")
            if result.details:
                print(f"  {result.details}")
            return 0
        else:
            print("ECHEC")
            print(f"  {result.message}")
            if result.details:
                print(f"  {result.details}")
            return 1
    except Exception as e:
        print("ERREUR")
        print(f"  {e}")
        return 1
