# Delivery Roadmap

Mise a jour : 2026-07-31

Cadence recommandee : sprint de 2 semaines.

## Baseline actuelle — v0.1.0-rc3

La version **v0.1.0-rc3** (2026-07-31) est la reference immuable. Elle couvre les
milestones M0 a M4 ci-dessous ainsi que la persistance PostgreSQL durable (EP-006).

Etat : architecture gelee, 351 tests unitaires + integration PostgreSQL valides,
5 pipelines CI verts (Backend Quality, Frontend Build, Security Scan, Shell
Validation, PostgreSQL Integration), protection de `main` adaptee au developpement
solo (checks obligatoires, merge via PR, push direct interdit).

A partir de maintenant :

- toutes les nouvelles fonctionnalites partent de RC3 ;
- les moteurs principaux restent gelee ;
- toute evolution doit etre justifiee par un besoin utilisateur, un retour pilote
  ou un bug.

## Vue Globale

| Sprint | Phase | Objectif | Livrable demo |
| --- | --- | --- | --- |
| 00 | P0 | Bootstrap monorepo | App demarre localement |
| 01 | P1 | Kernel minimal | Commands, events, config, logging |
| 02 | P1 | Identity & tenant context | utilisateur demo authentifie |
| 03 | P2 | Session & conversation | chat de simulation |
| 04 | P2 | Scenario & persona | client simule contextualise |
| 05 | P3 | CRM fictif | dossier client consultable |
| 06 | P3 | Actions metier | verify identity, create ticket |
| 07 | P3 | Procedure engine | checklist et obligations |
| 08 | P4 | Evaluation QA | score final rule-based |
| 09 | P4 | Coaching feedback | feedback et recommandations |
| 10 | P5 | Dashboard minimal | historique et KPI simples |
| 11 | P6 | Observabilite & hardening | logs, metrics, traces de base |
| 12 | P6 | Release candidate MVP | demo stable et documentee |

## Milestone M0 — Repository Ready

Inclut :

- structure monorepo ;
- backend FastAPI ;
- frontend minimal ;
- PostgreSQL ;
- Redis ;
- tests ;
- lint ;
- docker compose.

## Milestone M1 — Simulation Loop

Inclut :

- session ;
- message ;
- persona ;
- scenario ;
- conversation timeline.

## Milestone M2 — Business Actions

Inclut :

- CRM fictif ;
- action engine ;
- procedure engine ;
- event trail.

## Milestone M3 — Learning Value

Inclut :

- evaluation QA ;
- feedback ;
- rapport ;
- progression.

## Milestone M4 — MVP Release Candidate

Inclut :

- observabilite minimale ;
- documentation ;
- seed demo ;
- tests d'integration ;
- packaging local.

---

## Phase 2 — Pilot Success (EP-007/008/009)

Objectif : transformer RC3 en un produit utilise par un premier pilote. La
reussite n'est plus mesuree par des metriques techniques (tests, packages,
moteurs) mais par les KPIs produit ci-dessous.

### EP-007 — Pilot Success

Objectif : permettre a une entreprise de realiser une premiere session sans
assistance.

- **WP-001 Dashboard pilote ✅** (2026-07-31) : endpoint unique
  `GET /api/v1/pilot/dashboard` — 4 widgets (KPI, entonnoir 6 etapes, activite
  recente, alertes), sans metriques techniques ; alimente par les stores de
  persistance via `PersistenceFactory` (memory en demo, Postgres en prod).
- onboarding simplifie ;
- UX des erreurs et des etats vides ;
- documentation d'exploitation.

### EP-008 — Product Observability

Objectif : comprendre precisement l'usage reel.

- persistance des `ProductEvent` ;
- tableaux de bord internes ;
- entonnoir d'utilisation (Wizard -> Simulation -> Rapport -> Feedback) ;
- indicateurs d'abandon.

### EP-009 — Voice Production Readiness

Objectif : transformer le Voice Runtime en differenciateur commercial.

- mesure de latence STT/TTS ;
- qualite audio ;
- interruptions (barge-in) ;
- streaming optimise ;
- metriques de satisfaction.

## Tableau de bord KPI — Release 0.1

Metrique principale du pilot : la validation produit par l'usage.

| KPI | Cible Release 0.1 |
| --- | --- |
| Installation reussie | > 95 % |
| Wizard termine | > 90 % |
| Premiere simulation lancee | > 80 % |
| Simulation terminee | > 70 % |
| Rapport consulte | > 60 % |
| Feedback envoye | > 40 % |
| Satisfaction moyenne | >= 4/5 |
| Temps jusqu'a la premiere simulation | < 5 min |

