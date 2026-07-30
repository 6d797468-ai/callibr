# CAP-12 — Persona

Mise a jour : 2026-07-28

## Definition

Capacite de charger et d'utiliser des personas client : profil, comportement, emotions, style de communication.

## Stabilite

Le persona est un concept stable. Les personas specifiques changent, mais la capacite de les charger reste.

## AEB Volumes Concernes

- B04 — Customer Persona Engine & Emotion Engine
- B04 (partie 2) — Behavior Simulation Engine (BSE)

## Composants

| Composant | Emplacement | Statut |
| --- | --- | --- |
| Persona Seed | `domains/support_sav/` | Actif (2 personas) |
| Persona Runtime | `engines/persona/` | Planifie |

## Criteres De Stabilite

Une feature persona est terminee quand :

- Un persona peut etre charge depuis le domaine
- Le comportement du client simule suit le persona
- Les tests couvrent le chargement de persona
