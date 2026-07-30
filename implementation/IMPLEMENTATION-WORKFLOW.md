# Implementation Workflow

Mise a jour : 2026-07-28

## Evolution

Au debut du projet, le facteur limitant etait la documentation. Le cycle etait :

```
Architecture -> Documentation -> Plan
```

Apres S06, le facteur limitant devient la qualite du code. Le cycle est maintenant :

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

**Le code devient le livrable principal. La documentation accompagne le code, elle ne le remplace plus.**

## Cycle D'Execution Autonome

Quand un sprint est lance, l'objectif n'est plus "ecrire le document S07".

L'objectif est de livrer du code fonctionnel, teste, propre et documente.

### Phase 1 — Analyse

```
OBJECTIF du sprint
    |
    v
Analyser le depot
    |
    v
Identifier le travail restant
    |
    v
Lister les packages, classes, endpoints, tests a creer
```

Avant d'ecrire une ligne de code :

- comprendre l'objectif
- identifier les composants existants
- comprendre les dependances
- verifier les ADR concernes
- verifier les capabilities impactees

### Phase 2 — Developpement

```
Creer les packages
    |
    v
Implementer les classes
    |
    v
Ecrire les services
    |
    v
Creer les endpoints
    |
    v
Developper le frontend (si applicable)
    |
    v
Creer les migrations Alembic
    |
    v
Ajouter les modeles Pydantic
    |
    v
Implementer les repositories
```

Regles pendant le developpement :

- suivre l'architecture hexagonale
- respecter les contrats Pydantic
- respecter les frontieres entre packages
- ajouter les logs structures
- ajouter le X-Trace-Id
- ajouter l'audit trail pour les actions metier

### Phase 3 — Complétion

Chercher automatiquement et implementer :

- [ ] TODO restants
- [ ] methodes vides (`pass`)
- [ ] `NotImplementedError`
- [ ] interfaces incompletes
- [ ] endpoints manquants
- [ ] tests manquants
- [ ] validations absentes
- [ ] erreurs de typage

Rien ne doit etre laisse en l'etat.

### Phase 4 — Correction

Executer en boucle :

```
pytest
    |
    v
ruff check
    |
    v
mypy / pyright
    |
    v
frontend build (si applicable)
    |
    v
API smoke test
    |
    v
corriger
    |
    v
retester
```

Jusqu'a obtenir :

```
100% vert
```

Aucun sprint n'est termine tant que la boucle n'est pas verte.

### Phase 5 — Refactoring

Apres que tout fonctionne :

- supprimer le code duplique
- ameliorer les noms
- simplifier les services
- decouper les fonctions trop longues
- ameliorer les performances
- renforcer le typage
- eliminer les branches mortes

### Phase 6 — Tests

Pas uniquement des tests unitaires.

- [ ] Tests unitaires (logique metier)
- [ ] Tests d'integration (interfaces)
- [ ] Tests API (endpoints)
- [ ] Tests PostgreSQL (repositories)
- [ ] Tests frontend (composants critiques)
- [ ] Tests multi-tenant (isolation)
- [ ] Tests securite (auth, permissions)
- [ ] Tests de regression ( parcours existants)

### Phase 7 — Verification Architecture

Verifier automatiquement :

- [ ] Aucune dependance interdite
- [ ] Respect des couches (domaine ne depend pas d'infrastructure)
- [ ] Respect des contrats Pydantic
- [ ] Conformite avec l'AEB
- [ ] Respect des ADR
- [ ] Tenant ID present sur les donnees metier
- [ ] Pas de secret hardcode

### Phase 8 — Documentation

La documentation est une consequence, pas un point de depart.

Quand le sprint est termine :

```
Mettre STATUS.md a jour
    |
    v
Mettre DELIVERY-ROADMAP.md a jour
    |
    v
Mettre NEXT-ACTIONS.md a jour
    |
    v
Mettre le CHANGELOG a jour
    |
    v
Mettre le capability catalogue a jour (si nouvelle capability)
    |
    v
Fin
```

Pas l'inverse.

### Phase 9 — Validation Finale

Avant de marquer le sprint termine :

- [ ] Tous les tests passent
- [ ] Le lint est propre
- [ ] Le typage est correct
- [ ] Le frontend build
- [ ] L'API demarre
- [ ] Le parcours demo fonctionne
- [ ] La documentation est a jour
- [ ] Les ADR sont crees (si decisions)
- [ ] Le status est mis a jour

## Definition De "Sprint Termine"

Un sprint est termine quand et seulement quand :

1. Le code est implemente et fonctionnel
2. Tous les tests passent (100% vert)
3. Le lint est propre
4. Le typage est correct
5. La documentation est a jour
6. Le status est mis a jour
7. La demo fonctionne

Pas de "presque termine".

Pas de "on finira plus tard".

Pas de "c'est bon pour le MVP".

## Verification Automatique

L'agent IA doit executer ces commandes avant de marquer un sprint termine :

```bash
# Tests
pytest

# Lint
ruff check .

# Typage
mypy .

# Frontend build (si applicable)
cd apps/frontend && npm run build

# API smoke test
curl http://localhost:8000/health

# Docker (si applicable)
docker compose up -d
docker compose ps
```

Si une commande echoue, le sprint n'est pas termine.

## Anti-Patterns

### A eviter

- ecrire des documents avant le code
- marquer un sprint termine sans tests
- laisser des TODO permanents
- laisser des `pass` dans le code
- ignorer les erreurs de typage
- ignorer les erreurs de lint
- creer des interfaces sans les implementer
- ajouter des endpoints sans les documenter
- fusionner sans que tout soit vert

### A favoriser

- developper d'abord, documenter ensuite
- tester avant de merger
- corriger avant de passer a la tache suivante
- refactoriser apres que tout fonctionne
- verifier l'architecture a chaque etape
- maintenir le status a jour en temps reel

## References

- Implementation Principles : `IMPLEMENTATION-PRINCIPLES.md`
- Definition of Done : `DEFINITION-OF-DONE.md`
- Delivery Governance : `05-delivery/DELIVERY-GOVERNANCE.md`
- Capability Catalog : `09-capabilities/CAPABILITY-INDEX.md`
- ADR Registry : `../adr/ADR-REGISTRY.md`
