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
h1 { font-size: 22pt; margin: 0; }
h2 { font-size: 14pt; margin: 24px 0 8px; border-bottom: 2px solid #245b78; padding-bottom: 4px; color: #172026; }
h3 { font-size: 12pt; margin: 16px 0 4px; }
p { margin: 4px 0; }
.eyebrow { font-size: 9pt; color: #476173; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; }
.header { margin-bottom: 24px; }
.header .meta { font-size: 9pt; color: #526879; margin-top: 4px; }
.hero { background: #245b78; color: #fff; padding: 28px 24px; border-radius: 8px; margin-bottom: 24px; text-align: center; }
.hero .score { font-size: 48pt; font-weight: 800; line-height: 1; }
.hero .label { font-size: 10pt; opacity: 0.9; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
.hero .status-badge { display: inline-block; margin-top: 8px; padding: 4px 14px; border-radius: 999px; font-size: 9pt; font-weight: 700; text-transform: uppercase; }
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
.dim { flex: 1; min-width: 100px; text-align: center; padding: 12px 8px; border: 1px solid #d7dee4; border-radius: 6px; }
.dim .dim-value { font-size: 18pt; font-weight: 800; }
.dim .dim-bar { height: 4px; background: #eef2f5; border-radius: 999px; overflow: hidden; margin: 4px 0; }
.dim .dim-fill { height: 100%; border-radius: 999px; }
.dim .dim-label { font-size: 7pt; color: #526879; text-transform: uppercase; font-weight: 700; }
.feedback-box { background: #f7fafc; border: 1px solid #d7dee4; border-radius: 6px; padding: 16px; margin: 8px 0; }
.feedback-row { display: flex; justify-content: space-between; padding: 5px 0; font-size: 10pt; border-bottom: 1px solid #eef2f5; }
.action-plan { margin: 8px 0 16px; padding-left: 24px; }
.action-plan li { margin-bottom: 6px; font-size: 10pt; line-height: 1.5; color: #29465a; }
.footer { margin-top: 32px; padding-top: 12px; border-top: 1px solid #d7dee4; font-size: 8pt; color: #889aa8; text-align: center; }
"""


def build_action_plan(readiness: ReadinessResult) -> str:
    items = []
    if readiness.dimensions.adoption < 80:
        items.append("Augmenter le nombre de sessions par utilisateur (objectif : 5 sessions/utilisateur)")
    if readiness.dimensions.completion < 80:
        items.append("Améliorer le taux de complétion — les simulations abandonnées doivent être analysées")
    if readiness.dimensions.feedback < 70:
        items.append("Encourager le retour d'expérience après chaque simulation (objectif : 50% de taux de réponse)")
    if readiness.dimensions.analytics < 100:
        items.append("Finaliser la configuration des événements produit pour le suivi analytique")
    if not items:
        items.append("Tous les indicateurs sont au vert. Maintenir la cadence et étendre le déploiement.")
    return "".join(f"<li>{i}</li>" for i in items)


def build_report_html(data: DashboardData, readiness: ReadinessResult) -> str:
    status_color = {
        "READY": "status-ready",
        "ALMOST_READY": "status-almost_ready",
        "NOT_READY": "status-not_ready",
    }.get(readiness.status, "status-not_ready")

    readiness_label = (
        "Prêt" if readiness.status == "READY"
        else "Presque prêt" if readiness.status == "ALMOST_READY"
        else "Pas encore prêt"
    )

    total_would = sum(data.product.would_use_counts.values()) or 1
    would_yes_pct = round(data.product.would_use_counts.get("yes", 0) / total_would * 100)

    weak_rows = ""
    for c in data.performance.weakest_criteria[:5]:
        weak_rows += f"<tr><td>{c['label']}</td><td>{c['average']}%</td><td style='color:#b45309'>À améliorer</td></tr>\n"

    strong_rows = ""
    for c in data.performance.strongest_criteria[:5]:
        strong_rows += f"<tr><td>{c['label']}</td><td>{c['average']}%</td><td style='color:#2e7d32'>✅ Acquis</td></tr>\n"

    ranking_rows = ""
    for i, s in enumerate(data.business.scenario_ranking[:8]):
        ranking_rows += f"<tr><td>{i + 1}</td><td>{s['title']}</td><td>{s['average_score']}</td><td>{s['count']}</td></tr>\n"

    dims_html = ""
    dims = [
        ("Adoption", readiness.dimensions.adoption),
        ("Complétion", readiness.dimensions.completion),
        ("Feedback", readiness.dimensions.feedback),
        ("Stabilité", readiness.dimensions.stability),
        ("Analytics", readiness.dimensions.analytics),
    ]
    for label, val in dims:
        pct = min(val, 100)
        color = "#2f7d57" if val >= 80 else "#e65100" if val >= 50 else "#c62828"
        dims_html += f"""<div class="dim">
          <div class="dim-value" style="color:{color}">{pct}</div>
          <div class="dim-bar"><div class="dim-fill" style="width:{pct}%;background:{color}"></div></div>
          <div class="dim-label">{label}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>Callibr — Rapport Exécutif</title></head>
<body>

<!-- Header -->
<div class="header">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
    <svg width="48" height="48" viewBox="0 0 64 64" fill="none">
      <rect x="8" y="20" width="48" height="32" rx="4" fill="#245b78" opacity="0.12" />
      <rect x="8" y="20" width="48" height="32" rx="4" stroke="#245b78" stroke-width="2" fill="none" />
      <circle cx="32" cy="36" r="8" fill="#245b78" />
      <path d="M28 36l3 3 5-6" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M22 16l4-8h12l4 8" stroke="#245b78" stroke-width="2" fill="none" stroke-linejoin="round" />
    </svg>
    <div>
      <p class="eyebrow">Callibr — Rapport Exécutif</p>
      <h1 style="margin:0">Pilot Success Center</h1>
    </div>
  </div>
  <p class="meta">Release 0.1 &mdash; Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M")}</p>
</div>

<!-- Résumé exécutif -->
<div class="hero">
  <div class="score">{readiness.score}/100</div>
  <div class="label">Pilot Readiness</div>
  <div class="status-badge {status_color}">{readiness_label}</div>
  <p style="margin-top:12px;font-size:10pt;opacity:0.85">
    {data.overview.active_users} utilisateur(s) &middot; {data.overview.total_sessions} session(s) &middot;
    Score moyen : {data.performance.average_score}/100
  </p>
</div>

<!-- Indicateurs clés -->
<h2>Indicateurs clés</h2>
<div class="metrics">
  <div class="metric"><div class="value">{data.overview.simulations_started}</div><div class="label">Simulations lancées</div></div>
  <div class="metric"><div class="value">{data.overview.simulations_completed}</div><div class="label">Terminées</div></div>
  <div class="metric"><div class="value">{data.overview.completion_rate}%</div><div class="label">Taux de complétion</div></div>
  <div class="metric"><div class="value">{int(data.overview.average_duration_seconds / 60)} min</div><div class="label">Durée moyenne</div></div>
  <div class="metric"><div class="value">{data.product.average_satisfaction}/5</div><div class="label">Satisfaction</div></div>
  <div class="metric"><div class="value">{would_yes_pct}%</div><div class="label">Recommandation (Oui)</div></div>
</div>

<!-- Dimensions Readiness -->
<h2>5 piliers de la readiness</h2>
<div class="dimensions">{dims_html}</div>

<!-- Points forts / Points faibles -->
<h2>Analyse des compétences</h2>
<table>
  <thead><tr><th>Critère</th><th>Score</th><th>Statut</th></tr></thead>
  <tbody>
    {weak_rows if weak_rows else '<tr><td colspan="3" style="text-align:center;color:#526879">Aucune donnée disponible</td></tr>'}
  </tbody>
</table>

<table>
  <thead><tr><th>Point fort</th><th>Score</th><th>Statut</th></tr></thead>
  <tbody>
    {strong_rows if strong_rows else '<tr><td colspan="3" style="text-align:center;color:#526879">Aucune donnée disponible</td></tr>'}
  </tbody>
</table>

<!-- Feedback produit -->
<h2>Engagement des apprenants</h2>
<div class="feedback-box">
  <div class="feedback-row"><span>Satisfaction moyenne</span><strong>{data.product.average_satisfaction}/5</strong></div>
  <div class="feedback-row"><span>Recommanderait à son équipe</span><strong>{would_yes_pct}%</strong> ({data.product.would_use_counts.get("yes",0)})</div>
  <div class="feedback-row"><span>Abandons</span><strong>{data.product.abandon_count}</strong></div>
  <div class="feedback-row"><span>Replays consultés</span><strong>{data.product.replay_count}</strong></div>
</div>

<!-- Classement scénarios -->
{"<h2>Classement des scénarios</h2><table><thead><tr><th>#</th><th>Scénario</th><th>Score moyen</th><th>Simulations</th></tr></thead><tbody>" + ranking_rows + "</tbody></table>" if data.business.scenario_ranking else ""}

<!-- Plan d'action -->
<h2>Plan d'action prioritaire</h2>
<ol class="action-plan">{build_action_plan(readiness)}</ol>

<div class="footer">
  <p>Callibr — AI Contact Center Simulation Platform &mdash; Rapport généré automatiquement</p>
</div>
</body>
</html>"""


def generate_pdf(data: DashboardData, readiness: ReadinessResult) -> bytes:
    html = build_report_html(data, readiness)
    doc = weasyprint.HTML(string=html)
    return doc.write_pdf()
