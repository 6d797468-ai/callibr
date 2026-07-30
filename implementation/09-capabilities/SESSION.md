# CAP-09 — Session

Mise a jour : 2026-07-28

## Definition

Capacite de gerer le cycle de vie complet d'une session de simulation : creation, etat, historique, persistence et archivage.

## Stabilite

La session est un concept transversal. Elle supporte la simulation, l'evaluation et le reporting.

## AEB Volumes Concernes

- B02 — Simulation Operating Engine (SOE)
- B08 — Conversation Runtime Engine (CoRE)

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Session Service | `engines/simulation/` | Actif |
| Session Store | `packages/persistence/` | Actif |
| Session Timeline | `engines/simulation/` | Actif |

## Cycle De Vie

```
Creee -> En cours -> Terminee -> Archivee
```

## Criteres De Stabilite

Une feature session est terminee quand :

- Une session peut etre creee,inee et terminee
- L'historique est persiste
- Les tests couvrent le cycle de vie
