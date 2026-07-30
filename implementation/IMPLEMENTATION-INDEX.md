# Implementation Index

Mise a jour : 2026-07-28

## Statut

Le plan d'implementation Callibr est initialise et la premiere tranche executable a demarre.

Phase courante :

P4 — Learning Value MVP.

Objectif immediat :

Stabiliser l'evaluation detaillee, le rapport de session et le prochain Procedure Engine.

## Hierarchie De Decoupage

```
AEB (architecture cible)
  -> Business Capabilities (09-capabilities/)
    -> Epics (02-backlog/)
      -> Features
        -> Stories
          -> Tasks
          -> Code
```

## Documents Principaux

### Fondations

- [Master Plan](00-overview/CALLIBR-IMPLEMENTATION-MASTER-PLAN.md)
- [MVP Scope](00-overview/MVP-SCOPE.md)
- [Implementation Principles](IMPLEMENTATION-PRINCIPLES.md)
- [Implementation Workflow](IMPLEMENTATION-WORKFLOW.md)
- [Definition of Done](DEFINITION-OF-DONE.md)

### Capabilities

- [Capability Catalog](09-capabilities/CAPABILITY-INDEX.md)
- [Simulation](09-capabilities/SIMULATION.md)
- [CRM](09-capabilities/CRM.md)
- [Evaluation](09-capabilities/EVALUATION.md)
- [Reporting](09-capabilities/REPORTING.md)
- [Identity](09-capabilities/IDENTITY.md)
- [IAM](09-capabilities/IAM.md)
- [AI Runtime](09-capabilities/AI.md)
- [Scenario](09-capabilities/SCENARIO.md)
- [Session](09-capabilities/SESSION.md)
- [Orchestration](09-capabilities/ORCHESTRATION.md)
- [Procedure](09-capabilities/PROCEDURE.md)
- [Persona](09-capabilities/PERSONA.md)
- [Rule & Decision](09-capabilities/RULE.md)
- [Analytics](09-capabilities/ANALYTICS.md)
- [Multi-Tenant](09-capabilities/MULTI-TENANT.md)
- [Observability](09-capabilities/OBSERVABILITY.md)
- [Domain Packs](09-capabilities/DOMAIN-PACKS.md)

### Delivery

- [Delivery Roadmap](01-roadmap/DELIVERY-ROADMAP.md)
- [Epic Backlog](02-backlog/EPIC-BACKLOG.md)
- [Architecture To Code Mapping](04-architecture-to-code/ARCHITECTURE-TO-CODE-MAPPING.md)
- [Repository Target Structure](04-architecture-to-code/REPOSITORY-TARGET-STRUCTURE.md)
- [Delivery Governance](05-delivery/DELIVERY-GOVERNANCE.md)
- [Risk Register](06-risks/RISK-REGISTER.md)
- [Implementation Decisions](07-decisions/IMPLEMENTATION-DECISIONS.md)
- [Next Actions](NEXT-ACTIONS.md)
- [Implementation Status](STATUS.md)

### Architecture Decision Records

- [ADR Registry](../adr/ADR-REGISTRY.md)
- [ADR Template](../adr/ADR-TEMPLATE.md)
- [ADR-0001 — PostgreSQL](../adr/ADR-0001-POSTGRESQL.md)
- [ADR-0002 — FastAPI](../adr/ADR-0002-FASTAPI.md)
- [ADR-0003 — Hexagonal](../adr/ADR-0003-HEXAGONAL.md)
- [ADR-0004 — Monorepo](../adr/ADR-0004-MONOREPO.md)
- [ADR-0005 — Vertical Slice](../adr/ADR-0005-VERTICAL-SLICE.md)
- [ADR-0006 — Pydantic](../adr/ADR-0006-PYDANTIC-CONTRACTS.md)
- [ADR-0007 — Alembic](../adr/ADR-0007-ALEMBIC-MIGRATIONS.md)

## Audits

- [Audit complet Callibr - AEB, implementation et trajectoire Enterprise](08-audits/AUDIT-2026-07-28-CALLIBR-AEB-IMPLEMENTATION.md)

## Sprints Initiaux

- [Sprint 00 — Bootstrap](03-sprints/SPRINT-00-BOOTSTRAP.md)
- [Sprint 01 — Kernel](03-sprints/SPRINT-01-KERNEL.md)
- [Sprint 02 — Identity](03-sprints/SPRINT-02-IDENTITY.md)
- [Sprint 03 — Simulation Core MVP](03-sprints/SPRINT-03-SIMULATION-CORE.md)
- [Sprint 04 — Persistence & Audit Trail](03-sprints/SPRINT-04-PERSISTENCE-AUDIT.md)
- [Sprint 05 — Local IAM MVP](03-sprints/SPRINT-05-LOCAL-IAM.md)
- [Sprint 06 — Detailed Evaluation & Session Report](03-sprints/SPRINT-06-EVALUATION-REPORT.md)

## Ordre De Decoupage

```
AEB (architecture cible)
  -> Business Capabilities (09-capabilities/)
    -> Epics (02-backlog/)
      -> Features
        -> Stories
          -> Tasks
          -> Code
```

## Ordre D'Execution

1. Valider le scope MVP.
2. Executer Sprint 00. Termine.
3. Executer Sprint 01. Termine pour le kernel minimal, reste a durcir.
4. Demarrer la boucle simulation. Implementation initiale terminee.
5. Executer Sprint 02 pour l'identite demo et le contexte tenant. Implementation demo terminee.
6. Ajouter la persistance PostgreSQL et l'audit trail. Implementation initiale terminee.
7. Durcir l'IAM avec login local, token bearer et stockage users/tenants. Implementation initiale terminee.
8. Introduire l'evaluation detaillee et le rapport de session. Implementation initiale terminee.
9. Introduire le Procedure Engine MVP.

## Decision Forte

Le premier code doit servir la demo MVP.

La plateforme Enterprise complete reste guidee par l'AEB, mais le developpement commence par une tranche verticale simple.

L'architecture ne depend jamais des sprints. Les sprints ne definissent pas l'architecture.
