from __future__ import annotations

from datetime import datetime

import weasyprint

from callibr_telemetry.dashboard import DashboardData
from callibr_telemetry.readiness import ReadinessResult

REPORT_CSS = """
@page {
  size: A4;
  margin: 2cm 2.5cm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-size: 9px;
    color: #889aa8;
  }
}
body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.5;
  color: #172026;
}
h1 { font-size: 22pt; margin: 0 0 4px; }
h2 { font-size: 14pt; margin: 24px 0 8px; border-bottom: 2px solid #245b78; padding-bottom: 4px; }
h3 { font-size: 12pt; margin: 16px 0 4px; }
p { margin: 4px 0; }
.eyebrow { font-size: 9pt; color: #476173; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; }
.header { margin-bottom: 24px; }
.header .meta { font-size: 9pt; color: #526879; margin-top: 4px; }
.hero { background: #245b78; color: #fff; padding: 24px; border-radius: 8px; margin-bottom: 24px; text-align: center; }
.hero .score { font-size: 48pt; font-weight: 800; line-height: 1; }
.hero .label { font-size: 10pt; opacity: 0.9; margin-top: 4px; }
.hero .status-badge { display: inline-block; margin-top: 8px; padding: 4px 12px; border-radius: 999px; font-size: 9pt; font-weight: 700; text-transform: uppercase; }
.status-ready { background: #e8f5e9; color: #2e7d32; }
.status-almost_ready { background: #fff3e0; color: #e65100; }
.status-not_ready { background: #fce4ec; color: #c62828; }
.metrics { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 24px; }
.metric { text-align: center; padding: 12px; border: 1px solid #d7dee4; border-radius: 6px; }
.metric .value { font-size: 18pt; font-weight: 800; }
.metric .label { font-size: 8pt; color: #526879; text-transform: uppercase; font-weight: 700; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 16px; }
th { text-align: left; font-size: 8pt; text-transform: uppercase; color: #476173; border-bottom: 2px solid #d7dee4; padding: 6px 8px; }
td { padding: 6px 8px; border-bottom: 1px solid #eef2f5; font-size: 10pt; }
.dimensions { display: flex; gap: 16px; margin: 16px 0; flex-wrap: wrap; }
.dim { flex: 1; min-width: 100px; text-align: center; padding: 12px; border: 1px solid #d7dee4; border-radius: 6px; }
.dim .dim-value { font-size: 16pt; font-weight: 800; }
.dim .dim-label { font-size: 8pt; color: #526879; text-transform: uppercase; font-weight: 700; }
.feedback-box { background: #f7fafc; border: 1px solid #d7dee4; border-radius: 6px; padding: 16px; margin: 8px 0; }
.feedback-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 10pt; border-bottom: 1px solid #eef2f5; }
.footer { margin-top: 32px; padding-top: 12px; border-top: 1px solid #d7dee4; font-size: 8pt; color: #889aa8; text-align: center; }
"""


def build_report_html(data: DashboardData, readiness: ReadinessResult) -> str:
    status_color = {
        "READY": "status-ready",
        "ALMOST_READY": "status-almost_ready",
        "NOT_READY": "status-not_ready",
    }.get(readiness.status, "status-not_ready")

    total_would = sum(data.product.would_use_counts.values()) or 1
    would_yes_pct = round(data.product.would_use_counts.get("yes", 0) / total_would * 100)

    criteria_rows = ""
    for c in data.performance.weakest_criteria[:5]:
        criteria_rows += f"<tr><td>{c['label']}</td><td>{c['average']}%</td><td>À améliorer</td></tr>\n"
    for c in data.performance.strongest_criteria[:3]:
        criteria_rows += f"<tr><td>{c['label']}</td><td>{c['average']}%</td><td>✅ Point fort</td></tr>\n"

    ranking_rows = ""
    for i, s in enumerate(data.business.scenario_ranking[:8]):
        ranking_rows += f"<tr><td>{i + 1}</td><td>{s['title']}</td><td>{s['average_score']}</td><td>{s['count']}</td></tr>\n"

    dims_html = ""
    dims = [
        ("Adoption", readiness.dimensions.adoption, "#245b78"),
        ("Complétion", readiness.dimensions.completion, "#2f7d57"),
        ("Feedback", readiness.dimensions.feedback, "#f4b836"),
        ("Stabilité", readiness.dimensions.stability, "#7b61ff"),
        ("Analytics", readiness.dimensions.analytics, "#e65100"),
    ]
    for label, val, _ in dims:
        dims_html += f'<div class="dim"><div class="dim-value">{val}</div><div class="dim-label">{label}</div></div>'

    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Callibr — Rapport Exécutif</title></head>
<body>
<div class="header">
  <p class="eyebrow">Callibr — Rapport Exécutif</p>
  <h1>Pilot Success Center</h1>
  <p class="meta">Release 0.1 &mdash; Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M")}</p>
</div>

<div class="hero">
  <div class="score">{readiness.score}</div>
  <div class="label">Pilot Readiness Score</div>
  <div class="status-badge {status_color}">{readiness.status.replace("_", " ")}</div>
</div>

<h2>Vue d'ensemble</h2>
<div class="metrics">
  <div class="metric"><div class="value">{data.overview.simulations_started}</div><div class="label">Lancées</div></div>
  <div class="metric"><div class="value">{data.overview.simulations_completed}</div><div class="label">Terminées</div></div>
  <div class="metric"><div class="value">{data.overview.completion_rate}%</div><div class="label">Complétion</div></div>
  <div class="metric"><div class="value">{int(data.overview.average_duration_seconds / 60)} min</div><div class="label">Durée moy.</div></div>
  <div class="metric"><div class="value">{data.overview.active_users}</div><div class="label">Utilisateurs</div></div>
  <div class="metric"><div class="value">{data.overview.total_sessions}</div><div class="label">Sessions</div></div>
</div>

<h2>Dimensions Pilot Readiness</h2>
<div class="dimensions">{dims_html}</div>

<h2>Performance</h2>
<p><strong>Score moyen :</strong> {data.performance.average_score}/100</p>
<table>
  <thead><tr><th>Critère</th><th>Score</th><th>Statut</th></tr></thead>
  <tbody>{criteria_rows}</tbody>
</table>

<h2>Feedback produit</h2>
<div class="feedback-box">
  <div class="feedback-row"><span>Satisfaction moyenne</span><strong>{data.product.average_satisfaction}/5</strong></div>
  <div class="feedback-row"><span>Recommanderait à son équipe (Oui)</span><strong>{would_yes_pct}%</strong></div>
  <div class="feedback-row"><span>Abandons</span><strong>{data.product.abandon_count}</strong></div>
  <div class="feedback-row"><span>Replays consultés</span><strong>{data.product.replay_count}</strong></div>
</div>

{"<h2>Classement des scénarios</h2><table><thead><tr><th>#</th><th>Scénario</th><th>Score</th><th>Nb</th></tr></thead><tbody>" + ranking_rows + "</tbody></table>" if data.business.scenario_ranking else ""}

<div class="footer">
  <p>Callibr — AI Contact Center Simulation Platform &mdash; Rapport généré automatiquement</p>
</div>
</body>
</html>"""


def generate_pdf(data: DashboardData, readiness: ReadinessResult) -> bytes:
    html = build_report_html(data, readiness)
    doc = weasyprint.HTML(string=html)
    return doc.write_pdf()
