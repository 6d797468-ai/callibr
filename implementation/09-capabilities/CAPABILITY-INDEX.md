# Capability Catalog

Mise a jour : 2026-07-28

## Role

Ce catalogue est le pont entre l'AEB (architecture cible) et le backlog (execution).

Les capabilities sont stables. Elles changent rarement.

Les epics, features et stories derivent de ces capabilities.

## Hierarchie De Decoupage

```
AEB (architecture cible)
  -> Business Capabilities (ce document)
    -> Epics (backlog)
      -> Features
        -> Stories
          -> Tasks
          -> Code
```

## Regles

1. Une capability correspond a une capacite business stable du plateau.
2. Une capability ne disparait pas quand un epic est termine.
3. Chaque epic doit etre raccordable a au moins une capability.
4. Chaque capability peut supporter plusieurs epics successifs.
5. Les capabilities ne dependent pas des sprints.

## Catalogue

| ID | Capability | AEB Volumes | Statut |
| --- | --- | --- | --- |
| CAP-01 | [Simulation](SIMULATION.md) | B02, B08, C01 | En cours |
| CAP-02 | [CRM](CRM.md) | B07 | En cours |
| CAP-03 | [Evaluation](EVALUATION.md) | B09 | En cours |
| CAP-04 | [Reporting](REPORTING.md) | B10 | Planifie |
| CAP-05 | [Identity](IDENTITY.md) | C03, J01 | En cours |
| CAP-06 | [IAM](IAM.md) | J01-J03 | MVP local |
| CAP-07 | [AI Runtime](AI.md) | B03, E01-E06, H01-H15 | Stub deterministe |
| CAP-08 | [Scenario](SCENARIO.md) | B05 | En cours |
| CAP-09 | [Session](SESSION.md) | B02, B08 | En cours |
| CAP-10 | [Orchestration](ORCHESTRATION.md) | C01, C02 | Kernel minimal |
| CAP-11 | [Procedure](PROCEDURE.md) | B05, B06 | Planifie |
| CAP-12 | [Persona](PERSONA.md) | B04 | Seed data |
| CAP-13 | [Rule & Decision](RULE.md) | B06 | Planifie |
| CAP-14 | [Analytics](ANALYTICS.md) | B10, I11-I20 | Planifie |
| CAP-15 | [Multi-Tenant](MULTI-TENANT.md) | C03 | En cours |
| CAP-16 | [Observability](OBSERVABILITY.md) | K07, H10 | Baseline |
| CAP-17 | [Domain Packs](DOMAIN-PACKS.md) | G00-G20 | Seed Support/SAV |
