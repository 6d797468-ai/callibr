# ADR-0004 — Monorepo Modulaire

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P0 — Bootstrap

## Contexte

Callibr est compose de multiples composants :

- Backend API (FastAPI)
- Frontend (React)
- Packages partages (kernel, contracts, persistence, telemetry)
- Engines (simulation, crm, evaluation, etc.)
- Domaines (support_sav, etc.)
- Infrastructure (postgres, redis, docker)

Ces composants doivent etre developpes ensemble tout en preservant leurs frontieres.

## Decision

Callibr utilise un monorepo avec packages Python modulaires.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| Monorepo | Deploy atomique, partage de code facile, refactoring global | Build plus long, necessite un bon outillage |
| Multi-repo | Independance, deploy isole | Couplage difficile a gerer, duplication |
| Poly-repo avec workspace | Mix des deux | Complexite de configuration |

## Consequences

### Positives

- Deploy atomique d'une feature full-stack
- Partage de contrats entre backend et frontend
- Refactoring global possible sans coordination multi-repo
- Code review global avant merge

### Negatives

- Build plus long a mesure que le repo grandit
- Necessite un bon outillage (ruff, pytest, Makefile)
- Discipline sur les frontieres entre packages

### Neutres

- La structure de dossiers (apps/, packages/, engines/, platform/, domains/) est le premier outil d'organisation

## References

- AEB : D01 — Monorepo, Code Organization & Engineering Standards
- Capability : CAP-10 — Orchestration
- Implementation : Sprint 00 (monorepo bootstrap)
