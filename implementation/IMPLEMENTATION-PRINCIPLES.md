# Implementation Principles

Mise a jour : 2026-07-28

## Role

Ce document est la boussole de developpement de Callibr.

Il empeche la derive du projet.

Il doit etre consulte avant chaque decision de code.

## Le Code Comme Livrable Principal

Callibr est passe d'un projet documente a un projet pilote par l'execution.

Le code est le livrable principal.

La documentation accompagne le code, elle ne le remplace plus.

Le cycle de travail :

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

Pour le cycle complet, voir : `IMPLEMENTATION-WORKFLOW.md`

## Principes Fondamentaux

### 1. Toutes les fonctionnalites sont verticales

Chaque feature livree doit etre complete : API, logique metier, persistence, tests, documentation.

Pas de "couches a moitie faites".

Pas de "on fera l'API plus tard".

### 2. Toujours testes

Pas de merge sans tests.

Les tests unitaires couvrent la logique metier.

Les tests d'integration couvrent les interfaces.

Les tests E2E couvrent les parcours critiques.

### 3. Toujours documentes

Chaque module a un README.

Chaque API a une documentation OpenAPI.

Chaque decision a un ADR.

Chaque capability a un document dans le catalogue.

### 4. Toujours observables

Chaque composant emet des logs structures.

Chaque requete API a un X-Trace-Id.

Chaque erreur est standardisee.

### 5. Toujours auditable

Chaque action metier est tracée dans un audit trail.

Chaque changement de donnees est historise.

Chaque evenement est persiste.

### 6. Toujours compatibles AEB

Toute decision technique doit respecter l'architecture AEB.

Tout ecart doit etre justifie par un ADR.

L'AEB reste la verite architecturale.

### 7. Pas de dette volontaire

Pas de "TODO permanent".

Pas de "on corrigera plus tard" sans ticket.

Pas de "c'est bon pour le MVP" sans plan de durcissement.

### 8. Pas de magie

Pas de code implicitement execute.

Pas de conventions non documentees.

Pas de "ca marche, on ne sait pas pourquoi".

### 9. Separation des couches

```
AEB (architecture cible)
  -> Business Capabilities (catalogue)
    -> Epics (backlog)
      -> Features
        -> Stories
        -> Tasks
        -> Code
```

L'architecture ne depend pas des sprints.

Les sprints ne definissent pas l'architecture.

### 10. Pragmatisme guide

L'AEB est la vision.

Le plan d'implementation est la realite.

Le code est l'execution.

Ces trois niveaux ne doivent jamais etre melanges.

## Consequences De Violation

Si un principe est viole :

1. Identifier le principe viole
2. Creer un ADR justifiant l'ecart
3. Documenter la dette technique associee
4. Planifier le correctif dans un sprint futur

## References

- AEB : A00-A02 — Foundations, Vision, Architecture, Constitution
- Implementation Workflow : `IMPLEMENTATION-WORKFLOW.md`
- Capability Catalog : `implementation/09-capabilities/`
- Definition of Done : `implementation/DEFINITION-OF-DONE.md`
- Delivery Governance : `implementation/05-delivery/DELIVERY-GOVERNANCE.md`
