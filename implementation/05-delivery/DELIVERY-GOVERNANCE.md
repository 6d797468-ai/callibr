# Delivery Governance

Mise a jour : 2026-07-28

## Cycle De Travail

Le facteur limitant n'est plus la documentation. C'est la qualite du code.

Le cycle de travail est :

```
Architecture (AEB)
    -> Sprint
    -> Developpement
    -> Tests
    -> Correction
    -> Refactoring
    -> Documentation
    -> Validation
```

Pour le cycle complet, voir : [Implementation Workflow](../IMPLEMENTATION-WORKFLOW.md)

## Cadence

- sprint : 2 semaines ;
- demo interne : fin de sprint ;
- revue architecture : a chaque epic critique ;
- release candidate MVP : sprint 12.

## Definition Of Ready

Une story est prete si :

- besoin utilisateur clair ;
- criteres d'acceptation ;
- impact architecture connu ;
- contrats API/events identifies ;
- donnees necessaires connues ;
- risques notes.

## Definition Of Done

La definition of done complete se trouve dans :

[Definition of Done](../DEFINITION-OF-DONE.md)

Resume :

- code implemente ;
- tests ajoutes ;
- lint/type checks OK ;
- documentation mise a jour ;
- logs minimum presents ;
- erreurs standardisees ;
- aucun secret hardcode ;
- demo possible ;
- migration Alembic si changement de schema ;
- ADR si decision architecturale ;
- capability catalogue mis a jour si nouvelle capability.

## Gates MVP

| Gate | Controle |
| --- | --- |
| Architecture | respecte hexagonal + contracts |
| Security | pas de secret, auth sur routes protegees |
| Data | tenant_id present sur donnees metier |
| Tests | unitaires critiques + smoke |
| UX | parcours demo sans blocage |
| Ops | demarrage local documente |

## Politique D'ADR

ADR requis si :

- choix technologique majeur ;
- changement structure repo ;
- contrat API public ;
- changement modele donnees critique ;
- contournement d'un principe AEB.

