# ADR Template

Mise a jour : 2026-07-28

## Utilisation

Copier ce template pour creer un nouvel ADR.

## Format

```
# ADR-XXXX — [Titre]

Date : YYYY-MM-DD
Statut : Accepte | Depasse | Remplace
Decideurs : [noms]
Contexte : [ lien vers le contexte ]
```

## Sections Obligatoires

### Contexte

Quel est le probleme qui necessite cette decision ?

### Decision

Quelle est la decision prise ?

### Alternatives

Quelles alternatives ont ete considerees ?

| Alternative | Avantages | Inconvenients |
| --- | --- | --- |
| A | ... | ... |
| B | ... | ... |

### Consequences

Quelles sont les consequences de cette decision ?

- Positives :
- Negatives :
- Neutres :

### Packages Impactes

Quels composants du code sont modifies par cette decision ?

```yaml
affected_packages:
  - packages/contracts
  - apps/api
  - engines/evaluation
```

### Verification

Quels tests doivent etre executes pour valider cette decision ?

```yaml
verification:
  - pytest
  - mypy
  - architecture tests
  - lint
```

### Statut

- Accepte : la decision est active
- Depasse : une decision ulterieure l'a remplacee
- Remplace : une decision ulterieure l'a remplacee

### References

- Liens vers les volumes AEB concernes
- Liens vers les capabilities impactees
- Liens vers les epics/stories associees
