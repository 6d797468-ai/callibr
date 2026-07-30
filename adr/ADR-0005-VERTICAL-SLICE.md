# ADR-0005 — Vertical Slice Delivery

Date : 2026-07-27
Statut : Accepte
Decideurs : Callibr Architecture Team
Contexte : Phase P0 — Bootstrap

## Contexte

Callibr a un architecture cible tres ambitieuse (AEB avec 125+ volumes) mais doit livrer rapidement une premiere version executable.

Le risque principal est de passer des mois a construire une infrastructure sans jamais livrer de valeur utilisateur.

## Decision

Callibr adopte la Vertical Slice Delivery : chaque sprint livre une capacite complete et observable de bout en bout.

## Alternatives

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| Vertical Slice | Valeur livrable rapide, feedback continu, integration continue | Plus de travail par sprint (couches completes) |
| Horizontal Layers | Infrastructure solide avant la logique | Risque de ne jamais livrer de valeur |
| Big Design Up Front | Architecture coherente | Rigidite, feedback tardif |
| Component-Based | Independance des composants | Integration tardive possible |

## Consequences

### Positives

- Chaque sprint produit un resultat observable et testable
- Le feedback arrive tot et souvent
- L'integration est continue par nature
- Le risque de "building the wrong thing" est reduit

### Negatives

- Plus de travail par sprint (API + logique + persistence + tests + docs)
- Necessite de prioriser les capacites critiques en premier

### Neutres

- L'architecture AEB reste la reference, mais l'execution est pragmatique

## References

- AEB : A00-A02 — Foundations, Vision, Architecture, Constitution
- Master Plan : Strategie "Vertical Slice Delivery"
- Capability : Toutes les capabilities du catalogue
- Implementation : Tous les sprints
