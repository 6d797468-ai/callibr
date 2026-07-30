# ADR-0003 — ...

Statut extrait : à valider

Phase : F

Volume : F01 — Monorepo Blueprint & Repository Architecture

Source : [volume](../phase-f-delivery-operations/volume-f01-monorepo-blueprint-repository-architecture.md)

Ligne monolithe : 15336

## Décision Détectée

À compléter depuis le contexte.

## Extrait Source

```text
ADR-0003

...

Chaque ADR est autonome.

Versionné.

7. Prompts
prompts/

platform/

architecture/

engines/

tasks/

qa/

review/

evaluation/

Les prompts sont du code.

8. Contracts
contracts/

api/

events/

commands/

queries/

websocket/

crm/

voice/

Les contrats sont isolés.

9. Schemas
schemas/

json/

yaml/

protobuf/

database/

Tous les schémas partagés.

10. Packages

Les packages partagés.

packages/

core/

kernel/

sdk/

common/

telemetry/

security/

events/

auth/

storage/

llm/

Aucun métier ici.

11. Platform

Services transverses.

platform/

identity/

gateway/

runtime/

observability/

configuration/

scheduler/

notification/

Ces composants servent tous les Engines.

12. Engines

Le cœur du produit.

engines/

conversation/

crm/

evaluation/

analytics/

coaching/

knowledge/

voice/

reporting/

Chaque moteur est autonome.

13. Services

Services applicatifs.

services/

api/

websocket/

worker/

scheduler/

admin/

sync/

Ils orchestrent les moteurs.

14. Infrastructure
infrastructure/

docker/

kubernetes/

terraform/

ansible/

monitoring/

network/

Toute l'infrastructure est versionnée.

15. Deployments
deployments/

dev/

staging/

preprod/

production/

Chaque environnement possède sa configuration.

16. Datasets

Le projet versionne.

datasets/

golden/

benchmarks/

evaluation/

training/

fixtures/

Ces données servent aux tests et aux benchmarks.

17. Tools

Outils internes.

tools/

cli/

migration/

scaffold/

generator/

benchmark/

Ils accélèrent le développement.

18. Scripts

Scripts ponctuels.

scripts/

bootstrap/

maintenance/

cleanup/

release/

Les scripts critiques migrent ensuite vers des outils dédiés.

19. Tests
tests/

unit/

integration/

contract/

performance/

e2e/

chaos/

Les tests globaux du dépôt.

Les moteurs conservent également leurs tests locaux.

20. GitHub
.github/

workflows/

actions/

templates/

labels/

policies/

Toute l'automatisation GitHub.

21. Conventions de nommage

Exemples :

conversation_engine

crm_engine

evaluation_engine

voice_runtime

platform_gateway

Pas d'abréviations ambiguës.

22. README

Chaque dossier important possède :

README.md

Le README décrit :

responsabilité ;
architecture ;
dépendances ;
interfaces ;
exemples.
23. Ownership

Chaque répertoire possède un propriétaire.

Exemple.

owner:

reviewers:

team:

criticality:

Cela facilite les revues.

24. CODEOWNERS

Le dépôt utilise un fichier CODEOWNERS.

Exemple.

engines/conversation/

↓

Conversation Team

Principal Architect

Les revues sont automatisées.

25. Workspace Python

Le projet est organisé comme un workspace.

Chaque moteur reste installable indépendamment.

Exemple.

pip install -e engines/conversation

Cela accélère les tests locaux.

26. Gestion des dépendances

Règles.

Un Engine.

↓

Ne dépend jamais.

↓

D'un autre Engine.

Il dépend uniquement :

des Packages ;
des Contracts ;
des APIs internes ;
du Kernel.
27. Matrice des dépendances
Architecture

↓

Contracts

↓

Packages

↓

Platform

↓

Engines

↓

Services

↓

Applications

Les dépendances remontantes sont interdites.

28. Industrialisation

Le dépôt doit permettre.

développement local ;
CI ;
tests ;
génération de documentation ;
benchmarks ;
génération de prompts ;
génération de SDK.

Tout provient du même référentiel.

29. Bootstrap

Un nouveau développeur doit pouvoir lancer.

git clone

↓

bootstrap

↓

docker compose up

↓

pytest

↓

application opérationnelle

L'onboarding doit être inférieur à une heure.

30. Décisions d'architecture (ADR)

Ce volume formalise les principes suivants :

Monorepo unique.
Architecture documentaire intégrée.
Moteurs isolés.
Packages partagés.
Infrastructure versionnée.
Documentation co-localisée.
Ownership explicite.
```
