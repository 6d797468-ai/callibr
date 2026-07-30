"""
Callibr Score Trend Tracking

Suit l'evolution du score d'ingénierie dans le temps.
"""

import json
from datetime import datetime
from pathlib import Path

from engineering.scoring import compute_global_score

TREND_FILE = Path(".callibr/score-history.json")


def _ensure_dir():
    TREND_FILE.parent.mkdir(parents=True, exist_ok=True)


def record_score():
    _ensure_dir()
    global_score, categories = compute_global_score()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "global": global_score,
        "categories": {cat.name: cat.score for cat in categories},
    }

    history = []
    if TREND_FILE.exists():
        try:
            history = json.loads(TREND_FILE.read_text())
        except Exception:
            history = []

    history.append(entry)

    if len(history) > 100:
        history = history[-100:]

    TREND_FILE.write_text(json.dumps(history, indent=2))
    return entry


def get_trend() -> list[dict]:
    if not TREND_FILE.exists():
        return []
    try:
        return json.loads(TREND_FILE.read_text())
    except Exception:
        return []


def get_trend_summary() -> str:
    history = get_trend()
    if len(history) < 2:
        return "Pas assez de donnees pour une tendance (minimum 2 mesures)."

    current = history[-1]["global"]
    previous = history[-2]["global"]
    delta = current - previous

    first = history[0]["global"]
    total_delta = current - first

    trend_icon = "▲" if delta > 0 else "▼" if delta < 0 else "─"

    lines = [
        f"Score actuel : {current:.1f}%",
        f"Tendance : {trend_icon} {delta:+.1f}% depuis la derniere mesure",
        f"Evolution : {total_delta:+.1f}% depuis le debut ({len(history)} mesures)",
    ]

    if len(history) >= 3:
        scores = [h["global"] for h in history]
        avg = sum(scores) / len(scores)
        lines.append(f"Moyenne : {avg:.1f}%")

    return "\n".join(lines)


def print_trend():
    print("=" * 50)
    print("TENDANCE ENGINEERING SCORE")
    print("=" * 50)
    print()
    print(get_trend_summary())
    print()

    history = get_trend()
    if history:
        print("Historique :")
        for entry in history[-10:]:
            ts = entry["timestamp"][:16]
            score = entry["global"]
            bar_len = int(score / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {ts}  {bar}  {score:.1f}%")
    print()
