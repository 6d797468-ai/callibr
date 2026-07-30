# Volume K07 — Observability, Monitoring & SRE Architecture

> Extrait généré depuis `Architecture & Engineering Book (AEB).md` le 2026-07-27.

PHASE K — DEV PLATFORM, DEVSECOPS & PLATFORM ENGINEERING
Volume K07
Observability, Monitoring & SRE Architecture

Version : 1.0

Statut : Reliability Engineering Foundation

Criticité : Critique

1. Vision

L'observabilité permet de comprendre le comportement réel de Callibr.

Elle couvre :

logs ;
metrics ;
traces ;
events ;
dashboards ;
alerts ;
SLO ;
runbooks ;
postmortems.

2. Principe fondamental

Un système non observable n'est pas opérable.

Chaque service doit exposer ce qu'il fait, pourquoi il échoue et quel est l'impact.

3. Architecture globale

                    Services


                       │


                       ▼


                 Telemetry Collection


       ┌───────────────┼───────────────┐


       ▼               ▼               ▼


      Logs           Metrics          Traces


                       │


                       ▼


             Dashboards / Alerts / SLO

4. Telemetry Standards

Standards :

OpenTelemetry ;
structured logs ;
Prometheus metrics ;
trace context propagation ;
correlation_id ;
tenant_id safe tagging.

5. Golden Signals

Signaux :

latency ;
traffic ;
errors ;
saturation.

Pour l'IA :

model_latency ;
token_usage ;
tool_errors ;
guardrail_blocks ;
cost_burn_rate.

6. Alerting

Alertes basées sur :

SLO burn rate ;
latence critique ;
erreurs ;
queue lag ;
coût anormal ;
sécurité ;
données fraîches en retard.

7. Runbooks

Chaque alerte critique pointe vers :

description ;
impact ;
diagnostic ;
mitigation ;
rollback ;
escalation.

8. Data Model

TelemetrySignal
---------------

id

service

signal_type

name

owner

AlertRule
---------

id

signal

condition

severity

runbook_ref

SLODefinition
-------------

id

service

metric

target

window

9. API interne

Lister SLO :

GET /observability/slo

Créer alerte :

POST /observability/alerts

Lire traces :

GET /observability/traces/{trace_id}

10. Décisions d'architecture (ADR)

ADR-K07-001
OpenTelemetry est le standard de tracing.

Décision :

Uniformiser la télémétrie.

ADR-K07-002
Les alertes critiques sont liées à des runbooks.

Décision :

Accélérer la réponse incident.

ADR-K07-003
Les SLO pilotent l'alerting.

Décision :

Réduire le bruit et cibler l'impact utilisateur.

ADR-K07-004
Les données sensibles sont exclues des logs.

Décision :

Préserver confidentialité et conformité.

11. Critères d'acceptation

Observability conforme lorsque :

logs, métriques et traces existent ;
les traces traversent les services ;
les alertes pointent vers runbooks ;
les SLO sont mesurés ;
les dashboards couvrent les services critiques ;
les logs excluent les secrets.

Décision majeure : Observable by Design

Callibr est conçu pour être compris en production.
