# Callibr Implementation Plan

Mise a jour : 2026-07-27

Ce dossier transforme l'Architecture & Engineering Book en plan d'execution concret.

Le principe retenu est le Vertical Slice Delivery : chaque increment doit livrer une capacite utilisable de bout en bout, pas seulement un composant technique isole.

## Entrees De Reference

- Architecture source : `../Architecture & Engineering Book (AEB).md`
- Index AEB : `../AEB-Volumes/AEB-MASTER-INDEX.md`
- Roadmap source : `../AEB-Volumes/phase-f-delivery-operations/volume-f05-implementation-roadmap-sprint-execution-plan.md`
- Monorepo cible : `../AEB-Volumes/phase-f-delivery-operations/volume-f01-monorepo-blueprint-repository-architecture.md`
- Contrats API : `../AEB-Volumes/phase-f-delivery-operations/volume-f02-api-contracts-communication-architecture.md`

## Artefacts

- [Master Plan](00-overview/CALLIBR-IMPLEMENTATION-MASTER-PLAN.md)
- [MVP Scope](00-overview/MVP-SCOPE.md)
- [Delivery Roadmap](01-roadmap/DELIVERY-ROADMAP.md)
- [Epic Backlog](02-backlog/EPIC-BACKLOG.md)
- [Sprint 00 — Bootstrap](03-sprints/SPRINT-00-BOOTSTRAP.md)
- [Sprint 01 — Kernel](03-sprints/SPRINT-01-KERNEL.md)
- [Sprint 02 — Identity](03-sprints/SPRINT-02-IDENTITY.md)
- [Repository Target Structure](04-architecture-to-code/REPOSITORY-TARGET-STRUCTURE.md)
- [Architecture To Code Mapping](04-architecture-to-code/ARCHITECTURE-TO-CODE-MAPPING.md)
- [Delivery Governance](05-delivery/DELIVERY-GOVERNANCE.md)
- [Risk Register](06-risks/RISK-REGISTER.md)
- [Implementation Decisions](07-decisions/IMPLEMENTATION-DECISIONS.md)

## Decision De Demarrage

Le premier objectif de developpement n'est pas de construire toute la plateforme.

Le premier objectif est de livrer un MVP textuel complet :

1. creer un tenant local ;
2. creer un utilisateur ;
3. lancer une simulation SAV ;
4. dialoguer avec un client simule ;
5. executer des actions CRM fictives ;
6. terminer la session ;
7. generer une evaluation QA simple ;
8. afficher un rapport minimal.

