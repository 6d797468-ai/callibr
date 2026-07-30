# Definition of Done

Mise a jour : 2026-07-28

## Role

Une feature n'est terminee que si TOUS les criteres suivants sont remplis.

Pas d'exception.

Pas de "presque termine".

Pas de "on livree et on corrige apres".

## Criteres Obligatoires

### Code

- [ ] Code implemente et fonctionnel
- [ ] Code reviewe (au moins 1 autre personne ou agent)
- [ ] Aucun warning de lint (ruff)
- [ ] Aucun error de type (mypy/pyright)
- [ ] Aucun secret hardcode

### Tests

- [ ] Tests unitaires pour la logique metier
- [ ] Tests d'integration pour les interfaces
- [ ] Tests E2E pour les parcours critiques (si applicable)
- [ ] Tous les tests passent

### API

- [ ] Documentation OpenAPI a jour
- [ ] Contrats Pydantic valides
- [ ] Routes protegees (auth) si necessaire
- [ ] Erreurs standardisees (format consistent)

### Donnees

- [ ] Migrations Alembic creees et testees
- [ ] Tenant ID present sur les donnees metier
- [ ] Index crees pour les requetes frequentes
- [ ] Pas de donnees orphelines

### Observabilite

- [ ] Logs structures presents
- [ ] X-Trace-Id propage
- [ ] Erreurs loggees avec contexte
- [ ] Metriques de base (si applicable)

### Audit

- [ ] Audit trail pour les actions metier critiques
- [ ] Evenements emis pour les changements d'etat
- [ ] Historique des changements de donnees

### Documentation

- [ ] README du module a jour
- [ ] CHANGELOG mis a jour
- [ ] Architecture mapping mis a jour (si nouveau composant)
- [ ] Capability catalogue mis a jour (si nouvelle capability)

### Gouvernance

- [ ] ADR cree si decision architecturale
- [ ] Epic/Story rattache dans le backlog
- [ ] Sprint task creee

## Criteres Optionnels (selon contexte)

- [ ] Performance teste (si composant critique)
- [ ] Securite auditee (si route exposee)
- [ ] Demo preparable (si fonctionnalite visible)

## Niveaux De Done

| Niveau | Description |
| --- | --- |
| Done | Tous les criteres obligatoires remplis |
| Done + | Criteres optionnels remplis |
| Not Done | Au moins un critere obligatoire manquant |

## Utilisation

Avant de marquer une story comme "Done" :

1. Verifier chaque critere
2. Si un critere n'est pas rempli, la story reste "In Progress"
3. Si un critere ne s'applique pas, le justifier dans la description
4. Si un critere est impossible a remplir, creer un ticket de dette technique

## References

- Implementation Principles : `implementation/IMPLEMENTATION-PRINCIPLES.md`
- Delivery Governance : `implementation/05-delivery/DELIVERY-GOVERNANCE.md`
- Capability Catalog : `implementation/09-capabilities/`
