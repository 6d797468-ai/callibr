# Next Actions

Mise a jour : 2026-07-31

## CURRENT TARGET

Release 0.1 — Pilot Success

### Objective

Un premier client :

1. installe Callibr ;
2. lance une simulation ;
3. termine un scenario ;
4. telecharge un rapport ;
5. laisse un feedback.

## EP-007 — Pilot Success

Priorite : P0

- Dashboard pilote ✅ (EP-007 WP-001 — cockpit 4 widgets, endpoint unique `/api/v1/pilot/dashboard`)
- Onboarding final
- Error UX
- Empty states

Ordre d'execution recommande (prochaines etapes) :

1. Error UX (aucun ecran casse)
2. Empty states (aucune page vide)
3. Onboarding final (polish)

## EP-008 — Product Observability

Priorite : P0

- Product Analytics persistants
- Funnel Wizard -> Simulation -> Rapport -> Feedback
- Dashboard KPI

Cibles Release 0.1 : installation > 95 %, wizard > 90 %, premiere simulation > 80 %,
simulation terminee > 70 %, rapport consulte > 60 %, feedback envoye > 40 %,
satisfaction >= 4/5, temps jusqu'a la premiere simulation < 5 min.

## EP-009 — Voice Production Readiness

Priorite : P1

- Voice latency (STT/TTS)
- Streaming optimise
- Barge-in (interruptions)
- Metriques de satisfaction

## Rappels

- Toute evolution part de v0.1.0-rc3.
- Les moteurs principaux restent gelés.
- Toute evolution est justifiee par un besoin utilisateur, un retour pilote ou un bug.
