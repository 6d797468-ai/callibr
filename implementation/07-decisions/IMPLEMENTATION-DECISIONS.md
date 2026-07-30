# Implementation Decisions

Mise a jour : 2026-07-27

## DEC-IMP-001 — Vertical Slice Delivery

Decision :

Livrer Callibr par capacites utilisables de bout en bout.

Raison :

Reduire le risque d'integration tardive.

## DEC-IMP-002 — MVP Textuel Avant Voice

Decision :

La voix est exclue du MVP initial.

Raison :

Valider d'abord le coeur simulation, CRM, evaluation.

## DEC-IMP-003 — Stub IA Deterministe Au Debut

Decision :

Les premiers tests utilisent un client simule deterministe avant integration LLM.

Raison :

Garantir tests reproductibles et vitesse de developpement.

## DEC-IMP-004 — Multi-Tenant Des Le Sprint 02

Decision :

Le tenant context est introduit avant les donnees metier.

Raison :

Eviter une refonte SaaS plus tard.

## DEC-IMP-005 — Monorepo Modulaire

Decision :

Le projet demarre en monorepo avec packages Python modulaires.

Raison :

Accelerer le MVP tout en preservant les frontieres d'architecture.

